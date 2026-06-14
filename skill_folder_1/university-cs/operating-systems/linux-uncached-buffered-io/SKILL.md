
---
name: linux-uncached-buffered-io
description: Teach the Linux 6.14 `RWF_UNCACHED` uncached buffered I/O mechanism from the substrate up: page cache drop path, folio lifecycle, block-layer interaction, cgroup/NUMA effects, io_uring usage, and when it wins or regresses.
---

# Linux Uncached Buffered I/O (`RWF_UNCACHED`) — Mechanistic Internals

Use this skill when explaining, auditing, or teaching the kernel code paths surrounding Linux 6.14’s uncached buffered I/O. This is not a “how to use the flag” summary; it is a substrate-native breakdown for students or operators working below VFS.

## Prerequisites

- Linux page cache basics: `address_space`, radix-tree / xarray, `folio`, LRU inactive/active lists.
- `vfs_read()` / `vfs_write()` and `generic_file_*` helpers.
- `bio` / `request_queue` and writeback fundamentals.
- Linux 6.14 mainline baseline.

## What `RWF_UNCACHED` does

A per-I/O flag on `read()` / `write()` (and `io_uring` `IORING_OP_READV` / `IORING_OP_WRITEV` `rw_flag`) that says: still use the buffered-I/O path (caching, readahead, filesystem journaling), but free the resulting pages back to the per-CPU `pcp` freelist on completion instead of inserting them into the LRU inactive/active lists.

This is the “middle path”: cheaper than `O_DIRECT` for alignment and filesystem invariants, but avoids the DRAM-fill thrash problem caused by large sequential scans.

## Code path

1. Entry in `fs/read_write.c` or `io_uring` sets `rw->flags & RWF_UNCACHED`.
2. Normal `generic_file_buffered_read()` / `generic_file_write_iter()` path proceeds.
3. Cache-hit fast path still works. New pages populate the `address_space->page_tree`.
4. On I/O completion, the kernel selects a drop target: LRU insert vs pcp free.
5. Reads: `filemap_release_folio()` drops the folio to pcp.
6. Writes: after writeback (`wb` completion), the dirty folio is freed to pcp, bypassing inactive LRU.

## Interaction rules

- `O_DIRECT` semantics are unchanged; `RWF_UNCACHED` does not apply when the file is opened with `O_DIRECT`.
- `mmap()` on a file opened with `RWF_UNCACHED` behaves like ordinary mapped memory; the flag only affects explicit `read()`/`write()` calls.
- Ext4, XFS, Btrfs ship this enabled by default in 6.14; direct-IO-only or special pseudo-filesystems ignore the flag.
- Cgroup v2 `memory.high` / OOM pressure sees different charge dynamics because pages move through the pcp freelist instead of the LRU.
- NUMA: pcp-freed folios migrate across NUMA nodes less aggressively than LRU-inserted pages; high NUMA machines should pair `RWF_UNCACHED` with `madvise(MADV_RANDOM)` or `mbind()` if locality matters.

## io_uring usage

Set `rw->rw_flags` to `RWF_UNCACHED` in the `io_uring` sqe. Use with registered buffers + fixed files to remove per-op `pin_user_pages()` overhead and keep the kernel’s DMA mapping hot.

## When it wins and when it regresses

- Wins: sustained sequential throughput on fast NVMe when the working set exceeds DRAM as page cache. Typical improvement quoted in benchmarks: 65–75%.
- Neutral: workloads small enough to fit the cache.
- Regresses: random read workloads where cache-hit reuse is the dominant benefit.

## Diagnostic checklist

1. Observe `buff/cache` and `free` in `free -h` before/after a large copy. If `buff/cache` grows and stays up, the workload is a candidate.
2. Run `perf stat` on the workload with and without the flag; watch `page-faults` minor and `context-switches`.
3. Check `kswapd` CPU time: high values during steady-state copying are a strong signal.

## Recommended reading

- LWN: The return of `RWF_UNCACHED` — `https://lwn.net/Articles/998783/`
- Phoronix performance results — `https://www.phoronix.com/news/Uncached-Buffered-IO-Linux-6.14`
- Kernelnewbies Linux 6.14 summary — `https://kernelnewbies.org/Linux_6.14`
