---
name: systems-intel-postgresql-buffer-manager
description: "Teach 30-year evolution of PostgreSQL buffer manager locking: global lock → per-buffer → partitioned → atomics"
category: systems-internals
tags: [postgresql, buffer-manager, locking, concurrency, atomics, clock-sweep]
version: 1.0
---

# Teaching: PostgreSQL Buffer Manager Locking Evolution (30 Years)

## Learning Objectives
- Trace locking evolution: monolithic → per-buffer → partitioned → atomic
- Explain BufferTag hash table, BufferDescriptor, clock-sweep replacement
- Analyze why each bottleneck emerged and was resolved
- Apply lock granularity patterns to other systems

## Prerequisites
- Basic database buffer pool concepts (pages, pins, replacement)
- Lock types: mutex, RW lock, spinlock
- Atomic operations and memory ordering
- Hash table partitioning concepts

## Evolution Timeline

### Prehistory — Monolithic `BufMgrLock`
```c
BufMgrLock  // Single global lock for ALL operations
```
- Every lookup, eviction, read/write competed for same lock
- Pin count (`refcount`) protected by `BufMgrLock` — prevents eviction

### 6.5 (1998) — Buffer Context Lock (`cntx_lock`)
| Lock | Scope | Purpose |
|------|-------|---------|
| `cntx_lock` (per buffer) | Buffer content | Shared reads, exclusive writes |
| `BufMgrLock` (global) | Table, pins, flags, freelist | Short ops only |

**Key distinction:**
- **Pin** → protects from eviction
- **`cntx_lock`** → coordinates read/write of page data
- Must **pin first**, then acquire `cntx_lock`
- Multiple pins OK; only one exclusive `cntx_lock` for writing

### 8.1 (2005) — Decoupling `BufMgrLock` Monolith
Split into three locks:
| Lock | Protects |
|------|----------|
| `BufMappingLock` | Hash table (add/remove/lookup), BufferTag |
| `BufFreelistLock` | Clock hand (`nextVictimBuffer`), FreeList |
| `buf_hdr_lock` (per buffer) | Most descriptor fields |

**Gains:** No `BufMappingLock` for page header flags/clock-sweep; no `BufFreelistLock` if buffer in memory.
**New bottlenecks:** `BufMappingLock`, `BufFreelistLock`.

### 8.2 (2006) — Partitioned `BufMappingLock`
- Hash table → **static buckets**, dynamic element lists
- **One lock per bucket** — protects only that bucket
- Pattern seen widely in systems/libraries

### 9.5 (2015) — Removing `BufFreelistLock`
**Problem:** `BufFreelistLock` held for long clock-sweep — "disastrous for concurrency"

**Two phases:**
| Phase | Change | Author |
|-------|--------|--------|
| 1 | `BufFreelistLock` → short-held `buffer_strategy_lock`; released each clock tick | Robert Haas |
| 2 | `nextVictimBuffer` → **atomic integer**; clock ticking lock-free | Andres Freund |

`buffer_strategy_lock` retained for freelist (linked list) only.

### 9.6 (2016) — Full Atomicity
All descriptor fields → **atomic integers**:
- `refCount` (pin count)
- `usageCount`
- Other flags

**Result:** `buf_hdr_lock` **deprecated entirely**

> "That's the end of the story! No major change since."

## Current Lock Map
| Component | Implementation |
|-----------|----------------|
| Hash table | Partitioned `BufMappingLock` (per-bucket) |
| Pin count | Atomic integer |
| Usage count | Atomic integer |
| Clock hand | Atomic integer |
| Freelist | `buffer_strategy_lock` (short-held) |
| Buffer content | `cntx_lock` (per buffer, RW) |

## Teaching Flow (75 min)

### 1. Buffer Manager Architecture (10 min)
- 8KB pages, fixed buffer array, BufferTag → buffer ID hash
- Clock sweep: `nextVictimBuffer`, `usage_count` decrement sweep

### 2. Lock Evolution Walkthrough (30 min)
- Each phase: bottleneck → solution → new bottleneck
- Why pin ≠ content lock distinction matters
- Partitioning as universal pattern

### 3. Atomic Transition Deep Dive (20 min)
- Phase 1: short-held lock + release on each tick
- Phase 2: atomic `nextVictimBuffer` → lock-free clock
- Phase 3: all fields atomic → per-buffer header lock removed

### 4. Patterns & Generalization (15 min)
- Global → per-object → partitioned → atomic progression
- When to stop: contention vs complexity tradeoff
- Applicability: any fixed-size shared resource pool

## References
- Medium: Dichen Li, Mar 2025, "30 Years of PostgreSQL Buffer Manager Locking Design Evolution"
- Commits linked in article (Mikheev, Lane, Haas, Freund)

## Exercises
1. **Trace**: Instrument `BufMappingLock` contention under pgbench
2. **Atomic**: Convert a simple spinlock-protected counter to atomic
3. **Partition**: Implement partitioned hash table with per-bucket locks
4. **Simulate**: Clock sweep with atomic hand vs mutex hand
5. **Analyze**: Current `bufmgr.c` — find remaining lock operations