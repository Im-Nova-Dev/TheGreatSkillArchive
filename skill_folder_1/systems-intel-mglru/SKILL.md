---
name: systems-intel-mglru
description: "Teach Multi-Gen LRU (MGLRU): generation-based page reclaim replacing active/inactive LRU"
category: systems-internals
tags: [memory-management, page-reclaim, LRU, MGLRU, kswapd, folio, memcg]
version: 1.0
---

# Teaching: Multi-Gen LRU (MGLRU)

## Learning Objectives
- Explain why traditional active/inactive LRU fails under memory pressure
- Describe generation-based design: max_seq, min_seq, folio generations
- Walk through aging (promotion) and eviction (consumption) procedures
- Analyze tier system for file descriptor access patterns
- Evaluate working set protection via generation timestamps

## Prerequisites
- Linux page cache and page frame reclaim basics
- struct folio, page flags, rmap (reverse mapping)
- Memory cgroups (memcg) and LRU vec structure
- Refault detection and major/minor fault distinction

## Core Concepts

### Why Generations?
Traditional LRU: two lists (active/inactive), rough LRU approximation
- No common time reference across memcgs/nodes
- Hard to balance anon vs file pressure
- TLB flush cost not modeled
- Refault detection delayed

MGLRU: **generation timestamps** provide common frame of reference
- Enables cross-memcg and cross-node decisions
- Self-correcting PID feedback on refaults
- Fast paths: unmapped=no TLB flush, clean=no writeback

### Data Structures
```
lruvec (per node + memcg)
├── max_seq (youngest gen, shared anon+file)
├── min_seq[anon], min_seq[file] (oldest gen, separate)
├── folios[] (array indexed by truncated gen number)
└── Tiers within each generation (file descriptor access count)
```

**Generation numbers**: truncated to `order_base_2(MAX_NR_GENS+1)` bits in `folio->flags`
- Sliding window: `MIN_NR_GENS` to `MAX_NR_GENS` generations
- Values `1..MAX_NR_GENS` when on `lrugen->folios[]`; `0` otherwise
- Three monotonic counters: `max_seq`, `min_seq[anon]`, `min_seq[file]`

**Tiers**: page accessed `N` times via file descriptors → tier `order_base_2(N)`
- No dedicated array for tiers — atomic ops on `folio->flags`
- PID controller feedback loop monitors refaults across tiers

### Two Independent Procedures

#### Aging (Produces Young Generations)
```c
// Trigger
when (max_seq - min_seq + 1) approaches MIN_NR_GENS:
    increment max_seq
```

**Promotion mechanisms:**
1. **Page table walks**: iterate `lruvec_memcg()->mm_list`, `walk_page_range()` per `mm_struct`
2. **Rmap walks**: when eviction finds young PTE, scan adjacent PTEs
3. **On young PTE**: clear accessed bit, update gen counter to `(max_seq % MAX_NR_GENS) + 1`

#### Eviction (Consumes Old Generations)
```c
// Trigger
when lrugen->folios[min_seq % MAX_NR_GENS] becomes empty:
    increment min_seq
```

**Selection algorithm:**
1. Compare `min_seq[]` → select older type (anon vs file)
2. If equally old → select type whose **first tier** has lower refault %
   - First tier = single-use unmapped clean pages (best bet)
3. Sort by gen counter if aging updated it (page table access)
4. Move to `min_seq + 1` if:
   - Multiple file descriptor accesses AND
   - Feedback loop detected outlying refaults from its tier
   - Baseline: first tier refault rate

### Working Set Protection
- Each generation timestamped at birth
- If `lru_gen_min_ttl` set, `lruvec` protected when oldest gen born within TTL ms
- Advantages: easier config (agnostic to app/mem size), reliable (wired to OOM killer)

## Teaching Flow (90 min)

### 1. Traditional LRU Limitations (15 min)
- Active/inactive list approximation
- No cross-memcg comparison
- Refault detection latency
- TLB flush cost blindness

### 2. Generation Model (20 min)
- Generation numbers as timestamps
- Sliding window, truncated storage in folio flags
- Three monotonic sequences (max_seq, min_seq[anon/file])

### 3. Aging Procedure (20 min)
- Page table walks via mm_struct list
- Rmap walks for targeted aging
- Access bit clearing, gen counter update

### 4. Eviction Procedure (20 min)
- Min_seq consumption, type selection
- Tier-based refault comparison
- PID feedback loop mechanics

### 5. Working Set Protection & mm_struct List (15 min)
- Generation birth timestamps
- lru_gen_min_ttl configuration
- Per-memcg mm_struct list migration handling

## References
- Kernel docs: https://docs.kernel.org/mm/multigen_lru.html
- LWN: https://lwn.net/Articles/1063468/
- Default in distros since 6.1+

## Exercises
1. **Trace**: `cat /sys/kernel/debug/lru_gen/full` observe generations
2. **Tune**: Adjust `lru_gen_min_ttl`, measure refault rate under load
3. **Simulate**: Write userspace aging/eviction simulator with PID feedback
4. **Compare**: Benchmark MGLRU vs traditional LRU (echo 0 > /sys/kernel/mm/lru_gen/enabled)
5. **Debug**: Use `bpftrace` on `lru_gen_*` tracepoints