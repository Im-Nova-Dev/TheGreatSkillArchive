---
name: vfs-memory-reclaim-deadlock
description: Teach the Linux VFS-to-MM reclaim deadlock involving PF_MEMALLOC + GFP_NOFAIL in filesystem eviction paths. Mechanistic how-it-works coverage with code path tracing, allocation flag semantics, mitigation design, and kernel debugging exercises.
---

# Linux VFS-to-MM Reclaim Deadlock: PF_MEMALLOC + GFP_NOFAIL

## Core topic
A new anti-pattern where memory reclaim recurses into itself because filesystem inode eviction performs allocations with `GFP_NOFAIL` while the allocator is already in direct reclaim under `PF_MEMALLOC`.

## Mechanistic how-it-works
### 1. Direct reclaim entry
- `__alloc_pages_slowpath()` with insufficient free pages calls `__perform_reclaim()`.
- `__perform_reclaim()` sets `PF_MEMALLOC` on the current task.
- `PF_MEMALLOC` allows access to emergency atomic reserves (`__GFP_MEMALLOC`), but does not grant unlimited allocations of all GFP masks.

### 2. Shrinker-driven eviction
- The slab shrinker (`shrink_slab()`) invokes filesystem superblock shrinkers such as `super_cache_scan()`.
- `super_cache_scan()` calls `prune_icache_sb()` -> `evict()` -> `evict_inode()` -> filesystem-specific hooks.

### 3. Filesystem buffer reads in eviction
- FAT: `fat_truncate_blocks()` -> `fat_free_eofblocks()` -> `fat_ent_bread()` -> `sb_bread()` to read the FAT table.
- ext4: freeing extent tree nodes, journal revoke records, or block bitmaps may call `sb_getblk()`/`sb_bread()`.
- `sb_bread()` ultimately calls `__getblk_gfp()`/`__bread_gfp()` with `GFP_NOFAIL`.

### 4. GFP_NOFAIL under PF_MEMALLOC
- `GFP_NOFAIL` forces the allocator to retry indefinitely. When evaluated in this context, it can recurse into `__alloc_pages_slowpath()` -> `__perform_reclaim()` again.
- The recursion is not caught by `memalloc_nofs_*`, because those guards are saved in generic allocator entry points by normal filesystem code, not by the implicit shrinker path, and `PF_MEMALLOC` gives additional permissions that bypass those restrictions for reserve-granted allocations.

### 5. Consequences
- Reclaim recursion can exhaust emergency reserves, stall the allocator, or deadlock if multiple tasks recurse.
- Symptoms: kernel warnings at `__alloc_pages_slowpath`, stalls in `dmesg` or hung task detectors, saturation under page-cache pressure.

## Filesystem-specific behavior
### FAT / exFAT
- `evict_inode()` calls block-read helpers for metadata tables inside reclaim.
- Deadlock risk is high because FAT block reads happen unconditionally.

### ext4
- Journal transaction abort/revoke cleanup during `evict_inode()`.
- Extent-tree block reads and group descriptor reads.
- Has `memalloc_nofs_*` usage, but not consistently across all eviction subpaths.

### XFS
- Uses an inactive state that defers reference dropping to a workqueue, reducing in-memory structure access under shrinker locks.
- Generally avoids metadata reads under reclaim because dirty extents are flushed before the inode is reclaimable.

## Allocation flag semantics
| Flag | Role in this deadlock |
|---|---|
| `PF_MEMALLOC` | Set during direct reclaim; claims access to atomic reserves for allocation with `__GFP_MEMALLOC`. Does not prevent recursion. |
| `GFP_NOFAIL` | Retry-until-success. Hides recursive reclaim because `might_alloc()` can trigger reclaim again. |
| `GFP_KERNEL` / `GFP_NOFS` | Subject to reclaim restrictions; not allowed in atomic contexts. |
| `GFP_ATOMIC` | Allowed under `PF_MEMALLOC` reserves; for low-order allocations during interrupts or softirqs. |
| `__GFP_MEMALLOC` | Grants access to reserves, bypassing watermarks. Used internally when `PF_MEMALLOC` is set. |

## Candidate mitigations
1. Reserve expansion for `PF_MEMALLOC` tasks on large-block devices that need high-order folios.
2. Pre-allocate or mempool critical metadata for filesystem shrinkers. Limitation: hard to predict exact size at shrink time.
3. Restrict inode reclaim to kswapd only. Limitation: one bug originated in kswapd; kswapd is already reclaim, and the task there does not have normal `PF_MEMALLOC`.
4. Allow `evict_inode()` failure and wait with timeout. Risk: other subsystems may wait on evicted inodes.
5. Skip dirty inode eviction in `PF_MEMALLOC` context. Risk: dirty state is left unflushed.
6. Introduce VFS WQ-based deferred metadata reads in reclaim.

## Kernel debugging workflow
### Tracepoints and counters
- `perf trace -e kmem:mm_page_alloc,kmem:mm_page_free`
- `tracepoints in mm/vmscan.c`: `mm_vmscan_direct_reclaim_begin/end`
- `tracepoints in fs/inode.c`: `inode_evict`
- `dmesg` warnings from `__alloc_pages_slowpath()` / `alloc_pages_may_oem_alloc()`.

### Reproduction sketch
- Create a FUSE or autofs filesystem whose `evict` path reads from its backing store (e.g. a network mount or another filesystem).
- Scatter small files to fill page cache, then unmount or delete files to force eviction.
- Monitor with `vmstat -wm` and `slabtop` for shrinker activity under memory pressure via `echo 3 > /proc/sys/vm/drop_caches` or by running `stress`.

## Design challenge
Design a VFS API that lets shrinkers mark specific inodes or buffer heads as "safe to skip under `PF_MEMALLOC`, retry later". Evaluate the impact on memory-pressure latency.

## Historic parallel: classic deadlock
Before `memalloc_nofs_*`, a similar recursion occurred when filesystems held locks during reclaim and allocators recursed. The solution was adding `PF_MEMALLOC`-aware allocation contexts. This new deadlock shows that adding the first guard exposed an implicit recursion vector that was previously inaccessible.
