---
name: operating-systems
description: Teach operating systems including processes, threads, scheduling, memory management, virtual memory, file systems, concurrency, synchronization, I/O, system calls, interrupts, and practical OS design principles with teaching exercises.
---

# Operating Systems

## Core topics

1. Processes and threads
   - Lifecycle and states
   - CPU scheduling concept

2. Memory and storage
   - Paging and virtual memory
   - File systems

3. Concurrency and IO
   - Synchronization primitives
   - Blocking and nonblocking IO

## Teaching approach
- Compare process versus thread.
- Explain one paging concept.
- Model one synchronization problem.

## Mechanistic deep-dives: scheduler and preemption
- Linux preemption modes: `PREEMPT_NONE`, full preemption, and the 7.0 default `PREEMPT_LAZY`; understand what “lazy” does at the architectural level: when preemption is checked, how preempt_count interacts with need reschedule, and why reducing preempts trades throughput vs latency.
- Lazy preemption effects on user-space spinlocks: if a fast critical section is only safe with THPs, then latency policy choice becomes dependent on memory subsystem tuning, not just scheduler config.
- EEVDF vs CFS: slice accounting, latency nice, and how EEVDF permits tighter slice control with lazy preemption.
- PREEMPT_RT vs PREEMPT_LAZY: preempt-RT inverts some assumptions with threaded IRQs and forced preemption; lazy preemption is a middle ground for server kernels but can surprise hard-RT workloads.

## Memory subsystem interactions
- How THP choice changes preemption exposure for spinlock holders: TLB flush cost, hugepage collapse overhead, and NUMA balancing behavior alter the realistic critical-section length.
- mmap/SHM pinned-region behavior under lazy preemption: monitor page-fault frequency inside test workloads to detect when a scheduler change suddenly exposes memory pressure.

## VFS-to-MM reclaim deadlock: PF_MEMALLOC + GFP_NOFAIL (Kernel Recipes 2025)
### Background: direct reclaim and emergency reserves
- `__perform_reclaim()` sets `PF_MEMALLOC` so a task can dip into atomic reserves (`min_free_kbytes`-gated pages that few other contexts may use).
- Reserve pages exist to prevent full recursion: if the allocator ran out and reclaim also needed pages, it would deadlock.

### The new anti-pattern: allocate-to-free loop
- During slab/inode shrinker scan, `super_cache_scan()` calls `prune_icache_sb()` -> `evict()` -> `evict_inode()`.
- Filesystems such as FAT/ext4 may need to read on-disk metadata in `evict_inode()` (e.g. FAT table, extent tree blocks, journal revoke records).
- `sb_bread()` path uses `GFP_NOFAIL`. `GFP_NOFAIL` can recurse into reclaim even inside `PF_MEMALLOC` context for buffer pages that are not in the atomic reserves.
- Sequence: reclaim requests eviction -> eviction calls `sb_bread()` -> `sb_bread()` calls `__alloc_pages_slowpath()` -> might_alloc() triggers reclaim again -> recursion.
- This is distinct from the classic filesystem-lock-then-kmalloc deadlock handled by `memalloc_nofs_*`. The new pattern bypasses that guard because it is behind `PF_MEMALLOC`.

### Why the old guard fails
- `memalloc_nofs_save()` blocks filesystem allocation during reclaim when filesystem code is aware it is in reclaim context.
- `PF_MEMALLOC` tasks are allowed to allocate from reserves, but reserve pages are for atomic allocations; complex filesystem reads may still need order-0 caches not covered by reserves.
- The VFS shrinker path is implicit: filesystems did not know they were being called under direct reclaim.

### Filesystem-specific behavior
- FAT: `fat_truncate_blocks()`/`fat_free_eofblocks()` call `sb_bread()` for FAT blocks inside `evict`.
- ext4: extent tree reading, journal revoke maps, and block bitmap reads can recurse.
- XFS: inactive-to-evict flow does not rely on `sb_bread()` the same way, so it avoids the recursion.

### Candidate mitigations
1. Expand atomic reserve scope for `PF_MEMALLOC` tasks on large-block devices.
2. Pre-pin/reserve buffer heads around inode eviction; mempools (hard because size varies).
3. Restrict inode reclaim to kswapd only; insufficient—one bug originated in kswapd.
4. Allow `evict_inode()` to fail; risks stalls in other subsystems waiting for inode.
5. Skip dirty inode eviction in `PF_MEMALLOC` context to break recursion; leaves dirty state unflushed.

### Mechanistic analysis exercise
- Read `mm/vmscan.c` (`__perform_reclaim`, `try_to_free_pages`) and `fs/inode.c` (`evict_inode`, `prune_icache_sb`).
- Identify where `PF_MEMALLOC` is set and how the allocator tests it.
- Identify where `GFP_NOFAIL` hides recursion into reclaim; trace `alloc_pages_mayant_alloc()`.
- Design a VFS-layer API to make shrinker-initiated eviction safe under direct reclaim.

## IO_uring and preemption
- Completion latency under lazy preemption: io_uring completion polling is sensitive to preempt delay; benchmark poll loops with `IORING_SETUP_SQPOLL` under mixed CPU loads to see regressions or wins.
- IO_uring + BPF struct_ops (Merged Linux 7.1, March 2026): `IORING_OP_BPF` / `bpf_io_uring_submit_sqes()` allows BPF programs to replace `io_uring_enter()` event loops, with kfuncs for registered buffer pools and completion queue manipulation. Mechanism: BPF program runs in-place of default event loop, returns `IOU_LOOP_CONTINUE`/`IOU_LOOP_STOP`. Use cases: deprecating specific `io_uring` APIs by emulating in BPF, smarter polling loops, removing syscall overhead for always-running async workloads. Tradeoff: BPF debugging is harder than equivalent user-space code; risk of moving app logic into kernel.

## Teaching exercises
- Trace `need_resched` propagation in a kernel build with `ftrace` `sched_switch` and compare preemption frequencies across legacy, voluntary, and weak preemption kernels.
- Benchmark PostgreSQL or a spinlock-heavy userspace workload with and without THPs on two kernel preemption configs; chart how touch frequency and lock hold time shift the regression threshold.
- Design a time-slice extension protocol for a userspace critical section; test whether it masks the regression without requiring app changes, and identify why PostgreSQL maintainers rejected this fix.
- Memory reclaim tracing: create an `autofs` or `FUSE` filesystem that intentionally calls `sb_bread()` inside eviction; use `kmemleak` and `tracepoints` in `mm/page_alloc.c` and `fs/inode.c` to detect the recursive reclaim path. Measure with `perf trace -e kmem:mm_page_alloc,kmem:mm_page_free` and correlate with `warnings` in `dmesg`.
