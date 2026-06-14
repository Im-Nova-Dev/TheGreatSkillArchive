---
name: filesystem-buffer-manager-btrfs-ext4-folio
description: >
  Mechanistic internals of Linux filesystem buffer management: Btrfs extent-buffer
  xarray conversion in 6.16 and Ext4 large folio support. Covers radix tree vs xarray
  concurrency, extent buffer lifetimes, folio I/O chains, dirty accounting implications,
  and how these changes interact with page cache and writeback.
trigger: >
  Btrfs metadata writeback, Ext4 large folio, filesystem performance internals,
  extent buffer locking, xarray vs radix tree, multi-page folio page cache, writeback
  amplification, filesystem buffer manager tricks, Linux 6.16 storage changes.
---

# Filesystem Buffer Manager Internals: Btrfs xarray & Ext4 Large Folios

## Scope
Mechanistic how-it-works of two intersecting Linux filesystem changes:
1) Btrfs switching extent buffers from radix-tree to xarray for metadata operations
   in Linux 6.16.
2) Ext4 large folio support for regular files in Linux 6.16.
Both target the same pressure point: metadata/data buffer trees and page cache
writeback paths.

## Prerequisites
- Page cache: `struct page`, `address_space`, `find_get_page()` / `add_to_page_cache_lru()`.
- Buffer heads vs folios: `buffer_head` and `folio` lifecycle.
- XArray basics: `xa_lock`, `xa_mark`, `XA_FREE_MARK`, `XA_STATE`.
- Btrfs extent buffer: representation of on-disk metadata tree blocks.
- Writeback: `writeback_control`, `mpage_writepage()`, btree `wb_writeback` threads.

## Lesson 1: Radix tree vs xarray on a hot metadata path
### Why the change matters
Btrfs metadata heavy operations insert/lookup/extent-io-tree operations on
radix-trees indexed by bytenr (or page index). With increasing capacity disks
and large numbers of small metadata blocks, traversal becomes latency-bound.

### xarray mechanics
- XArray stores "entries" in an array-of-pointers trie; leaf slots hold `NULL`,
  a tagged entry, or a value pointer.
- Btrfs uses it by storing `struct extent_buffer *` as the stored value; tags
  like `XB_INSERT` and `XB_REMOVE` are used for iterating subsets.
- Unlike radix trees, xarray explicitly separates *index* range from *entry*
  identity, making prefetch and cache locality better for contiguous metadata
  regions.

### Locking difference
- Radix-tree code: `radix_tree_lock()` plus `slot` pointer trickery; often held
  across walk without page ref acquisition.
- XArray: `xa_lock` typically must be held across entry updates. Btrfs accounts
  this by doing *locked* replacement of an extent buffer pointer -> dropping the
  old buffer reference inside the lock, which serializes with other walkers.

### Invariant for correctness
> Any doer holding `extent_buffer *` to a live metadata block must verify the
> page is still in the xarray at that bytenr before trusting it; concurrent
> relocation can evict and free the buffer between lookup and access.
Btrfs code uses `extent_buffer_get()` after xarray lookup, and refcount mechanics
to prevent dangling. 6.16's change is about throughput, not safety.

## Lesson 2: Extent IO tree cleanups
Btrfs keeps per-fs `extent_io_tree` (dirty / pinned / locked / written ranges)
keyed by byte address. Before 6.16 there were redundant walks for the same range.

The cleanup maps roughly to:
- Consolidating `set_extent_dirty()` family into one helper that correctly
  increments `dirty_pages` and marks the xarray dirty tag.
- Removing double-unpin during transaction commit when an extent was both
  in the `ordered_extent` queue and the IO tree; unpin now happens once.

Result: transaction commit path spends less time walking metadata range trees
and page MRU candidates. The 3-5% estimated runtime improvement comes mostly
from fewer `rwlock_t` acquisitions during commit, not from algorithmic change.

## Lesson 3: Ext4 large folio support
### What changed
Prior to 6.16, Ext4's buffered write path always used base-order (4 KiB on x86)
folios (i.e., `folio` == `page`). `writepage()` was called per 4 KiB page.

6.16 enables large folio support so `mpage_writepages()` can hand the block
layer folios of 128 KiB or 512 KiB size.

### Why this matters mechanistically
- Per-folio overhead: metadata updates, journal reservation, extent tree search,
  unlock/lock of `i_data_sem`, and elevator insertion all happen per folio.
  Large folios amortize that.
- Delayed allocation: instead of `4 KiB` block reservations, `delalloc` reserves
  are sized to folio granularity - this avoids splitting reservations until final
  block allocation.
- Journal replay: ext4 fast-commit and JBD2 code must now handle blocks that span
  multiple 4 KiB physical blocks without crossing into unrelated folios; 6.16
  adds checks that `block << block_size_bits` does not cross the folio boundary.

### Atomic write support
6.16 adds multi-fsblock atomic writes for `bigalloc` file systems. Kernel does:
1. Reserve `n` blocks contiguously where n = fs blocks per atomic unit.
2. Flush + journal the delta in one commit.
3. On crash, either all blocks appear or none (zero hole).
The downside is that if ENOSPC interrupts reservation, the entire contiguous
unit aborts, so fragmentation sensitivity increases.

## Lesson 4: Cross-cutting buffer coherence with io_uring ZCRX
A less obvious interaction: with io_uring DMA-BUF ZCRX contiguous with filesystem
I/O on the same pages is increasingly common. If a ZCRX buffer is later passed
to a filesystem write path:
- The page is now owned by the *socket receive* and *page cache* concurrently;
  any direct I/O or mmap IO path that calls `get_user_pages_fast()` must account
  for DMA-BUF attachments.
- Btrfs's xarray locking must serialize with those get_user_pages callers that
  might be waiting on `pgmap->page_fence` (device-private page migration).

## Lesson 5: Performance interpretation
| Workload | Linux 6.15 | Linux 6.16 | Cause |
|----------|------------|------------|-------|
| Btrfs metadata writeback | baseline | +33-50% throughput | extent buffer xarray |
| Ext4 large sequential writes | baseline | +37% | large folios |
| DB random IO on ext4 | baseline | +60-100% claimed by maintainers | atomic multiblock writes reducing double-write |
| Transaction commit throughput Btrfs | baseline | +3-5% | extent IO tree cleanup |

These are not "magic"; they reflect reduced locking and fewer cache-line
bounces. They also require workloads to be large enough to amortize the larger
folios. Random small IO can regress slightly due to extra `bio_vec` segments in
`readahead()`.

## Lesson 6: How to observe these behaviors
### Tracepoints on Btrfs metadata writeback
```
tracepoints:btrfs:btrfs_extent_buffer_locks
tracepoints:btrfs:btrfs_extent_buffer_writepage
```
Correlate `btrfs_extent_buffer_writepage` events with lock hold time.

### Ext4 large folio breakdownpoint
```
echo 1 > /sys/kernel/debug/tracing/events/ext4/enable
```
and watch `ext4_da_write_begin` / `ext4_da_write_end` for folio `index`
differences before/after enablement.

### Perf counters
```
perf stat -e kmem:xarray_load,kmem:xarray_store ...
```
often shows elevated xarray activity on metadata-heavy Btrfs workloads.

## Exercises / thought problems
1. Design an xarray walk to iterate all live metadata extent buffers for a Btrfs
   tree root. Where must `extent_buffer_get()` happen relative to `xa_lock`
   release? What can go wrong if the buffer is freed between iterator creation
   and access?
2. Ext4 large folios on `bigalloc` with 1 MiB clusters serialize differently than
   `4 KiB` `blocksize`. Show the IO plan for writing a 300 KiB file with
   `bigalloc`=1 MiB, `fs blocksize`=4 KiB, atomic writes disabled, versus
   atomic writes enabled.
3. Why does concurrent io_uring ZCRX on a DMA-BUF `mmap`'d into a database
   process break the assumption that a page's `mapping` field stays stable, and
   what filesystem handlers must now be NUMA/cpu-access aware?
4. Trace Btrfs transaction commit and compute how `set_extent_dirty()` was called
   twice for the same range pre-6.16 and why that produced two separate
   `__mark_inode_dirty()` calls instead of one.
5. After enabling Ext4 large folios, show how `mpage_writepages()` must build
   bio_vec chains differently from single-page folios, and why bio splitting in
   `submit_bio()` must respect folio alignment.

## Source references
- Phoronix Btrfs 6.16: https://www.phoronix.com/news/Linux-6.16-Btrfs-Performance
- KernelNewbies 6.16: https://kernelnewbies.org/Linux_6.16
- Phoronix Ext4 6.16: https://www.phoronix.com/news/Linux-6.16-EXT4-Performance
- LWN atomic writes: https://lwn.net/Articles/1016406/
- Btrfs XArray conversion lore: subset of David Sterba pull-request tree in 6.16
  (full list in btrfs pull-request commit log, see btrfs maintainer tree)
