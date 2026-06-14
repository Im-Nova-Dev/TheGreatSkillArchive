---
name: kernel-mm-maintainer-transition-2026
description: >
  Teach the Linux kernel memory management (mm) subsystem maintainer transition in 2026,
  focusing on subsystem size, previous single-maintainer bottleneck, and implications
  for change velocity and regression risk in post-6.19/7.x kernels.
trigger: >
  questions about Andrew Morton stepping down as mm maintainer, Linux MM maintainership,
  kernel memory subsystem governance, post-2026 kernel memory subsystem stability,
  mm regression risk, or filesystem/memory subsystem coupling.
---

# Linux Memory Management Subsystem Maintainer Transition (2026)

## Scope
Mechanistic and organizational overview of the Linux kernel MM maintainer transition
announced April 21, 2026, and its implications for developers, distro maintainers,
and systems engineers who rely on stable memory behavior across kernel upgrades.

## Prerequisites
- Linux kernel file layout: `mm/` directory, `fs/*` and `mm/` interaction through
  `shrinkers`, `page reclaim`, and `VMA`/`address_space` abstractions.
- Basic understanding of MM responsibilities: page allocator (`buddy`/`slab`),
  reclaim, compaction, NUMA balancing, THP, cgroup memory.
- Mailing list / git workflow: `linux-mm@kvger.org`, `mm-stable` trees.

## Lesson 1: What the mm subsystem actually covers
MM is one of the widest-reaching subsystems in the kernel:

- Memory allocation: `mm/page_alloc.c`, `mm/slab.c`, `mm/slub.c`
- Page reclaim and kswapd: `mm/vmscan.c`
- Transparent Huge Pages (THP): `mm/huge_memory.c`
- NUMA balancing: `mm/mempolicy.c`, `mm/autonuma.c`
- cgroup memory controller: `mm/memcontrol.c`
- OOM killer: `mm/oom_kill.c`
- Device memory / CMA: `mm/cma.c`
- Memory hotplug: `mm/memory_hotplug.c`

It touches every other subsystem. A regression in MM is rarely isolated:
filesystems, networking (page pool), block I/O (bio), and drivers all observe the
same allocator behavior.

## Lesson 2: The maintainer role and its unique constraints
Andrew Morton's 26-year tenure was unusual in kernel history:

- `mm/` patch review bottleneck: most MM patches still flow through the `-mm` tree
  before reaching Linus's tree.
- Guidelines emphasis: patches touching both `fs/` and `mm/` require explicit MM review.
- Cross-subsystem callback changes: filesystems implementing `address_space_operations`
  or shrinkers depend on MM ABI stability.

## Lesson 3: Implications of a leadership vacuum
As of May 2026 the kernel community had not announced a formal succession plan after
the Zagreb summit. Probable near-term effects:

1. **Slower review throughput for complex MM changes** — especially MM/fs crossovers
   such as filesystem shrinker recursion and alloc-in-reclaim paths.
2. **Preference for conservative patches in 7.1/7.2** — distro kernels may freeze MM
   behavior to reduce risk even if `-next` introduces aggressive changes.
3. **Increased pressure on co-maintainers** — expected recipients of more review:
   `mm/vmscan.c` (stable tree maintainers), `mm/slab` maintainers, and likely new
   elections at the next kernel summit.

## Lesson 4: Concrete areas to watch for regressions
Given prior history, watch these code paths most carefully when upgrading to 7.x:

1. **Large block allocation** — StorageNewsletter reported allocation time for large
   blocks dropped from 3.6 s to 0.43 s. Verify on your workload that this optimization
   does not introduce fragmentation under heavy THP use.
2. **alloc-in-reclaim** — Filesystems or drivers allocating under reclaim can re-enter
   the allocator and deadlock with shrinkers. This is the same family as PF_MEMALLOC +
   GFP_NOFAIL anti-pattern (referenced in source-feed).
3. **Page pool and network Rx path** — `net/core/page_pool.c` depends on MM for page
   recycling. Any change to page-recycling or `page->freelist` handling can break
   AF_XDP and io_uring ZCRX fast paths.
4. **shrinkers recursion** — Filesystems with active shrinkers (btrfs, XFS) observed
   VFS/MM coupling regressions during the 6.x series.

## Lesson 5: What this means for production operators
- Run MM-heavy workloads (databases, large-page hibernation, containers under memory
  pressure) with `CONFIG_DEBUG_LOCK_ALLOC` and `CONFIG_SLUB_DEBUG` until the 7.x MM
  tree stabilizes.
- Enable `vm.oom_dump_tasks=1` and monitor `dmesg` for `shrink_slab` recursion warnings.
- Pin memory policy with `numactl --cpunodebind` / `--membind` on NUMA hosts to reduce
  surprises from autonuma changes.

## Exercises / thought problems
1. Audit your kernel config: which MM config options affect your production workload?
   Map each option (`CONFIG_TRANSPARENT_HUGEPAGE`, `CONFIG_COMPACTION`, `CONFIG_CMA`,
   `CONFIG_SLUB_DEBUG`) to a failure mode if the option were disabled or enabled.
2. Simulate alloc-in-reclaim deadlock: write a kernel module that calls `kmalloc(GFP_KERNEL)`
   from a shrinker callback. Observe `dmesg` warnings. What does this tell you about
   PF_MEMALLOC semantics?
3. Profile `mm/vmscan.c` via `bpftrace` during a memory-pressure event: map
   `shrink_node` and `shrink_slab` latencies to which shrinker callbacks are most
   expensive.
4. Hypothesis: if the new MM maintainer prefers a conservative code review posture,
   which currently in-flight features (THP madvise, cgroup v3 mm pressure, DAMON
   improvement) are most at risk of delay?
