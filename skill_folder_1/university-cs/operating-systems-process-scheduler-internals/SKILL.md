---
name: operating-systems-process-scheduler-internals
description: Teach modern Linux CPU scheduler internals including CFS assumptions, EEVDF behavior, sched_ext/eBPF schedulers, and how kernel algorithms map to latency/throughput outcomes.
---

# Operating Systems: Linux Process Scheduler Internals

## Scope
Go beyond "process scheduling overview" into mechanistic understanding of CFS→EEVDF evolution, sched_ext hooks, and how scheduler data structures affect latency and throughput.

---

## 1. From CFS to EEVDF: What changed

### CFS core model
- Single runqueue per logical CPU.
- Red-black tree ordered by `vruntime`.
- Pick leftmost task → task with minimum vruntime.
- `vruntime` advances proportionally to real time and inversely to task weight.
- Heuristics: `sched_latency`, `sched_min_granularity`, `sched_wakeup_granularity`.

### Failure modes of CFS
- **No urgency concept:** shortest vruntime may correspond to a batch job that just slept, while an urgent task waits.
- **Latency-sensitive heuristics** were ad-hoc (e.g., wakeup preemption based on delta-vruntime and thresholds).
- **Complexity grew** as heuristics tuned for webservers, desktop, mobile, and HPC each ran best under different parameters.

---

## 2. EEVDF formal semantics

### Eligibility
A task is eligible when its share of CPU time consumed up to current global virtual time does not exceed its fair allocation. Expressed via per-cfs_rq weighted average vruntime.

### Virtual Deadline
```text
deadline = vruntime + calc_delta_fair(requested_slice, weight)
```
Tasks with shorter requests receive earlier deadlines → latency-sensitive work wins.

### Preemption
Any running task can be preempted immediately on arrival of an eligible task with earlier deadline.

### vlag management
Prevents starvation of sleeping tasks and prevents burst on wake. Dynamically initializes vruntime on enqueue.

### Tree selection (`__pick_eevdf`)
Walk rbtree with subtree min-deadline pruning to find eligible task with smallest deadline.

### Interaction with nice/cgroup weight
`calc_delta_fair` converts slice into virtual time using inverse task weight. Higher weight = slower vruntime progression = earlier deadline for same real-time interval.

| Feature | CFS | EEVDF |
|--------|-----|-------|
| Policy key | min vruntime | min deadline among eligible |
| Latency control | heuristics | explicit via slice / deadline |
| Sleeping task accounting | implicit | explicit vlag |
| Preemption trigger | delta threshold | earlier deadline |

---

## 3. sched_ext: eBPF-driven scheduler class

### Motivation
Custom scheduling policies for specific workloads without kernel patching. Examples: database mixed-workload isolation, GPU-heavy k8s pods, cgroup-scoped policies.

### Kernel hooks
- `BPF_STRUCT_OPS(select_cpu)`: preferred CPU on wakeup.
- `BPF_STRUCT_OPS(enqueue)`: place task in DSQ(s).
- `BPF_STRUCT_OPS(dispatch)`: choose task for this CPU.
- `BPF_STRUCT_OPS(running/stopping)`: for vruntime/vtime tracking.
- `dispatch_from_dsq`, `yield`.

### DSQ model
Dispatch queues organize queued tasks:
- Local DSQ: tasks running on this CPU.
- Global DSQ: shared across CPUs.
- Dispatch uses `scx_bpf_dispatch` and `scx_bpf_consume`.

### Fallback and safety
If BPF program faults or returns error, kernel gracefully falls back to CFS/EEVDF. SysRq + `sched_ext_dump` tracepoint provides debugging visibility.

### Latency trap
A common mistake: using a long slice for latency-sensitive tasks in sched_ext. This delays their virtual deadline relative to competing tasks and inflates tail latency. For databases, split transaction work into small chunks and hand those to the scheduler.

---

## 4. Mechanistic teaching approach

### Trace a context switch
1. CPU receives interrupt / timer.
2. `scheduler_tick()` runs current task accounting.
3. If running task is `sched_ext`, call its `stopping` hook to update slice/deadline accounting.
4. `pick_next_task()` walks scheduler classes in priority order: STOP → DL → RT → FAIR → IDLE.
5. FAIR runs `pick_next_entity()` → EEVDF path selects earliest eligible virtual deadline.
6. Task returns to user-space with updated vruntime and slice.

### Conflict map: where EEVDF can degrade latency
1. **WRRK (weighted runqueue) skew** when cgroup weights shift during heavy concurrency.
2. **NUMA-balancing interference** because load-balancing is orthogonal to EEVDF selection.
3. **Preemption-RT lock inversion** in core scheduler path when priority inheritance collides with per-task vruntime updates.

---

## 5. Exercises

1. Draw the CFS runqueue tree before and after a 5 ms nice-0 task sleeps 200 ms and wakes up. Show vruntime positions under CFS vs EEVDF with explicit `deadline` annotations.
2. For EEVDF, write pseudocode for `__pick_eevdf` with subtree pruning. Argue its O(log n) property.
3. Implement a tracing eBPF program that samples `p->se.deadline`, `vruntime`, and task weight for the currently running task and prints them.
4. In sched_ext, design a minimal FIFO scheduler that dispatches IDs in order. Identify how to respect `sched_setscheduler` calls from user-space applications.
5. Simulate: with two tasks A (nice 0, slice 1 ms) and B (nice 10, slice 10 ms), both running on one CPU, calculate relative deadline values and determine which runs first under EEVDF.
