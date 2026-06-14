---
name: mglru-reclaim-loop-internals
description: "Mechanistic internals of Linux Multi-Gen LRU (MGLRU) reclaim loop design, aging vs reclaim coupling, dirty folio flush semantics, generation promotion, and the 2026 bug fixes that eliminated spurious OOMs and raised MongoDB throughput by ~30%. Targets OS students and database/kernel developers at the mechanistic \"why does it scan and evict what it does\" level."
tags:
  - linux-kernel
  - mm
  - mglru
  - memory-reclaim
  - vmscan
  - folio
  - oom
  - database-performance
related_skills:
  - systems-internals/linux-mglru-reclaim-loop-dirty-folio
  - university-cs/operating-systems/linux-mglru-reclaim-loop-dirty-folio
---

# MGLRU Reclaim Loop Internals

## Source material
LWN.net Article 1063468: `[PATCH 0/8] mm/mglru: improve reclaim loop and dirty folio handling`
Base commit: `dffde584d8054e88e597e3f28de04c7f5d191a67`

## 1 What MGLRU tries to do
Instead of the traditional two-list LRU (active/inactive), MGLRU keeps multiple generation descriptors per folio and moves folios between generations as they are referenced. Younger generations are "hot," older generations are "cold." Reclaim targets the oldest generations first.

## 2 The original problem: hidden coupling and dirty flush omission
Before March 2026:

- `shrink_folio_list()` / `mglru_lru_gen_scan()` combined 3 concerns in one loop:
  1. deciding *which* folios to try to reclaim
  2. walking generations and counting how many to scan
  3. executing writeback for dirty folios
- Dirty flush was performed in the *aging* preliminary scan, not the reclaim scan, so dirty folios often returned to the LRU without ever being written out or reclaimed.
- After reclaim, if no folios had been freed, the loop could still report occupancy as "successful" because generation counters moved without reflecting actual reclamation.
- Result: under memory pressure, the kernel could kill processes (OOM) while file folios sat on old generations that were effectively "invisible" to reclaim due to dirty/skip logic.

## 3 The fix: scan budgets, decoupled helpers, and in-loop dirty flush

### 3.1 Scan-budget design
At the top of each iteration, the loop computes an explicit folio scan budget. The budget limits how many folios it will walk in that pass. This replaces the earlier implicit "walk until something interesting" logic, which could scan arbitrarily many folios before returning.

### 3.2 Aging vs reclaim decoupling
- Aging (demotion to colder generations) is now a separate path and optional.
- Reclaim returns `nr_reclaimed` + `nr_scanned` so the caller can apply MGLRU-specific throttling (e.g., "if we scanned 1024 folios and reclaimed 0, stop trying and let the OOM killer run").
- This is why the OOM reproducer now works: the loop sees that no file folios are being reclaimed and falls through instead of pretending progress.

### 3.3 Dirty writeback moved into the reclaim loop
The dirty flush now happens *during* reclaim rather than in a pre-pass. Mechanistically:

1. Reclaim walks a generation.
2. If it encounters a dirty folio, it calls `writeout()` (via `writeout_per_bio`).
3. The folio is held in `WBC` and re-visited; if still dirty after writeback, it is skipped for this pass (not falsely claimed as reclaimed).
4. If writeback succeeds, the folio is then a candidate for actual eviction.

### 3.4 Smaller reclaim batch
Smaller batches keep the loop responsive, reduce the chance that a long writeback blocks other cgroup/lru work, and make "end-of-loop" bookkeeping more accurate.

## 4 Concrete before/after behavior

| Behavioral Failure | Pre-fix | Post-fix |
|---|---|---|
| Spurious OOM despite evictable file folios | Yes | No |
| Dirty folios skipped without writeback | Yes | No |
| Refault rate (MongoDB YCSB B) | Baseline | -52.9% |
| MongoDB throughput (same workload) | Baseline | +30.1% |

## 5 Mechanistic code-path walkthrough

### `mm/vmscan.c` reclaim decision tree (simplified)
```
mglru_lru_gen_scan()
  ├─ budget = compute_folio_budget(...)
  ├─ for each generation oldest -> newest
  │    ├─ scan at most `budget` folios
  │    ├─ if clean            → put on LRU to reclaim list
  │    ├─ if dirty+writeback  → trigger writeback; retract to next pass
  │    ├─ if referenced       → keep; flip to younger generation
  │    └─ count nr_scanned / nr_reclaimed
  └─ return (nr_reclaimed, nr_scanned)
```

### Exact looked-up symbols
- `mm/vmscan.c`: `shrink_folio_list()`, `mglru_lru_gen_scan()`, `shrink_node()`, `shrink_node_memcg()`
- Folio state used: `folio_test_dirty()`, `folio_test_writeback()`, `folio_test_referenced()`, `folio_test_unevictable()`
- Writeback path: `writeout_per_bio()`, `wbc_attach_folio_create()`

## 6 Database engine implications
Database engines (PostgreSQL, MongoDB, MySQL) with large buffer pools own folios in the *file* LRU rather than anonymous pages. When MGLRU mis-scanned dirty file folios:

- Eviction probability for truly clean pages dropped, pushing useful pages to colder generations.
- Memory pressure triggered more flips to swap / OOM because file folios counting as "used" never left RAM.
- The fix improves fairness in mixed-file+anon workloads: file folios that are genuinely clean now age out predictably, reducing unnecessary eviction of anonymous buffer-pool pages.

## 7 Observability
- `/proc/vmstat`: `pgpgin`, `pgpgout`, `pgscan`, `pgsteal`, `pgactivate`
- `/sys/kernel/mm/lru_gen/`: generation walk counters per memcg
- `bpftrace`/`tracefs`: trace `mm_vmscan_direct_reclaim_begin` + `mm_vmscan_direct_reclaim_end` to count loop iterations and reclaimed folios per iteration
- `debugfs/tracing`: trace `mglru_lru_gen_scan` once instrument hooks are added

## 8 Patch Summary

| Patch | Subject | Key Change |
|-------|---------|------------|
| 1 | consolidate common code for retrieving evictable size | Code deduplication |
| 2 | relocate the LRU scan batch limit to callers | Move batch limit logic |
| 3 | restructure the reclaim loop | Core loop restructuring with scan budget |
| 4 | scan and count the exact number of folios | Precise scan counting |
| 5 | use a smaller batch for reclaim | Reduce batch size |
| 6 | don't abort scan immediately right after aging | Fix aging blocking reclaim |
| 7 | simplify and improve dirty writeback handling | Move dirty flush into reclaim loop |
| 8 | remove sc->file_taken | Cleanup unused field |

**Net code change:** `mm/vmscan.c` - 81 insertions(+), 110 deletions(-) = **29 lines removed**

## 9 Detailed test results (LWN 1063468, March 2026)
### MongoDB + YCSB Workload B (95% read, 5% update) — **Primary Win**
- **Hardware**: 48c/96t NUMA machine, 2 nodes, 128GB memory, NVMe storage
- **Setup**: MongoDB in 10G cgroup, WiredTiger cache 4.5G, **no swap**, NVMe storage
- **Methodology**: Median of 3 runs, results described as "stable"

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Throughput (ops/sec)** | 61,643 | 80,216 | **+30.1%** ↑ |
| **Average Latency (µs)** | 507.1 | 388.2 | **-23.5%** ↓ |
| **pgpgin (page-ins)** | 158,190,589 | 101,871,227 | **-35.6%** ↓ |
| **pgpgout (page-outs)** | 5,880,616 | 5,770,028 | -1.9% |
| **workingset_refault** | 7,262,988 | 3,418,186 | **-52.9%** ↓ |

> **Author note:** "We can see a significant performance improvement after this series for file cache heavy workloads like this. The test is done on NVME and the performance gap would be even larger for slow devices, we observed >100% gain for some other workloads running on HDD devices."

### Chrome &amp; Node.js (Yu Zhao's test script) — **Fairness verification**
- **Configuration**: 256G ZRAM swap, 32 memcg, 64 workers

| Metric | Before | After |
|--------|--------|-------|
| Total requests | 77,920 | 79,564 |
| Per-worker 95% CI (mean) | [1199.9, 1235.1] | [1224.2, 1262.2] |
| Per-worker stdev | 70.5 | 76.1 |
| Jain's fairness | 0.996706 | 0.996328 |

**Latency distribution:** Nearly identical across all buckets.
**Conclusion:** "Seems identical, reclaim is still fair and effective, total requests number seems slightly better."

### OOM Issue Reproducer — **Critical Fix (Patch 6)**
- **Scenario**: Mixed file (mmap reads with 120ms pause) + anonymous allocation exceeding memcg limit (52G vs 48G limit). File worker pauses should allow reclaim to keep up.

| Configuration | Result |
|---------------|--------|
| MGLRU disabled | ✅ Finished 128 iterations |
| MGLRU enabled (before) | ❌ Hung/OOM after ~10-20 iterations |
| MGLRU enabled (after patch 6) | ✅ Finished 128 iterations |

> **Root cause:** Patch 6 ("don't abort scan immediately right after aging") fixes the issue where aging would prematurely terminate the reclaim scan, leaving evictable file folios un-reclaimed and causing OOM.

### Other workloads (no regression)
- Chrome/Node.js fairness: Jain's index ~0.996 maintained
- MySQL: +1.26% TPS at peak (innodb_buffer_pool=26G, 2G memcg)
- FIO: +4.2% MB/s peak (EXT4 ramdisk, zipf:1.2)
- Kernel build: -1.6% time (3G memcg, ZRAM swap, tmpfs)

## 10 Related 2026 developments
- **cache_ext** (LSFMM+BPF 2026): eBPF-customizable page cache eviction — 70% GET throughput improvement via custom `struct_ops` per cgroup
- **NO_PAGE_MAPCOUNT** (kernel 6.15+): Eliminate `mapcount` field, replace with folio `_total_pages_mapped` — less precise PSS but simpler reclaim
- **MGLRU flag optimization**: Shift 3 page flags to enable up to 63 generations
- **BPF hook proposal**: Custom generation-placement decisions via BPF
- **Android foreground integration**: Vendor hook exempts foreground task from reclaim (not mainline)

## 11 Teaching module (enhanced)
1. Read `mm/vmscan.c` around `mglru_lru_gen_scan()`. Identify where dirty folios enter writeback in pre-fix code and trace why they never reached eviction.
2. Instrument a workload with mixed file-backed (mmap SQLite or WiredTiger) and anon memory; measure OOM frequency before/after.
3. Compare generation-wise page-age histograms under memory pressure with `/sys/kernel/mm/lru_gen/` to see if old generations are actually shrinking post-fix.
4. Trace `workingset_refault` and `pgpgin` correlation: when refault rate drops, observe how efficiently working set is identified.
5. Build a minimal reproducer: memcg with 48G limit, 52G pressure (46G anon + 4G file, file worker pausing), verify OOM before/after.