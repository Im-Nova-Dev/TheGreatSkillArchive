---
name: eevdf-preempt-lazy-zcrx-mglru-cross-layer-internals
description: Mechanistic cross-layer OS internals module covering how Linux 7.0’s default PREEMPT_LAZY + EEVDF scheduler interacts with io_uring ZC Rx completion storms and MGLRU reclaim behavior. Covers latency inversion, dirty-flush stalls, NUMA-aware page aging, and the production pathologies exposed by MongoDB YCSB and the March 2026 MGLRU reclaim-loop fixes.
triggers:
  - EEVDF
  - PREEMPT_LAZY
  - io_uring zero copy
  - ZC Rx
  - MGLRU
  - cross-layer scheduler memory networking
  - latency inversion
  - dirty folio reclaim stall
  - NUMA page aging
---

# EEVDF / PREEMPT_LAZY + io_uring ZC Rx + MGLRU Cross-Layer Internals

Mechanistic how-it-works for advanced OS students and performance engineers. Target kernel: Linux 7.0 (Arch rolling, Ubuntu 26.04 LTS baseline). Focus: why a multishot `IORING_OP_RECV_ZC` workload can make EEVDF deadlines slip, why MGLRU reclaim stalls under mixed ZC Rx + dirty file pressure, and how the March 2026 reclaim-loop refactor changes the observable behavior.

---

## 1. The three subsystems and why they collide

| Subsystem | Role in the hot path | Key struct / knob |
|---|---|---|
| EEVDF + PREEMPT_LAZY | Chooses which task runs next; “lazy” defers `need_resched` until slice/tick | `sched_latency`, `sched_min_granularity_ns`, `preempt_lazy` |
| io_uring ZC Rx | Delivers packet payloads as DMA’d user pages with CQE notifications | `io_uring_zcrx_area_reg`, refill ring, `IORING_RECV_MULTISHOT` |
| MGLRU reclaim | Evicts cold folios when memcg hits `memory.high`/`memory.max` | `lru_gen_run()`, `mglru_lru_gen_scan()`, dirty writeback path |

Collision: a CPU-bound receiver thread running `io_uring` multishot ZC Rx can hold the CPU for thousands of completions without yielding. Under EEVDF + PREEMPT_LAZY, the kernel only checks for preemption at tick or explicit yield, so the receiver can starve latency-sensitive tasks across the same run queue. Concurrently, if the receiver thread is also dirtying pages (e.g., parsing into a mmap’d WiredTiger cache), MGLRU reclaim must walk those dirty folios; if dirty writeback was happening in a decoupled pre-pass rather than inside the reclaim scan, the OOM killer could fire while clean file folios still existed.

---

## 2. EEVDF deadline mechanics under sustained ZC Rx

### 2.1 vruntime and lag
- Each task has `vruntime` (accumulated virtual runtime).
- EEVDF schedules eligible tasks in **increasing `vruntime` order**: the task with lowest `vruntime` runs next.
- When a task sleeps, its `vruntime` is frozen. On wakeup, EEVDF compares its `vruntime` against the current CPU’s `cfs_rq->min_vruntime`.
- If `vruntime < min_vruntime`, the task is “owed CPU” and preempts.

### 2.2 What PREEMPT_LAZY changes
- Traditional `PREEMPT` clears `TIF_NEED_RESCHED` at every kernel exit.
- `PREEMPT_LAZY` batches reschedule checks into a lazy flag evaluated only at voluntary preempt points (`cond_resched()`, explicit syscalls, tick).
- Consequence: long `io_uring` completions loops in kernel context do *not* preempt immediately.

### 2.3 ZC Rx completion loop anatomy
1. Userspace submits `IORING_OP_RECV_ZC` + `IORING_RECV_MULTISHOT`.
2. Kernel issues `io_recvzc` against the ZC page pool.
3. NAPI / softirq fills page from NIC DMA and posts CQE.
4. Application drains CQ in a tight `io_uring_peek_cqe` loop.
5. After processing, application advances refill ring tail to return buffer to kernel pool.

Steps (4)-(5) can consume an entire time slice on one CPU without reaching a preempt check.

### 2.4 Latency inversion pattern
- A foreground DB task on the same CPU is eligible and has low `vruntime` (owed CPU).
- The ZC Rx receiver loop does not yield.
- EEVDF cannot preempt because PREEMPT_LAZY suppresses `need_resched`.
- Result: foreground task misses its deadline; tail latency spikes.

Mitigation primitives:
- `io_uring_submit_and_wait_cancel(ring, min_complete)` introduces a blocking wait point that hits the scheduler’s voluntary preempt path.
- `sched_yield()` inside the polling loop when CQ depth exceeds a threshold.
- Set `IORING_SETUP_SQPOLL` + `DEFER_TASKRUN` to decouple completion draining from the application thread’s CPU budget (kernel thread runs the CQ drain, application thread only blocks on `peek_cqe`).

---

## 3. MGLRU dirty-folio reclaim stall mechanism

### 3.1 Pre-March-2026 pathology
The old reclaim loop combined three concerns:

1. generation aging (promotion/demotion)
2. scan-number calculation (how many folios to walk)
3. dirty folio writeback execution

Dirty writeback was performed in a preliminary pass *before* the primary reclaim scan, not *during* it. When reclaim encountered a dirty folio during the actual scan, it usually skipped it without triggering writeback because the pre-pass had already decided the dirty set. This created two failure modes:

- **Spurious OOM**: Reclaim reported “all candidates scanned” but freed ~0 pages because every candidate was dirty and skipped.
- **Refault amplification**: Dirty file folios never written back remained in RAM in old generations, crowding younger hot pages into colder generations and causing extra refaults.

### 3.2 Post-patch behavior (Linux 7.0 with March 2026 series)
- Scan budget is computed at loop entry.
- Reclaim iterates the isolated folio list:
  - Clean folio → try reclaim immediately.
  - Dirty folio → trigger `writeout_per_bio()` / `wbc_attach_folio_create()` inside the scan.
  - If writeback launched, folio is skipped this scan but tracked for next pass.
- Decoupled aging: promotion/demotion is a separate phase; abort after aging no longer short-circuits reclaim.

### 3.3 Interaction with ZC Rx pressure
When ZC Rx delivers payloads into an application mmap region backed by a tmpfs or ext4 file:
- Application writes into the mmap region → dirties file folios.
- MGLRU must reclaim or write back those folios under memcg pressure.
- If dirty writeback is forced *outside* reclaim (old path), the pressure window is lost.
- New path’s in-loop writeback means dirty folios encountered during reclaim are written immediately, breaking the OOM death loop.

### 3.4 NUMA-sensitive aging under ZC Rx + MGLRU
ZCRX can allocate pages on a specific NUMA node (via `mbind()` on the data area). MGLRU tracks `lruvec` per (node × memcg). When a process dirties pages on node A but runs on node B:
- The pages age in node A’s `lruvec`.
- Reclaim on node B’s memcg may scan node A `lruvec` only if cross-node LRU scanning is enabled.
- Result: dirty folios on the “wrong” node survive longer, increasing OOM risk on the pressured node.

Debug signal:
- `cat /sys/kernel/mm/lru_gen/min_ttl_ms` — see generation TTL; high TTL makes cross-node aging even slower.
- `trace_mm_vmscan_lru_shrink_inactive_start` / `_end` tracepoints show per-node scanned/reclaimed counts.

---

## 4. Cross-layer production pathology (synthesized from LWN + arXiv + CVE data)

### 4.1 Scenario A: Database + ZC Rx
A MongoDB or PostgreSQL instance uses `io_uring` ZC Rx for replication traffic and runs its own buffer pool (mmap’d WiredTiger / shared_buffers) on the same machine.

1. ZC Rx multishot loop burns a full CPU slice.
2. EEVDF + PREEMPT_LAZY fail to preempt; foreground DB query latency spikes.
3. Simultaneously, the buffer pool dirties pages beyond memcg limit.
4. MGLRU reclaim starts; dirty flush is ineffective (pre-patch) → spurious OOM.
5. Post-patch MGLRU writes back dirty folios early, but if the ZC Rx thread holds `kswapd`/`kcompactd` CPU budget via reclaim loops, foreground latency still rises.

### 4.2 Scenario B: CVE-2026-43121 amplification under ZC Rx
- ZCRX manages `niov` freelist and per-slot `user_refs`.
- Refill and scrub paths race on SMP systems.
- Under heavy ZC Rx traffic, the race window widens because the refill ring is drained faster, increasing the chance that a scrub happens concurrently with a refill put.
- 4-byte OOB write corrupts freelist metadata; next `io_zcrx_return_niov()` may return a stale pointer to the NIC hardware queue → memory corruption or NIC DMA to freed memory.

---

## 5. Mechanistic code-path map

```
io_uring ZC Rx
  -> net_iov refcount transitions (user_refs race domain)
  -> page_pool_refill() -> FILL ring
  -> CQE -> userspace advance refill tail

EEVDF / PREEMPT_LAZY
  -> pick_next_task_fair()
  -> vruntime min-heap / EEVDF eligibility check
  -> lazy resched: preempt_lazy flag not evaluated in softirq path

MGLRU reclaim
  -> mglru_lru_gen_scan()
     -> budget = compute_folio_budget()
     -> for each generation
        -> isolate candidate folios
        -> if dirty -> writeout() in-loop
        -> if clean -> try_to_unmap() + remove_mapping()
        -> update nr_scanned / nr_reclaimed
```

Key symbols:
- `kernel/sched/fair.c`: `pick_next_task_fair()`, `entity_eligible()`, `update_curr()` vruntime tick.
- `kernel/sched/ext.c`: `scx_dispatch()` / `scx_enqueue()` — `sched_ext` overrides.
- `mm/vmscan.c`: `mglru_lru_gen_scan()`, `shrink_folio_list()`.
- `net/core/page_pool_user.c`: ZC Rx user page pool and `net_iov` lifecycle.

---

## 6. Debug recipe for cross-layer stalls

1. Confirm EEVDF + PREEMPT_LAZY:
   ```
   grep PREEMPT /boot/config-$(uname -r)
   zcat /proc/config.gz | grep PREEMPT
   cat /sys/kernel/mm/lru_gen/enabled
   ```

2. Measure ZC Rx completion rate:
   ```c
   tracepoint:io_uring:io_uring_zcrx_complete
   {
       printf("area=%d off=%d cpu=%d\n", args->area_id, args->buf_off, cpu);
   }
   ```
   Watch for single-CPU saturation at >250k completions/s.

3. Watch scheduler preempt behavior:
   ```bash
   trace-cmd record -e sched:sched_switch -e sched:sched_waking
   ```
   Look for latency-sensitive tasks repeatedly appearing as `next_pid` but never actually running because current task stays on CPU.

4. Watch MGLRU reclaim:
   ```bash
   bpftrace -e 'tracepoint:mm_vmscan:mm_vmscan_direct_reclaim_begin { @[pid] = count(); }'
   ```
   High frequency + low reclaimed count ⇒ dirty flush still ineffective.

5. Observe dirty folio writeback latency:
   ```
   iostat -x 1
   cat /proc/vmstat | grep -E 'pgpgin|pgpgout|pgmajfault|workingset_refault'
   ```

---

## 7. Teaching module / lab exercise

1. Read `kernel/sched/fair.c` `entity_eligible()` and explain why PREEMPT_LAZY suppresses the EEVDF preempt check in the softirq path.
2. Run a single-threaded `io_uring` ZC Rx workload with `IORING_RECV_MULTISHOT` and measure per-task deadline misses via `trace-cmd record -e sched:sched_waking`; observe how inserting `sched_yield()` every N completions changes the miss rate.
3. Boot a kernel with the March 2026 MGLRU series; repeat step 2 under a 4GB memcg with a mixed WiredTiger + ZC Rx workload; show that the post-patch kernel no longer OOM’s while the pre-patch kernel does.
4. Reproduce the `niov->user_refs` race condition pattern in userspace with two threads sharing a refill ring; confirm double-return with KASAN or explicit invocations.

---

## 8. References

- LWN MGLRU reclaim loop fix (March 2026): https://lwn.net/Articles/1063468/
- LWN MGLRU reconsideration: https://lwn.net/Articles/1060967/
- Kernel docs MGLRU: `Documentation/mm/multigen_lru.rst`
- Kernel docs io_uring ZC Rx: `Documentation/networking/iou-zcrx.html`
- Penligent CVE-2026-43121: https://www.penligent.ai/hackinglabs/io_uring-zcrx-freelist-race-four-bytes-past-the-edge/
- ArXiv UFS eBPF scheduler (May 2026): https://arxiv.org/abs/2605.02377
- EEVDF docs (7.1.0-rc6): https://docs.kernel.org/scheduler/sched-eevdf.html
- io_uring ZC Rx kernel docs: https://docs.kernel.org/networking/iou-zcrx.html
- Existing related skills: `ebpf-sched-ext-internals`, `linux-mglru-reclaim-loop-internals`, `af-xdp-and-io-uring-zcrx-internals`
