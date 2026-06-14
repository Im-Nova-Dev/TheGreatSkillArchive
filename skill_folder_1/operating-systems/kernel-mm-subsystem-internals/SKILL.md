---
name: kernel-mm-subsystem-internals
description: >
  Teach Linux kernel memory management subsystem internals at the mechanistic level:
  page allocator internals, page reclaim, deferred dequeue in kernel primitives,
  shrinker recursion risks, alloc-in-reclaim deadlock patterns, and how mm
  subsystem changes (including maintainer transitions) affect kernel stability.
  Covers practical debug and regression mitigation for 6.x/7.x kernels.
trigger: >
  questions about Linux kernel memory management architecture, page allocator internals,
  mm subsystem maintainer transition, Linux 7.x mm regressions, shrinker recursion,
  alloc-in-reclaim deadlock, oom_killer, transparent huge pages, page reclaim issues,
  memory debugging via bpftrace/slub_debug, or kdump analysis.
---

# Linux Kernel Memory Management Subsystem Internals

## Scope
Mechanistic deep-dive of the Linux `mm/` subsystem: allocation paths, reclaim,
compaction, NUMA balancing, MM/fs/vm crossover regressions, and how the 2026
maintainer transition affects change velocity. Focus on object lifetimes and
concurrency invariants rather than usage tutorials.

## Prerequisites
- C kernel basics: `kmalloc`, `kfree`, `atomic_t`, `mutex`, `spinlock`.
- Linux page frame abstraction: `struct page`, `struct page_frag`, `ZONE_NORMAL`,
  `ZONE_DMA`, `ZONE_DMA32`, `ZONE_MOVABLE`.
- I/O path basics: bio, block layer, filesystem `address_space`.
- `bpftrace` or `perf kvm` event tracing for kernel internals.

## Lesson 1: mm/ directory scope and why it touches everything
164+ interlinked source files. Major areas:

| Area | Key files |
|------|-----------|
| Page allocator | `mm/page_alloc.c`, `mm/internal.h` |
| Slab/SLUB/SLOB | `mm/slub.c`, `mm/slab.c` |
| Page reclaim | `mm/vmscan.c` |
| Memory compaction | `mm/compaction.c` |
| Transparent Huge Pages | `mm/huge_memory.c` |
| NUMA balancing | `mm/mempolicy.c`, `mm/autonuma.c` |
| cgroup memory controller | `mm/memcontrol.c` |
| OOM killer | `mm/oom_kill.c` |
| CMA | `mm/cma.c` |
| Memory hotplug | `mm/memory_hotplug.c` |
| File-backed page cache | `mm/filemap.c`, `mm/truncate.c` |

Cross-subsystem dependencies: networking (`net/core/page_pool.c`), block I/O
(`bio`), all filesystems (shrinkers, `invalidate_inode_pages2`), device drivers
(DMA coherent allocations via `dma_alloc_coherent`).

**Consequence**: An mm regression rarely stays in mm/. It propagates into
filesystem corruption, network Rx stalls, block-layer timeouts, or driver crashes.

## Lesson 2: Page allocator fast path and slow path
Fast path (`rmqueue()`):
1. Per-CPU page freelist (`struct per_cpu_pages`).
2. Zone watermark check against `min`, `low`, `high`.
3. Migratetype matching to avoid fragmentation (`MIGRATE_MOVEABLE`,
   `MIGRATE_RECLAIMABLE`, `MIGRATE_UNMOVABLE`).

Slow path (`__alloc_pages_slowpath()`):
1. Wake kswapd, direct reclaim.
2. Try compaction (`compact_zone()`); may stall on zone lock.
3. Fallback to lower zone (e.g., `ZONE_NORMAL` → `ZONE_DMA`).
4. OOM kill if all else fails.

### Critical invari
- A page on the PCP freelist is **not** on the buddy freelist; double-free
  corrupts both lists and crashes the allocator.
- `alloc_pages(GFP_KERNEL)` **must not** be called from atomic context
  (interrupt, softirq, holding spinlock). Use `GFP_ATOMIC`, or `GFP_NOWAIT`.

## Lesson 3: alloc-in-reclaim deadlock
**Pattern**: filesystem or driver calls `kmalloc(GFP_KERNEL)` from a shrinker
callback, or from `release_freepages()` during reclaim.

**Why it deadlocks**:
1. Reclaim holds `fs_reclaim` lock (`current->flags & PF_FSTRANS`).
2. `kmalloc(GFP_KERNIAL)` tries to reclaim memory.
3. `shrink_slab()` calls the same shrinker recursively → BUG / WARN.
4. On ext4/btrfs/XFS, this has caused filesystem freeze under memory pressure.

**Mitigation**:
- Shrinkers must use `GFP_NOFS` or `GFP_NOIO`; never `GFP_KERNEL`.
- Use `mapping_set_gfp_mask()` to constrain `page_cache_alloc()`.
- Kernel 5.19+ added `SGP_NOHWPOISON` and gfp mask propagation helpers.

## Lesson 4: Shrinker recursion and VFS-MM crossover
Filesystems register shrinkers to reclaim inode/dentry caches:

```c
static int myfs_shrink_scan(struct shrinker *shrinker, struct shrink_control *sc) {
    // Must not allocate GFP_KERNEL memory!
}
```

The kernel checks via `gfp_zone()` and `mapping_gfp_mask()`. VFS uses
`shrink_slab()` across mount, unmount, and memory-pressure paths.

**Regression pattern**: A new VFS feature (e.g., shared subtree ACLs, idmapped
mounts) introduces an allocation from `shrink_control` callbacks without
propagating the gfp mask → regression.

**Watch for**: btrfs and XFS shrinker changes in `mm/vmscan.c` release notes.

## Lesson 5: Page pool and network Rx path coupling
`net/core/page_pool.c` depends on mm for page recycling during receive:

- `page_pool_alloc_pages()` calls `alloc_pages()` directly under NAPI softirq.
- Under memory pressure, allocator fallback may take the full reclaim path,
  breaking latency guarantees on the network Rx path.
- Workaround: page pool pre-allocates pages at device open; drivers implement
  `page_pool` recycling with optimizations (`PP_FLAG_DMA_MAP`).

**Implication for io_uring ZCRX**:
ZCRX reuses page pool for DMA into userspace pages. Any change to page recycling
or `page->freelist` layout can break fast paths without changing a single line of
networking code. Same applies to AF_XDP.

## Lesson 6: Transparent Huge Pages (THP) pitfalls
- `khugepaged` scans for collapse candidates; runs as a kernel thread per node.
- Collapse races with `mmap_write_lock` and `page_count`.
- 7.x trend: `madvise(MADV_COLLAPSE)` support added; userspace can trigger collapse
  without khugepaged.
- **Fragmentation risk**: THP compaction can fragment the buddy allocator and
  degrade workload latency on memory-constrained hosts.

## Lesson 7: Subsystem governance and the 2026 maintainer transition
Andrew Morton stepped down as sole mm maintainer after 26 years in April 2026.
As of May 2026 the community had not announced a formal replacement.

**Effect on regression risk**:
- Slower review throughput for MM/fs crossover changes (shrinker recursion,
  alloc-in-reclaim).
- Likely conservative 7.1/7.2 merge window for mm complexity.
- Parallel concerns: Rust-for-Linux concurrency patterns must still honor mm
  locking rules.

**Production recommendations**:
1. Pin kernel mm configuration to known-good for critical loads until mm tree
   stabilizes post-transition.
2. Enable `CONFIG_SLUB_DEBUG=y`, `CONFIG_DEBUG_LOCK_ALLOC=y` during kernel
   testing.
3. Monitor `dmesg` for `shrink_slab` recursion, `alloc_pages` fallback warnings,
   and `SLUB` corruption reports.

## Exercises / thought problems
1. Walk the slab allocator path for `kmalloc(256, GFP_KERNEL)`: identify each
   lock acquired and the maximum allocation fallback chain. Under what gfp_mask
   would this fail with `-ENOMEM`?
2. Design a `bpftrace` script that traces `shrink_slab` entry and shows the
   time spent in each shrinker callback. Which shrinker is the most expensive on
   a system running PostgreSQL + ext4 + kernel TCP?
3. Hypothesize: if a new mm maintainer prefers conservative shrinker changes,
   which current feature (e.g., DAMON-based proactive reclaim, cgroup v3 mm
   pressure events, memcg `swap:1` highlimit) is most at risk of delay in 7.2?
4. AF_XDP user reports Tx queue stalls after upgrading from 6.6 to 7.0. You
   suspect page pool/cma interaction. Sketch the debug plan.
