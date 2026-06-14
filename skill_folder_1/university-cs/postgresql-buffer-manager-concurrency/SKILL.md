---
name: postgresql-buffer-manager-concurrency
title: PostgreSQL Buffer Manager Lock-Free Concurrency and Eviction Internals
description: Mechanistic how-it-works coverage of PostgreSQL's buffer manager concurrency evolution from monolithic locks to fully atomic descriptor fields, clock-sweep victim selection, page pinning semantics, and the remaining freelist scheduling bottleneck.
triggers:
  - database internals
  - systems internals
  - buffer manager
  - concurrency
  - eviction algorithms
  - PostgreSQL
  - latch-free scalars
  - lock-free data structures
languages:
  - C
  - SQL
difficulty: advanced
estimated_time: 30 minutes
tags:
  - systems
  - databases
  - concurrency
  - memory management
  - kernel-user-space
---

# PostgreSQL Buffer Manager Concurrency and Eviction Internals

## Objectives
1. Trace the evolution from `bufmgrLock` to atomics in PostgreSQL's buffer manager.
2. Explain the mathematical basis of the clock-sweep algorithm and its `usageCount` decay.
3. Differentiate pinning (refcount) from access synchronization (`cntx_lock` then atomics).
4. Identify the remaining bottleneck and why it is not a practical scaling limit.

## Audience
- Database systems students and developers.
- Kernel and storage engineers interested in user-space concurrency mechanisms.
- Performance analysts troubleshooting PostgreSQL buffer pool contention.

## Prerequisites
- Familiarity with POSIX threads, spinlocks, and atomics (gcc `__atomic` builtins or C11 `<stdatomic.h>`).
- Awareness of PostgreSQL shared memory segments and postmaster forking model.
- Basic knowledge of database page replacement algorithms (LRU, clock).

---

# Module 1: Data Structures and Shared Memory Layout

PostgreSQL runs a shared buffer pool in a single System V SHM segment. The pool size is fixed at startup.

Key structures (simplified):
- `BufferTag`: identifies a page on disk (`forkNum`, `rnode`, `blockNum`).
- `BufferDescriptor`: per-buffer metadata array (1:1 mapping to physical buffers).
- `buf_table`: hash table mapping `BufferTag` -> `BufferDesc` slot id (`buf_id`).

```c
typedef struct BufferTag {
    ForkNumber  forkNum;
    RelFileNode rnode;
    BlockNumber blockNum;
} BufferTag;

typedef struct BufferDesc {
    BufferTag  tag;
    int         buf_id;
    slock_t     buf_hdr_lock;     /* OBSOLETE since 9.6; kept for illustration */
    int         refcount;
    int         usageCount;
    int         flags;
} BufferDesc;
```

The descriptor array is the primary shared data structure. It lives in shared memory so postmaster and all child backends can access it without a system call.

## Module 2: Pinning vs. Locking - Semantic Separation

PostgreSQL maintains two orthogonal concerns for each buffer:

| Concern | Mechanism | Purpose |
|---------|-----------|---------|
| Eviction prevention | refcount (pin) | A pinned buffer is never a victim of the clock hand. |
| Access coordination | cntx_lock (legacy) / atomics (modern) | Serializes reads and writes to the same page. |

Understanding the difference is critical:
- A backend may pin a buffer multiple times for read-only operations.
- Multiple backends can hold shared (read) access concurrently via atomics on the descriptor state.
- Only exclusive writers need exclusive semantics.

## Module 3: Clock-Sweep Victim Selection

PostgreSQL does *not* use LRU. It uses a **clock-sweep algorithm**, a practical approximation with O(1) amortized operation.

```c
/* Pseudocode for a single clock hand tick */
static inline int
BufferClockSweepStep(void)
{
    int buf_id = nextVictimBuffer;      /* atomic, no lock needed since 9.5 */
    BufferDesc *buf = &BufferDescriptors[buf_id];

    if (BufferIsPinned(buf)) {
        /* Skip pinned buffers, advance to next in the circular pool */
    } else if (buf->usageCount > 0) {
        /* Decay: this access is not "recent enough" to protect the page */
        buf->usageCount--;
    } else {
        /* This page has not been accessed recently: candidate for eviction */
        return buf_id;
    }

    nextVictimBuffer = (buf_id + 1) % NBuffers;
    return -1;
}
```

Mechanistic insight: The "hand" never moves backward in the buffer array. A buffer's resistance to eviction is a discrete counter that decays only when the clock hand passes over it while the page is unpinned. This means high-frequency scans disrupt hot index pages unless `usageCount` is higher than 1.

## Module 4: The Locking Evolution - Mechanistic Detail

### Stage 1: Monolithic `bufmgrLock`
All operations required acquiring one lock. Throughput limited by Amdahl's law: every page lookup, hash table insertion, and victim selection serialized through a single spinlock.

### Stage 2: `cntx_lock` (Postgres 6.5)
Introduced per-buffer read/write locks. Cooperative pin-then-lock protocol:
1. Pin buffer (increment refcount).
2. Acquire `cntx_lock` (shared for read, exclusive for write).
3. Use the page.
4. Release lock.
5. Unpin.

Remaining bottleneck: `bufmgrLock` still protected hash table lookups, victim selection, and freelist management.

### Stage 3: Three Lock Decomposition (Postgres 8.1)
`bufmgrLock` split into:
- `BufMappingLock`: protects hash table bucket array and `tag` swap.
- `BufFreelistLock`: protects `nextVictimBuffer` and the free list.
- `buf_hdr_lock`: per-buffer header lock protecting flags, refcount, usageCount.

Improvement: Page lookup and header manipulation decoupled. But `BufFreelistLock` and `BufMappingLock` became new serialization points.

### Stage 4: Partitioned Hash Table (Postgres 8.2)
Fixed-size hash table split into N buckets, each with its own bufhash lock. Requires hash function to stay stable (no dynamic rehashing). Lookup contention reduced roughly by factor of N.

### Stage 5: Atomic Next Victim + CAS Refcount (Postgres 9.5)
CAS (compare-and-swap) operations added to PostgreSQL via a complex cross-platform abstraction (GCC builtins, MSVC intrinsics, etc.).

Key transformations:
- `nextVictimBuffer` from lock-protected integer to `pg_atomic_uint32`.
- `BufFreelistLock` deprecated in favor of short-held `buffer_strategy_lock` (only for freelist chaining).
- Clock hand now advances without acquiring any lock:
  ```c
  buf_id = pg_atomic_fetch_add_u32(&nextVictimBuffer, 1) % NBuffers;
  ```

### Stage 6: Fully Atomic BufferDescriptor Fields (Postgres 9.6)

Remaining fields converted to atomics:
- `refcount`: `pg_atomic_uint32` with fetch_add/sub for pin/unpin.
- `usageCount`: `pg_atomic_uint32`.
- Flags (dirty, valid, etc.): atomically updated.

At this point:
- No per-buffer locks.
- No freelist lock on the fast path (only when acquiring a buffer from the freelist).
- Only `buffer_strategy_lock` remains globally, but is held briefly and not a throughput bottleneck because freelist access is almost always followed by expensive disk I/O.

## Module 5: Why Atomic Refcount Is Hard - Implementation Detail

Pinning semantics require that a buffer cannot be evicted if `refcount > 0`. The naive implementation:

```c
static inline bool
PinBuffer_LockFree(BufferDesc *buf)
{
    uint32 old = pg_atomic_read_u32(&buf->refcount);
    uint32 new;
    do {
        if (old == 0)
            return false; /* must be on freelist, not in pool */
        new = old + 1;
    } while (!pg_atomic_compare_exchange_u32(&buf->refcount, &old, new));
    return true;
}
```

Note the ABA problem resistance: Postgres uses monotonic counters that don't wrap in practice (max pins limited by `max_backends`). No hazard pointers because the buffer ID space is bounded and the `buf_table` hash table ensures stable ID reuse only after rejoining the freelist.

## Module 6: The Remaining Bottleneck - `buffer_strategy_lock`

Even after removing per-buffer locks, the clock hand must coordinate with freelist management:

```c
LWLockAcquire(BufferStrategyLock, LW_EXCLUSIVE);
victim = StrategyGetBuffer(...);
LWLockRelease(BufferStrategyLock);
```

This is a single LWLock. Why does it not bottleneck modern PostgreSQL?
1. **Amortization**: Each clock sweep covers many buffers; lock acquisition cost is O(1).
2. **I/O masking**: A cache miss triggers a `ReadBuffer` that blocks on I/O. Networked or NVMe storage has latency measured in µs-ms, dwarfing the ~100ns lock acquisition.
3. **Partitioning opportunity**: While not implemented, a partitioned strategy (multiple freelist queues) could eliminate even this lock, analogous to the `BufMappingLock` split.

## Module 7: Code-Level Walkthrough - `ReadBuffer_common`

```c
Buffer
ReadBuffer_common(SMgrRelation reln, ForkNumber forkNum,
                  BlockNumber blockNum, ReadBufferMode mode,
                  BufferTag *tag)
{
    uint32              hashcode;
    int                 buf_id;
    BufferDesc         *bufHdr;
    LWLockAcquire(BufMappingLock, LW_SHARED);
    buf_id = BufTableLookup(tag, &hashcode);
    LWLockRelease(BufMappingLock);

    if (buf_id >= 0) {
        bufHdr = &BufferDescriptors[buf_id];
        if (pg_atomic_fetch_add_u32(&bufHdr->refcount, 1) >= 1)
            return BufferIdGetBuffer(buf_id);
    }

    /* Cache miss: StrategyGetBuffer may atomically advance clock hand. */
    bufHdr = StrategyGetBuffer(reln, forkNum, mode, buf_id);

    /* Pin the newly selected buffer */
    pg_atomic_fetch_add_u32(&bufHdr->refcount, 1);

    /* Load page from OS/file cache or storage */
    ReadBuffer_common_locked(bufHdr, tag, ...);

    return BufferIdGetBuffer(bufHdr->buf_id);
}
```

Note the contention paths: `BufMappingLock` is shared for read and exclusive for insert/remove. Victim selection lives in `StrategyGetBuffer`.

## Module 8: Comparison With Operating System Page Cache

Linux's page cache uses an LRU variant (`active/inactive` lists, `workingset_*` refault tracking). PostgreSQL avoids OS page cache (via `O_DIRECT`) to implement its own clock-sweep with semantic knowledge (knows sequential scans are one-time accesses).

Key difference:
- OS cache: universal algorithm, no workload-specific hints.
- PostgreSQL: workload-aware via `usageCount`, `refcount` semantics, and the ability to bypass pages entirely.

## Lab Exercise: Instrumenting the Clock Hand

1. Compile PostgreSQL with `DEBUG_BLOCK_SIG` and `TRACE_SLOWLOG` enabled.
2. Connect to a running instance and run `pg_stat_bgwriter`.
3. Observe `buffers_checkpoint`, `buffers_clean`, `buffers_backend` to see clock-hand-driven eviction activity.
4. Use `perf record -e syscalls:sys_enter_pread64` to observe the cost of a physical I/O versus the cost of a clock-hand tick (should be immeasurable).
5. Repeat with `pg_prewarm` to pre-populate `usageCount` and measure eviction resistance.

## Discussion Questions
1. Why did Postgres choose a clock sweep over true LRU? Consider O(1) guarantees and per-access overhead in a multi-process shared pool.
2. Could `buffer_strategy_lock` be eliminated entirely? Sketch a lock-free freelist using hazard pointers or epoch-based reclamation.
3. How does `usageCount` interact with sequential table scans that touch millions of pages?
4. For a workload dominated by index-only scans, would a different replacement policy improve performance? What policy would you implement?

---

# Further Reading
- PostgreSQL source: `src/backend/storage/buffer/README`, `freelist.c`, `buf_table.c`.
- CMU 15-445 Database Systems: `bufmgr` lecture notes.
- Dichen Li (2025): "30 years of PostgreSQL buffer manager locking design evolution."
- C. Mohan et al. (1992): "ARIES: A Transaction Recovery Method" (buffer management context).