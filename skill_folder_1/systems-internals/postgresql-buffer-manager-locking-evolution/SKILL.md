---
name: postgresql-buffer-manager-locking-evolution
description: Treat PostgreSQL buffer manager as a teaching case study in concurrency refinement. Covers BufMgrLock split into BufMappingLock/BufFreelistLock/buf_hdr_lock in 8.1, clock-split + partitioned hash in 8.2, and the 9.5 atomic handoff that replaced BufFreelistLock with short-held buffer_strategy_lock and atomic nextVictimBuffer. Aims below 'how to use' to explain why each split was forced by a specific bottleneck and how atomic refcount/descriptor fields eliminated per-buffer locks.
---

# PostgreSQL Buffer Manager Locking Evolution

Use this skill when teaching lock refinement in database systems or systems courses. Focus: why the buffer manager moved from one lock to many, then from many locks to atomics, and what the residual contention looks like today.

## The Single-Lock World (Pre-6.5)

- One `BufMgrLock` guards:
  - buffer lookup hash table
  - freelist / clock hand
  - per-buffer descriptor metadata
- Every `ReadBuffer`/`ReleaseBuffer` path reseizes that one lock.
- Under DIO utilization this becomes the throughput ceiling regardless of CPU count.

## 6.5 Split: Two (then Three) Locks

- Added per-buffer `cntx_lock` (shared/exclusive) for pin/unpin.
- `BufMgrLock` renamed `BufMappingLock` and now only guards hash table.
- Internal clock-sweep victim selection introduced but with global `nextVictimBuffer`.
- Result: concurrent read pinning improves; still serialize on freelist.

## 8.1 Breakup: Domain Decomposition

PostgreSQL 8.1 introduced three principal locks:

| Lock | Guards | Scope |
|---|---|---|
| `BufMappingLock` | buffer hash buckets | Shared (reads), Exclusive (insert/delete) |
| `BufFreelistLock` | freelist head/tail + clock hand | Exclusive only |
| `buf_hdr_lock` | per-buffer descriptor (usageCount, flags) | Per-slot |

- Hash table partitioned into 2048+ buckets; hash bucket lock is the unit of mapping contention.
- Victim selection still walks a singly linked list protected by `BufFreelistLock`; relevant because this is where pin-count check happens (`refcount == 0`).

## 8.2 Hash Partitioning

- Hash table became a power-of-two bucket array of `BufferDescPivot` entries.
- Each bucket has its own lock; collisions only serialize within a tag bucket.
- Freelist and clock hand remain on `BufFreelistLock`; victim scan still O(N) worst case.

## 9.5 Clock Atomic Handoff

This is the mechanistic turning point for high-core-count systems.

### What changed

- Introduced `buffer_strategy_lock` (short-held), replacing long-held `BufFreelistLock`.
- `nextVictimBuffer` became an atomic field with `pg_atomic_compare_exchange_u32` loop.
- Descriptor fields (`refCount`, `usageCount`, `flags`) became `pg_atomic_uint32` with `pg_write_barrier()` semantics.
- Clock hand no longer holds any lock across the costliest operation: `pg_atomic_fetch_sub_u32(&refcount, 1)` + per-buffer direct compare.

### Why this won

- I/O wait time dominates actual freelist traversal: freed buffers are almost always just a few steps ahead.
- Per-core `NextVictimBuffer` reads plus CAS advancement removes any global serializer.
- Pin/unpin no longer take a lock: refcount is manipulated atomically without `buf_hdr_lock`.

## 9.6 Full Descriptor Atomicity

9.6 converted the remaining descriptor metadata and deprecated `buf_hdr_lock`. Only `buffer_strategy_lock` survives, for `StrategyGetBuffer()` control flow; it is almost never the bottleneck because early-outs (refcount > 0) avoid slow paths.

## Residual Contention After 9.6

The measurable bottleneck post-9.6 is pinned-buffer partitioning during hash-table collisions, not descriptor field synchronization:

- What still takes a shared `BufMappingLock`:
  - `LockBufferForRead` via `LockShared`
- What still takes an exclusive `BufMappingLock`:
  - `LockBufferForCleanup`
  - `LockBufferForXLog` during WAL write

## Mechanistic Takeaways

1. **Lock refinement pattern**: start single-lock, then split by domain (mapping vs descriptor vs strategy), then refine the hottest domain further (atomics when low-contention read dominates and write is simple structured).
2. **Pinning is the natural atomic target**: buffer lifetime is governed by a single integer; the natural reflection of "another backend has this pinned" is a counter, not a lock.
3. **Victim selection is I/O amortized**: CLOCK is tolerant of slightly stale next victim values; slack lets the atomic handoff approach scale without fairness.
4. **The pattern regrettably underused**: Most students learn lock granularity refinement perfectly symbolically; postgres translates each pattern in production over 25+ years.

## Exercises / Research Prompts

1. **Mechanistic:** Draw the state machine for `StrategyGetBuffer()`. Under what conditions does it fall through to `WaitIO` and release `buffer_strategy_lock` early?
2. **Correctness audit:** Reconstruct the `BufFreelistLock` ABA race that atomics fixed. Is there still a case where `nextVictimBuffer` can loop infinitely?
3. **Comparison project:** Map PostgreSQL's `BufMappingLock` modernization onto Linux's SLAB/SLUB lock-free freelist (Kreitzer / Glauber).
4. **Performance profiling plan:** How would you measure whether `buffer_strategy_lock` is now the bottleneck under high-concurrency DIO workloads?