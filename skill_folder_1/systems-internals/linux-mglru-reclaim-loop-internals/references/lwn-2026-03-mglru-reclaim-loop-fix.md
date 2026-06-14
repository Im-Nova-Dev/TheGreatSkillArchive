# Reference: LWN 1063468 — mm/mglru: improve reclaim loop and dirty folio handling
Source: https://lwn.net/Articles/1063468/ (March 18, 2026)
Author: Kairui Song (Tencent, via B4 Relay)
Subject: [PATCH 0/8] mm/mglru: improve reclaim loop and dirty folio handling
Modified: mm/vmscan.c; net -29 LOC

## Problem Statement
MGLRU's reclaim loop had become a maintenance and performance liability:
- Aging, scan-number calculation, and reclaim were tightly coupled.
- Dirty folio writeback was decoupled from the reclaim scan, so dirty pages were skipped.
- Abort-after-aging path meant folios were isolated but never reclaimed, causing OOM despite evictable file-backed memory.
- Coarse reclaim batch size increased latency of individual reclaim rounds.

## Patch Series
1. consolidate common code for retrieving evitable size
2. relocate the LRU scan batch limit to callers
3. restructure the reclaim loop
4. scan and count the exact number of folios
5. use a smaller batch for reclaim
6. don't abort scan immediately right after aging
7. simplify and improve dirty writeback handling
8. remove sc->file_taken

## Performance Evidence
MongoDB YCSB B, 20M records, 6M ops, 32 threads, 95% read, NVMe, no swap:
- Before: 61642.78 ops/sec, latency 507.11 µs, pgpgin 158190589, workingset_refault 7262988
- After: 80216.05 ops/sec (+30.1%), latency 388.18 µs (-23.5%), pgpgin 101871227 (-35.6%), workingset_refault 3418186 (-52.9%)

Chrome + Node.js, 32 cgroups, 64 workers each, 2-node 128G NUMA, 256G ZRAM swap:
- Total requests 77920 -> 79564 (+2.1%)
- Jain fairness 0.996706 -> 0.996328 (no regression)

OOM reproducer (1 node pmem ramdisk, 120ms mmap batch pauses, anon alloc, 52G demand vs 48G memcg):
- Pre-patch: hung/OOM after 10-20 iterations; anon 46.7G, file 4.16G
- Post-patch: 128 iterations complete successfully

## Code Paths to Inspect
- mm/vmscan.c: `shrink_folio_list()`, `reclaim_folio_list()`, `mglru_lru_gen_scan()`
- mm/swap.c: folio aging and promotion helpers
- mm/memcontrol.c: memcg-aware reclaim wrappers
- tracepoints/mm/vmscan.h: `trace_mm_vmscan_lru_shrink_inactive_start/end`

## Pitfalls
- dirty folio writeback is rate-limited by background flusher; reclaim loop now initiates it inline instead of precomputing dirty counts.
- smaller batches mean more frequent loop re-evaluation, reducing chance dirty pages stall progress.
