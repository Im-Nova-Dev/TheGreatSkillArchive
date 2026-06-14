# Kernel MM Maintainer Transition & Linux 7.x Notes

## Core Context
- **Date:** April 21, 2026
- **Event:** Andrew Morton stepped down as Linux kernel memory management (mm) maintainer after 26 years.
- **Subsystem breadth:** `mm/` spans 164 interlinked source files and touches every other kernel subsystem, so mm regressions rarely stay local.
- **Security note:** 17.9% of Linux kernel security vulnerabilities reported between 2020 and 2024 originated in the mm codebase.

## Immediate Implications (May 2026)
1. **Review throughput slowdown** – complex MM and MM/fs crossover changes will likely move slower.
2. **Conservative merge posture** – expected preference for conservative patches in the 7.1/7.2 merge windows, especially for alloc-in-reclaim and shrinker recursion paths.
3. **Co-maintainer pressure** – mm/vmscan, slab, compaction, and autonuma maintainers will absorb more of the review load.

## Regression Watch-Points for 7.x
- **Large-block allocation performance:** StorageNewsletter noted large-block alloc time dropped from 3.6s to 0.43s in 7.0; verify this does not increase fragmentation under THP-heavy workloads.
- **alloc-in-reclaim deadlocks:** filesystems/drivers calling `kmalloc(GFP_KERNEL)` from shrinkers or reclaim paths can re-enter the allocator (PF_FSTRANS recursion).
- **Page pool / network Rx coupling:** `net/core/page_pool.c` calls `alloc_pages()` under NAPI softirq; any change to mm page recycling directly affects AF_XDP and io_uring ZCRX paths.
- **Shrinker recursion:** btrfs/XFS shrinkers and VFS `shrink_slab()` callbacks are a historical source of cross-subsystem regressions.

## Production Recommendations
- Enable `CONFIG_DEBUG_LOCK_ALLOC=y` and `CONFIG_SLUB_DEBUG=y` during initial 7.x soak testing.
- Pin memory policy on NUMA hosts (`numactl --cpunodebind/--membind`) to reduce surprises from autonuma.
- Monitor dmesg for `shrink_slab` recursion warnings and `SLUB` corruption reports.
