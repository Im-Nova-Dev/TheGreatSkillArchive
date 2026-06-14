---
name: linux-sched-ext-dsq-scheduling-mechanics
description: Mechanistic teaching module on Linux sched_ext (SCX) Dispatch Queue scheduling mechanics. Covers ops.select_cpu/enqueue/dispatch, local vs global DSQ transitions, vtime accounting, BYPASS fallback, error recovery, and concurrency pitfalls for BPF schedulers in production. Targets OS students and kernel/performance engineers below "how to use" level.
---

# Linux sched_ext DSQ Scheduling Mechanics

## Core premise
`sched_ext` (SCX) is a new Linux scheduler class where scheduling decisions are implemented in eBPF programs. It replaced custom schedulers for many use cases starting in kernel 6.12 and matures through 7.x. Understanding it at the mechanistic level requires tracking each hook the kernel calls, the data structures it passes, and the feedback loops between tasks, CPUs, and DSQs.

## 1. Activation semantics
- When a BPF scheduler is loaded and registered, tasks marked `SCHED_EXT` transition to sched_ext.
- Tasks created before loading remain in fair class until they set `SCHED_EXT` or the scheduler activates.
- `SCX_OPS_SWITCH_PARTIAL`: if set, only `SCHED_EXT` tasks use sched_ext, leaving `SCHED_NORMAL`/`SCHED_BATCH`/`SCHED_IDLE` on fair class.
- Scheduler unloading automatically restores fair class; no reboot required.

## 2. Scheduling hooks
### `select_cpu()`
- **Signature:** `s32 select_cpu(struct task_struct *p, s32 prev_cpu, u64 wake_flags)`
- **Purpose:** return target CPU hint. Acceptable values are any online CPU.
- **Mechanistic behavior:** returning `-EINVAL` or an offline CPU causes kernel to override selection with default policy. On idle CPU, BPF can immediately dispatch into `SCX_DSQ_LOCAL` to avoid going through the global DSQ.
- **Default helper:** `scx_bpf_select_cpu_dfl()` performs topology-based selection, preferring `prev_cpu` if idle.

### `enqueue()`
- **Signature:** `void enqueue(struct task_struct *p, u64 enq_flags)`
- **Called after `select_cpu()` returns.**
- Dispatches into DSQs. Operation must be non-blocking.
- Immediate-mode flag `SCX_ENQ_IMMED`: dispatch bypasses normal DSQ and executes immediately if target CPU is ready.

### `dispatch()`
- **Signature:** `void dispatch(s32 cpu, struct task_struct *prev)`
- **Called when CPU needs a runnable task.**
- Typical pattern: drain a DSQ onto the CPU’s local DSQ via `scx_bpf_consume()`.
- If `prev` task is still runnable, BPF scheduler must re-enqueue it; otherwise kernel yields via fair class briefly.

### `running()` / `stopping()`
- `running(p)` is invoked when task begins execution. Used to advance virtual time and pricing.
- `stopping(p, runnable)` is invoked when task stops. Charges execution time. Default yield sets `p->scx.slice = 0`.

## 3. Dispatch Queue types and invariants
- `SCX_DSQ_LOCAL`: per-CPU. Fastest consume path. Tasks dispatched here become eligible immediately on that CPU.
- `SCX_DSQ_GLOBAL`: shared. Backing FIFO/priority queue for all CPUs.
- Custom DSQs: created with `scx_bpf_dsq_create()`; unlimited scalar IDs.
- **Built-in `SCX_DSQ_GLOBAL` cannot be used as priority queue.** You cannot call `scx_bpf_dispatch_vtime()` on it. Create a custom DSQ for vtime ordering.

## 4. vtime accounting (precise mechanism)
- Each task carries `p->scx.dsq_vtime`, representing its virtual runtime.
- Global monotonic `vtime_now` tracks system-wide progress. Commonly stored in a BPF map or global eBPF variable.
- When a task starts (`running()`), update: `if (vtime_before(vtime_now, p->scx.dsq_vtime)) vtime_now = p->scx.dsq_vtime`.
- **Concurrency note:** this update is racy across CPUs. The kernel accepts transient inaccuracies; do not depend on strict atomicity of `vtime_now`.
- When enqueuing with vtime: cap lag to one slice to prevent idling tasks from accumulating excessive credit.

## 5. Dispatch flow step by step
1. Wakeup path -> `select_cpu()` -> choose target CPU or delegate to `scx_bpf_select_cpu_dfl()`.
2. `enqueue()` -> dispatch into DSQ via `scx_bpf_dispatch()` or `scx_bpf_dispatch_vtime()`.
3. CPU executes from `SCX_DSQ_LOCAL` first; if empty, drains `SCX_DSQ_GLOBAL` or custom DSQ via `scx_bpf_consume()`.
4. If CPU finds no work after draining, kernel calls `ops.dispatch()` to allow BPF scheduler to inject tasks.
5. Tasks leaving CPU via `stopping()` may be re-enqueued by scheduler or returned to fair class briefly.

## 6. Bypass mode and fallback guarantees
- When BPF scheduler cannot satisfy CPU demand, kernel can enter **bypass** mode: tasks run under the fair class for a short duration.
- Controlled by `SCX_OPS_BYPASS_*` flags.
- `SCX_EV_BYPASS_DURATION` / `SCX_EV_BYPASS_DISPATCH` counters expose fallback volume in sysfs.
- Fallback protects the system from a stalled BPF scheduler. It is not an exception path for normal scheduling.

## 7. Error detection, recovery, and SysRq handling
- Errors: invalid CPU selection (tracked by `SCX_EV_SELECT_CPU_FALLBACK`), local DSQ to offline CPU (`SCX_EV_DISPATCH_LOCAL_DSQ_OFFLINE`), re-enqueue loops (`SCX_EV_REENQ_LOCAL_REPEAT`).
- Recovery:
  - `SysRq-S` unloads BPF scheduler.
  - Scheduler process death unloads it.
  - Stalled runnable tasks trigger automatic fallback.
  - `SysRq-D` triggers `sched_ext_dump` without stopping the scheduler for post-mortem analysis.

## 8. Concurrency model and caveats
- BPF programs execute within kernel scheduler context. Non-sleepable verifier constraints apply.
- BPF maps hold scheduler state. Updates from multiple CPUs to shared maps must assume no mutual exclusion beyond BPF per-CPU or RCU guarantees.
- `vtime_now` is a shared scalar updated from `running()`. Authors accept benign races; treat it as approximate.
- DSQ kernel code performs internal enqueue/dequeue; calling helpers incorrectly from BPF scheduler causes halting paths like `SCX_EV_REENQ_IMMED` counters climbing.

## 9. Class-specific BPF flags and kernel behavior
| Flag | Effect |
|------|--------|
| `SCX_OPS_SWITCH_PARTIAL` | Only `SCHED_EXT` tasks use sched_ext. |
| `SCX_OPS_ENQ_EXITING` | Skip `enqueue()` for exiting tasks; direct dispatch to local DSQ. |
| `SCX_OPS_ENQ_MIGRATION_DISABLED` | Treat `migration_disabled` tasks as local-only. |
| `SCX_OPS_ENQ_LAST` | Preserve currently running task until another is ready. |

Observe these flags in `ops->flags` when reading `events` or drgn state to understand bypass depth.

## 10. Debugging and observability
- Sysfs: `/sys/kernel/sched_ext/<scheduler>/events`
- Tracepoints: `sched_ext_dump` for errors.
- `scx_show_state.py` uses drgn to dump `ops`, enable_seq, bypass_depth, nr_rejected.
- `/proc/<pid>/sched` field `ext.enabled` shows whether a task is managed by sched_ext.
- High `SCX_EV_REENQ_LOCAL_REPEAT` indicates incorrect `SCX_ENQ_REENQ` usage inside `dispatch()`.
- Falling back to fair class spuriously often means enqueue rate exceeds DSQ drain rate, causing BYPASS spikes.

## 11. Teaching exercises
1. Implement a scheduler that always selects the first idle CPU via `select_cpu()` and dispatches to `SCX_DSQ_LOCAL`. Measure context switches under mixed latency/throughput workload.
2. Modify `scx_simple` to use a per-CPU custom DSQ rather than a global DSQ. Profile lock contention and cache misses.
3. Inject a spuriously failing `select_cpu()` and observe `SCX_EV_SELECT_CPU_FALLBACK`.
4. Intentionally create an `SCX_ENQ_REENQ` loop in `dispatch()` and watch `SCX_EV_REENQ_LOCAL_REPEAT` climb.
5. Compare vtime fairness against fair-CFS latency distribution under THP vs 4K pages.

## 12. Source file map
- Core scheduler: `kernel/sched/ext.c`, `kernel/sched/ext_hooks.c`
- Internal definitions: `kernel/sched/ext_internal.h`
- BPF common header: `tools/sched_ext/scx_common.bpf.h`
- Reference schedulers: `tools/sched_ext/*.bpf.c`
- Debug helper: `tools/sched_ext/scx_show_state.py`

## 13. Related intel
See `/home/nova/.hermes/intel/systems/sched-ext-bpf-scheduler-internals.md` for collected kernel-doc-level material and full example implementation walkthrough.

---

End of teaching skill.
