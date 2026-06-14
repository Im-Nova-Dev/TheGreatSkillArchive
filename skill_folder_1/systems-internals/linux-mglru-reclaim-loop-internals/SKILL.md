# Linux MGLRU Reclaim Loop Internals
Mechanistic how-it-works coverage of Multi-Gen LRU page reclaim, dirty folio handling, and the 2026 reclaim-loop refactor.

## 1. What This Skill Covers
- Classic LRU vs MGLRU design differences (generation concept, eviction order).
- The reclaim loop: scanning budget, generation aging, folio selection, and dirty page handling.
- The pathology fixed by the March 2026 series: tight coupling of aging/reclaim/scan-number plus ineffective dirty flush.
- How to read the code paths and instrumentation (`workingset_refault`, `pgpgin`, `pgmajfrac`).
- Debug signals: unexpected OOM with file folios still available, low `pgpgin` reduction under file-heavy loads.
- Kernel configs and knobs: `CONFIG_LRU_GEN`, `CONFIG_LRU_GEN_STATS`, sysfs walkthrough at `/sys/kernel/mm/lru_gen/`.

## 2. Why MGLRU Was Introduced
Classic active/inactive LRU lists fight between protecting young pages and aggressively reclaiming cold ones. MGLRU introduces explicit generations:

- Each page is assigned a generation number (affine to LRU clock).
- Accesses promote pages to younger generations.
- On reclaim, the oldest generations are scanned first.
- Goal: more accurate coldness estimation and lower reclaim overhead.

MGLRU was merged around Linux 6.1. Expected benefits:
- Better distinguishing between hot and cold pages.
- Reduced CPU time in `vmscan`.
- Better behavior under memory pressure for file-backed and anon workloads alike.

## 3. The Reclaim Path at a Glance
Simplified flow when a memcg or system hits its reclaim target:

1. `try_to_free_mem_cgroup_bounded()` or `shrink_node()` calls into MGLRU via `get_scan_range()`.
2. MGLRU walks generations from oldest to newest:
   - `inc_nr_migrated()` or `get_nr_to_scan()` decides scan budget (max folios to scan this round).
   - `shrink_folio_list()` gets invoked with a prepared `struct list_head *list` of candidate folios.
3. For each folio:
   - If active: try to deactivate (page referenced but not “hot”).
   - If inactive: try to reclaim. Reclaim succeeds with `try_to_unmap()` + `remove_mapping()`.
   - If dirty: writeback is triggered. In the pre-patch path, dirty folio handling was coupled and often skipped/aborted.
4. If target not met, retry loop scans more generations.

## 4. The Pathology: Tight Coupling and Dirty Flush Ineffectiveness
The March 2026 patches (Kairui Song, LSFMMBPF 2026 context) fix these specific behavioral issues:

- Aging, scan-number calculation, and reclaim loop ran in tangled control flow.
- Dirty folio writeback happened in a separate path that often did not fire during reclaim scans.
- Immediate abort right after aging meant many pages never entered the actual reclaim step.
- Scan batch size was coarse and coupled to list creation rather than remaining budget.

Observable symptom before patch:
- File faults elevated (`pgpgin` high), Mongo/YCSB throughput flat or regressed.
- Unexpected OOM despite evictable file folios present.
- Workingset refaults were much higher than ideal.

## 5. Mechanistic Code-Level Details (post-patch behavior)
### 5.1 Scan Budget
- `nr_to_scan` is computed once per reclaim loop iteration.
- List creation batches folios; reclaim loop checks budget and stops without over-scanning.

### 5.2 Decoupled Aging
- `list_lru_isolate()` or equivalent isolates candidate folios first.
- Aging only affects non-reclaimable promotion between inactive/active sets.
- Reclaim no longer aborts right after aging, so every isolated folio goes through full reclaim attempt.

### 5.3 Dirty Flush Inside the Reclaim Loop
- Dirty folios encountered in the reclaim list are now handled immediately:
  - If `folio_test_dirty()`:
    - Try to writeback via `writeout()` path.
    - If writeback initiated, folio is either skipped this pass (launder) or reclaimed if writeback succeeds before scan arrives.
- This tracks pages as they actually appear during reclaim instead of relying on precomputed dirty counts.

### 5.4 Smaller Reclaim Batch
- Smaller batches improve responsiveness: reclaim loop can re-evaluate remaining budget and dirty pressure sooner.

### 5.5 Removal of `sc->file_taken`
- `file_taken` was a counter tracking file-backed pages already reclaimed in this scan. Removing it simplifies accounting because the reclaim loop now drives its own iteration independently.

## 6. Performance Evidence
### MongoDB YCSB Workload B (no swap, NVMe)
- Throughput: 61642 → 80216 ops/sec (+30.1%)
- Average latency: 507 µs → 388 µs
- File refaults dropped 52.9%
- `pgpgin` dropped 35.6%

### Chrome/Node memory cgroups (2-node NUMA, ZRAM swap)
- Request throughput: +2.1% (non-regressive)
- Jain fairness: remains ~0.996, i.e., fair.

### OOM reproducer (no swap, 48GB memcg vs 52GB demand)
- Pre-patch MGLRU: hung/OOM after 10-20 iterations with file folios still evictable.
- Post-patch: completed all 128 iterations successfully.

## 7. Key Data Structures and Symbol Map
| Symbol | Role |
|--------|------|
| `struct lruvec` | Per-memcgroup + node LRU state; holds generation counters and folio lists. |
| `struct gen_cookie` | Tracks “when” a generation was born for affine promotions. |
| `lru_gen_run()` / `lru_gen_shrink_one()` | Core loop functions. |
| `inc_nr_migrated()` | Advances target generation and returns pages scanned. |
| `workingset_activation()` | When a folio is referenced during reclaim, it gets reactivated into a younger generation. |
| `workingset_refault` | Per-node counter used to detect thrashing; tracked via `/proc/vmstat`. |
| `pgpgin`/`pgpgout` | Overall page-in/page-out counters from `/proc/vmstat`. |
| `lruvec->flags` | Contains `LRUVEC_CONGESTED`, `LRUVEC_ACTIVE`, etc., used to skip/select generations. |

## 8. Sysfs and Tracing Interface
Read current state:
- `/sys/kernel/mm/lru_gen/`
  - `enabled` (0/1), `min_gen`, `max_gen`, etc.
  - Per-memcg directories if `CONFIG_MEMCG` enabled.

Trace MGLRU behavior:
- `trace_mm_vmscan_lru_shrink_inactive_start()`
- `trace_mm_vmscan_lru_shrink_inactive_end()`
- These tracepoints expose scanned/reclaimed/dirty pages per node/memcg.

Key vmstat counters to monitor:
- `workingset_refault`: spikes indicate reclaim is failing to keep hot pages.
- `pgpgin`: drops mean fewer file page-ins during steady state.
- `pgmajfault`: major fault rate; high values mean disk thrashing.

## 9. Config Options
- `CONFIG_LRU_GEN`: enable MGLRU.
- `CONFIG_LRU_GEN_STATS`: adds cheaper stats gathering for instrumentation.
- Boot parameter: `lru_gen=1` to enable on kernels that treat it as optional.

Runtime control via sysfs:
```bash
cat /sys/kernel/mm/lru_gen/enabled
```

If disabled, the kernel falls back to active/inactive LRU automatically.

## 10. Interaction with Other Subsystems
### NUMA
- MGLRU tracks `lruvec` per node × memcg. Reclaim can prefer local node folios if memcg cpuset constrains placement.
- Cross-node migrations may briefly trigger extra folios to age before eviction.

### cgroup v2
- Memory pressure triggers reclaim at memcg boundary.
- `memory.high`/`memory.max` use the same vmscan entry points; MGLRU does not change cgroup reclaim semantics.

### THP
- Transparent Huge Pages increase folio batch sizes. Dirty THPs require writeback of the entire folio before reclaim.

## 11. Practical Diagnosis
### Symptom: Database workload suffers under memory pressure
1. Check `workingset_refault` trend (increasing or flat?).
2. Check if MGLRU is enabled (`/sys/kernel/mm/lru_gen/enabled`).
3. Compare `pgpgin` before/after filesystem scrub or logical changes; large drop implies better cache residency.
4. If OOM occurs with file folios present:
   - Capture `dmesg` post-patch to see if reclaim loop timed out.
   - Inspect `trace_mm_vmscan_lru_shrink_inactive_start/end` to see reclaim ratio per generation.

### Tuning
- If dirty IO is skewing reclaim, use `vm.dirty_ratio` and `vm.dirty_background_ratio` to control writeback pressure independently of LRU behavior.
- For database-heavy workloads, monitor whether readahead is polluting youngest generations; adjust `readahead_ratio` or application-level prefetch patterns.

## 12. How to Read the Code
Useful entry points:
- `mm/vmscan.c`: `shrink_folio_list()`, `reclaim_folio_list()`, `try_to_reclaim_page()`.
- `mm/swap.c`: folio aging and promotion helpers.
- `mm/memcontrol.c`: memcg-aware reclaim wrappers invoking MGLRU.
- `tracepoints/mm/vmscan.h`: events marking shrink start/end.

Build gentle reading order:
1. `lruvec_init()` — sets up generation bookkeeping.
2. `get_scan_range()` — determines generations and scan count.
3. `list_lru_isolate()` / `__list_lru_walk_one()` — isolate candidate folios.
4. `shrink_folio_list()` — apply reclaim logic to isolated folios.
5. `workingset_activation()` / `folio_add_lru()` — promotion after successful reuse.

## 13. Watch Items (2026–2027)
- Further patches to decouple generation-placement policy for better file/anon balance.
- BPF hook proposal for custom generation assignment.
- Readahead page placement fix (considered simple but not yet landed as of this skill).
- Potential removal or refactor of entire MGLRU if maintainership remains disputed; watch for `CONFIG_LRU_GEN` becoming defconfig on by default or dropped.

## 14. Pitfalls and Common Misunderstandings
- MGLRU does not eliminate OOM; it just scavenges more effectively. If allocation pressure exceeds all reclaimable memory, OOM still wins.
- `swappiness` is less meaningful under MGLRU; generation placement heuristics supersede it.
- Dirty folios still require writeback bandwidth; MGLRU cannot make a slow disk faster.
- Generation count grows monotonically and wraps modulo a maximum; probes on `/sys/kernel/mm/lru_gen/` can expose overflow semantics if you export gen IDs to userspace.

## 15. References and Further Reading
- LWN “Reconsidering the multi-generational LRU”: https://lwn.net/Articles/1060967/
- LWN “mm/mglru: improve reclaim loop and dirty folio handling”: https://lwn.net/Articles/1063468/
- Linux kernel documentation: `Documentation/mm/multigen_lru.rst`
- Core kernel code: `mm/vmscan.c`, `mm/swap.c`, `mm/memcontrol.c`
- Phoronix benchmark coverage: https://www.phoronix.com/news/Linux-MGLRU-30p-MongoDB
- PostgreSQL buffer manager locking context (related cache pressure): `/home/nova/.hermes/intel/systems/postgresql_bufmgr_locking_evolution_2025-06.md`
