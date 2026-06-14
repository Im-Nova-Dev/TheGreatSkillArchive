---
name: ebpf-sched-ext-internals
description: Teach Linux eBPF schedulable class (`sched_ext`) internals, including ops callbacks, enqueue/dequeue mechanics, priority inversion mitigation via BPF maps, and how to prototype schedulers without kernel patches.
triggers:
  - scheduler internals
  - scheduling class
  - sched_ext
  - eBPF scheduler
  - EEVDF internals
  - kernel scheduling
  - CPU scheduler
  - BPF inference
  - sched_class
---

# eBPF `sched_ext` Internals

## Quick positioning
`sched_ext` is the Linux kernel's pluggable scheduling class. It lets you load a BPF ELF that implements the callbacks the kernel invokes synchronously during the schedule path (`kernel/sched/ext.c`). You do not need to patch the kernel or reboot; `sched_ext` is a loadable module (CONFIG_SCHED_CLASS_EXT=y).

## Core mechanism: `sched_ext_class` in the schedule path

### Class ordering and dispatch
The kernel scheduler calls `p->sched_class->next` when the current task exhausts its quantum or blocks. By installing `sched_ext_class` as `ext_sched_class` above `fair_sched_class`, ext callbacks get invoked before the CFS/EEVDF logic is asked to pick a task.

```
p->sched_class = &ext_sched_class
p->sched_class->next = &fair_sched_class
p->sched_class->prev = ???  // depends on boot order
```

When a task wakes, `check_preempt_wakeup` compares it against the current task using the `ops->yield`-style prediction and `ops->dispatch`.

### Required ops
In ELF section `.bss.sched_ext_ops` you define a `struct sched_ext_ops`. Minimal viable ops:

| op | when called | contract |
|---|---|---|
| `enqueue` | task transitions to TASK_RUNNING | place task on a run-queue or internal queue |
| `dequeue` | task stops being runnable | remove from run-queue |
| `dispatch` (runnable selector) | `schedule` needs `next` | return task to run on this CPU |
| `yield` | task calls `sched_yield()` | move it behind peers |
| `set_cpus` | cpuset/cpus allowed changes | obey or ignore; ext *must* respect if possible |
| `cpuset_change` | task moves cgroup/cpuset | adjust placement |

Return semantics: `dispatch` returning `NULL` falls through to `fair_sched_class` (CFS). `dequeue` returning 0 means success; nonzero skips subsequent ops.

### Memory and locking constraints
- All ops run in RCU read-side critical section for wakeup paths; `dispatch` may run with `rq->lock` held.
- Sleeping or taking mutexes in ops is prohibited; it deadlocks the scheduler core.
- Must not call `schedule()` or `cond_resched()`. Long computations stall the entire CPU.

## Mechanistic trick: direct-to-CPU placement
Most vanilla schedulers allow the kernel to place a wakee on any permitted CPU. `sched_ext` lets you internalize placement by storing target CPU in a per-task structure or eBPF map before calling `bpfbpf_task_enqueue`.

```python
# Pseudo-code in BPF/C
static int enqueue(struct bpf_cpumask *__cpu_mask, u64 *__cpu) {
    u32 tid = bpf_get_current_pid_tgid() >> 32;
    u32 cpu = map_lookup_cpu_target(tid);
    if (cpu)
        __cpu = cpu;
    return 0;  // actual enqueue implementation hidden
}
```

This is the fix for the EEVDF idle-sibling scan failure: break the "look for an idle sibling" heuristic by denying the kernel permission to choose.

## Application-level hinting (measured pattern)

### Contract
Userspace writes into BPF map keyed by `pid` (or inode of its cgroup). The scheduler reads on wakeup and selects tier.

```
map: { pid -> { tier: TIME_SENSITIVE|BACKGROUND, involved_futex_lock: u64 } }
```

When `tier == TIME_SENSITIVE`, scheduler:
1. Direct-enqueues onto target CPU.
2. Preempts any background task running there.
3. If that background task holds a lock the time-sensitive task waits on, the detection path is enhanced by recording the lock wait in another map that the kernel can read on context switch.

### FIFO vs EEVDF vs ext
- SCHED_FIFO: no time accounting → CPU-bound equal-priority starves bursty.
- EEVDF: good per-task deadlines but poor *initial placement* under bursty wakeup storms.
- UFS extends EEVDF while overriding the placement algorithm; does not replace the `vruntime` logic.

## Priority inversion mitigation (in-kernel)

### Why it exists in DBMS
PostgreSQL uses spinlocks and lightweight locks in shared buffers/walwrite; a background task can hold these while a foreground transaction waits. Under normal scheduling, the background task is not boosted automatically.

### How `sched_ext` fixes it
- On mutex/futex wait, userspace records `{waiting_tid, lock_addr}` into a map.
- The scheduler, when choosing to preempt the lock holder, observes the map entry. If preempting would block a higher-tier task, it either:
  - defers preemption until the lock is released, or
  - boosts the holder to time-sensitive tier until release.

This is implemented as a BPF map lookup inside `dispatch`; zero-copy shared memory with userspace.

## Verification: how to observe behavior

### bpftool introspection
```bash
bpftool prog show -t
# name, id, type, btf, pinned, cflags
bpftool map dump
# inspect your priority map
bpftool net show
# does not show ext scheduler state yet; check /sys/fs/bpf/sched if pinned
```

### ftrace and tracepoints
```bash
trace-cmd record -e sched:sched_waking -e sched:sched_switch
# Waking: pid, target_cpu, wakee
# Switch: prev_pid, next_pid, prev_state, target_cpu
```

Bootstrap and detect preemption chains that match UFS policy.

### perf and bpftrace one-liners
```bash
# count times a task was preempted while running on a CPU other than its base/pinned CPU
perf stat -e 'sched:sched_switch' -a
```

### Load testing pattern
Use `pgbench` with mixed tpmc+cpu_bound background analytics. Measure tail latency at 99.9th percentile under EEVDF vs UFS by pinning `postmaster` cgroup and watching `sched:sched_waking` rate per CPU.

## Failure vectors when writing a `sched_ext` scheduler
- Returning `NULL` from `dispatch` repeatedly causes every task to fall through to CFS → the ext class becomes a no-op by mistake.
- Calling `bpf_probe_read` with large structs inside ops: O(n) is fine, but O(n log n) per wakeup can regress the whole system because wake rates run in the thousands/sec per core.
- Not honoring `cpuset.cpus`: tasks may be pinned to offline CPUs under cpuset hot-unplug if you don't listen to `cpuset_change`.
- `set_cpus` returning `-EINVAL` or ignoring when userspace restricts cpuset: results in migratetype bugs in the memory scheduler (ILM).

## Relationship to `cpuset`, `cgroup.cpu`, and `sched_setattr`
- `sched_ext` runs above the cgroup weight layer; `cpu.weight` can be combined with ext placement but `cpu.max` is still enforced by throttle_unthrottle.
- `SCHED_DEADLINE`/`SCHED_FIFO` still beat ext tasks because SCHED_NORMAL is the only policy `sched_ext` replaces; rt policy is higher in the class order.

## Suggested lab exercise
1. Boot a kernel with `CONFIG_SCHED_CLASS_EXT=y` and `CONFIG_DEBUG_FS=y`.
2. Write a minimal BPF `sched_ext` that pins every runnable thread to the lowest-numbered permitted CPU.
3. Measure per-CPU run-queue lengths with `cat /proc/sched_debug` before and after.
4. Add a two-tier priority map and reproduce the throughput/latency split for mixed pgbench workloads.

## Key reading
- David Vernet's `sched_ext` talk (Linux Plumbers 2023, 2024) on ops callbacks and locking contracts.
- Kernel internals: `kernel/sched/ext.c`, `kernel/sched/sched.h`, `kernel/sched/fair.c` EEVDF admission test.
- The UFS paper measurement methodology for mixed database workloads.
- INTEL: /home/nova/.hermes/intel/systems/2026-06-06-ebpf-sched-ext-extensible-scheduler.md (this run)
- Kernel docs: https://docs.kernel.org/scheduler/sched-ext.html
