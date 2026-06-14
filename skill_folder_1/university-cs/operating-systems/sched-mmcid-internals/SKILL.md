---
name: sched-mmcid-internals
description: >
  Teach Linux per-memory-map concurrency ID (MM CID / SCHED_MM_CID) internals at the
  mechanistic level: purpose, rseq exposure, bitmap-based ownership, ownership
  modes, mode-switch mechanics, and the Linux 6.19 rewrite regressions.
  Covers root-cause analysis of CVE-2025-39780, the MMCID bitmap rewrite
  (Thomas Gleixner V3 20-patch series), mode-switch boundary costs, memory-ordering
  issues on weakly ordered architectures, and sched_ext interaction.
  Targets kernel developers, performance engineers, and advanced systems programmers
  who need to read kernel/sched/mmcid.c, trace events, or reason about thread-pool
  scheduling overhead and BPF-scheduler live-locks.
trigger: >
  questions about MM CID, SCHED_MM_CID, sched_ext class switching, per-memory-map
  concurrency IDs, Linux 6.19 scheduler regressions, CVE-2025-39780, mm_cid bitmap,
  rseq concurrency IDs, sched_ext task state transitions, scheduler ownership modes,
  or kernel hotplug selftest scheduler warnings.
---

# Scheduler MM CID Internals

## Scope
Mechanistic treatment of the Linux kernel's per-memory-map concurrency ID subsystem
(`SCHED_MM_CID`), from its purpose and userspace exposure through the internal ownership
protocols, the 6.19 bitmap rewrite, and the downstream regressions observed in the
field. Not a usage guide — covers data structures, invariants, concurrency
constraints, and failure paths that let you read and debug `kernel/sched/` and
`kernel/sched/ext.c`.

## Prerequisites
- `rseq` basics: per-thread registration, abi, and restart sequences.
- Scheduler class switching (`normal`, `idle`, `deadline`, `ext`).
- CFS/sched_entity flow.
- Concurrency primitives: `seqcount`, `mutex`, IRQ work, per-CPU variables.
- Thread-pool scheduling patterns and `clone()` / `CLONE_THREAD` copy-on-write mm.

---

## Lesson 1: What MM CID is, and why it exists
The kernel exposes to userspace via `rseq` an array of per-CPU "concurrency IDs".
For a given memory map (`struct mm_struct`), a CID of `N` means that at least `N`
threads from that mm are concurrently running on different CPUs. This is the only
reliable kernel mechanism userspace has for deterministic, per-mm cross-CPU
affinity without syscalls on every migration.

### Visibility
- `struct rseq::rseq_cs` points to a TLS area where a userspace library records
  the current CPU + CID.
- `sched_setattr()` and `clone()` inherit the parent's mm; new threads in the same
  process share the same `mm_struct` and therefore coordinate through the same
  MMCID bitmap.

### Invariants
1. A thread may only report a CID >= 0 when it holds a valid CPU ownership slot.
2. The number of simultaneously valid CIDs for an `mm` cannot exceed `nr_cpu_ids`.
3. CID transitions are tied to scheduler class switches and `enqueue/dequeue`.

---

## Lesson 2: Original CID management — complexity that caused regressions
Before Linux 6.19 the CID ownership was tracked via:
- A linked list of `mm_cid` objects inside `struct mm_struct`.
- Per-task `task->mm_cid` pointer.
- Refcount-style acquisition/release at scheduler enqueue/dequeue.

### Why this was slow
- Each `enqueue_task` and `dequeue_task` had to traverse or update the linked list
  under a lock/mutex. That puts non-trivial instruction latency in the *hottest*
  scheduler path: one invoked millions of times per second on busy servers.
- Cache-line ping-pong: the list head was shared across all threads of an mm, so
  high-contention thread pools saw the mm_struct cache line bouncing between cores.

---

## Lesson 3: The 6.19 rewrite — bitmap ownership
Thomas Gleixner's V3 20-patch series replaced the linked list with a flat bitmap
plus per-CPU ownership records.

### Core data structures
```c
/* Simplified conceptual view */
struct mm_cid {
  unsigned long *bitmap;         /* nr_cpu_ids bits */
  unsigned long max_cid;
  /* per-CPU ownership array accessed via this_cpu_ptr */
};
```

- Bitmap length = `bitmap_size(nr_possible_cpus())`.
- Each bit = "does this CPU currently own a CID for this mm?"
- `max_cid` precomputed to bound loops.
- Ownership records shifted to per-CPU variables to eliminate cross-core cache-line
  traffic during enqueue/dequeue fastpaths.

### Key functions introduced / reworked
- `mm_cid_alloc()` — allocates/claims a CID for a task at enqueue time.
- `mm_cid_free()` — releases ownership at dequeue.
- `mm_cid_switch()` — deferred mode change when a thread crosses the mode-switch
  boundary (e.g. from `SCHED_NORMAL` to `sched_ext` or `SCHED_DEADLINE`).

---

## Lesson 4: Mode-switch boundaries and bitmap operation cost
The most important performance win was supposed to be reduced bitmap operations.
Instead, in certain workloads the rewrite inserted more:

### The thread-pool pattern that hit the regression
A pool configured to frequently cross mode-switch boundaries forces:
1. Release old bitmap ownership.
2. Acquire new ownership.
3. Update `rseq` user-visible state.

With a linked list, these were amortized through reference counting.
With the naive bitmap rewrite, each boundary crossing performs a `bitmap_weighted_or()`
on the full bitmap.

### The 6.19 urgent fix
- Cache `num_possible_cpus()` and use `cpumask_weighted_or()` to short-circuit when
  the union doesn't add any new bits.
- Reduce bitmap operations by ~30% on thread-pool mode-switch workloads.
- Move `cpu_relax()` out of `for()` loops to fix build failures when it's a macro
  (not a performance change, but a correctness + build change).

**Measurement tip**: `perf record -e cycles:k -e sched:sched_switch -a` plus
`perf script | grep mm_cid_` to count mode-switch bitmap invocations vs
enqueue pairings.

---

## Lesson 5: Memory ordering and weakly ordered architectures
The bitmap rewrite introduced an ownership mode transition protocol that assumed
strongly ordered memory (x86). On ARM, POWER, and RISC-V, the release/acquire
barriers around per-CPU bitmap updates were too weak under high scheduler tick
interrupts on the same core, causing a hard lock-up in production workloads.

### What the fix does
- Adds explicit `smp_wmb()` / `smp_rmb()` pairs around bitmap state transitions
  in `mm_cid_switch()`.
- Makes per-CPU ownership updates use `this_cpu_cmpxchg()` instead of
  `__this_cpu_write()` so the transition is atomic with respect to interrupts.

---

## Lesson 6: CVE-2025-39780 — sched_ext invalid task state transition
This CVE is distinct from the MMCID rewrite but interacts with it through scheduler
class switching.

### Trigger path
1. Thread calls `bpf()` to attach a `sched_ext` program.
2. `bpf_struct_ops_link_create()` initiates class switch from `SCHED_NORMAL` to `SCX`.
3. Inside `scx_enable()`, the code iterates tasks and calls `scx_enable_task()`.
4. `scx_enable_task()` uses `get_task_struct()` to skip dead tasks during setup,
   but *does not* skip them when actually switching the class in `switching_to_scx()`.

### Result
- A dead task (usage=0, already on its way to `PF_POSTED_DEATH`) is passed to
  `scx_set_task_state()`, which expects a valid `TASK_*` state and computes:
  `invalid state transition 0 -> 3`.
- `0` is typically `TASK_RUNNING` or `TASK_DEAD`; `3` is often `TASK_UNINTERRUPTIBLE`.
  The transition is illegal because dead tasks cannot be put to sleep.

### Reproduction
- `tools/testing/selftests/kernel/hotplug.sh` in a tight loop reliably triggers
  the warning on 6.12–6.17 rc2.

### Fix behavior
- Class switch code now skips tasks with `usage == 0` *before* changing their state,
  aligning the class-switch predicate with the setup predicate.

---

## Lesson 7: BPF CI live-lock and the scheduler hook surface
The 6.19 urgent patchset also fixed a BPF CI live-lock. The new deferred mode-change
path posted an IRQ work item that conflicted with `sched_clock()`-based tracepoints,
causing a circular wait on a per-CPU lock.

### Mechanistic explanation
1. Scheduler tick runs on CPU X with `rq->lock` held.
2. Tick handler triggers IRQ work for MMCID deferred mode switch.
3. IRQ work tries to acquire the same CPU's `rq->lock` to update the bitmap.
4. `rq->lock` cannot be released until the tick finishes, but tick cannot finish
   until IRQ work fires.
5. BPF tracepoints attached to `sched:sched_switch` made this observable in CI
   because BPF programs are allowed to sleep on `bpf_probe_read()`.

### The fix
- Make MMCID deferred mode changes self-immune to scheduler tick by deferring IRQ
  work posting until after the lock is released (`post_schedule` hook).

---

## Lesson 8: Relationship between MM CID and sched_ext
`sched_ext` BPF schedulers interact with MMCID through:
1. `scx_enable()` / `scx_disable()` — mode switch triggers bitmap acquire/release.
2. `scx_set_task_state()` — operates on the same task state machine NORMAL/DEADLINE
   schedulers use; correctness requires skipping dead tasks just like CFS.

### sched_ext + MM CID invariant
- If a `sched_ext` scheduler migrates a task across CPUs, the old CID must be freed
  *before* the new one is acquired, otherwise the mm's bitmap will show a false
  "duplicate CID" state and userspace `rseq` readers will see a bogus count.

---

## Lesson 9: Debugging and introspection
### Reading MMCID state from a live kernel
```c
#include <linux/sched.h>
#include <linux/mm.h>

/* gdb / crash: */
p ((struct mm_struct *)0xADDR)->mm_cid
```

### bpftrace for mode switches
```bpftrace
tracepoint:sched:sched_switch
/comm == "sched_ext" || comm == "sched_deadline"/
{
  @switches[args->next_comm] = count();
}
```

### Perf / sched
```
perf top -e sched:sched_switch
perf record -e sched:sched_switch -ag -- sleep 3
perf script | c++filt | grep mm_cid
```

### Reproducing CVE-2025-39780 on a test kernel
```bash
git checkout v6.17-rc2
tools/testing/selftests/kernel/hotplug.sh &
while kill -0 $! 2>/dev/null; do sleep 1; done
# look for:
# sched_ext: Invalid task state transition 0 -> 3 for <task>
```

---

## Lesson 10: Exercises / thought problems
1. **Bitmap math**: On a 256-CPU machine, compute the cache line footprint of the
   original linked-list approach vs the bitmap approach. Assume `sizeof(list_head) = 16`,
   `cache_line_size = 64`, and a thread pool of 64 threads all sharing the same mm.
2. **Mode switch cost**: Write an `eBPF` program that counts `mm_cid_switch()` calls
   per second on your laptop under a high-concurrency server workload. Compare counts
   before and after `sched_setattr(..., SCHED_DEADLINE, ...)` on the same thread.
3. **Memory ordering**: Draw the `smp_wmb()` placement in `mm_cid_switch()` required
   to prevent the weakly-ordered lock-up. Why is `smp_rmb()` unnecessary on the
   consumer side?
4. **CVE fix reasoning**: Given the call-trace in CVE-2025-39780, explain why moving
   the dead-task check into `switching_to_scx()` is insufficient. Where else in the
   class transition path must the skip occur?
5. **Performance regression design**: Design a microbenchmark that demonstrates the
   ~30% bitmap operation reduction claimed by patch `47ee94efc`. What IO_uring or
   thread-pool primitives would you use, and which perf counters distinguish bitmap
   ops from enqueue/dequeue?

---

## References
- LWN.net, "[patch V3 00/20] sched: Rewrite MM CID management" (Thomas Gleixner, Oct 2025)
  https://lwn.net/Articles/1044027/
- Phoronix, "Linux 6.19 Sees Last Minute Scheduler Regression Fixes" (Feb 2026)
  https://www.phoronix.com/news/Linux-6.19-Scheduler-Fixes-Last
- NVD, CVE-2025-39780: sched/ext invalid task state transition
  https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2025-39780
- kernel.org git:
  - 4463c7aa11a6e67169ae48c6804968960c4bffea
  - 47ee94efccf6732e4ef1a815c451aacaf1464757
  - 4327fb13fa47770183c4850c35382c30ba5f939d
- `Documentation/admin-guide/hw-vuln/core-scheduling.html`
- `arch/x86/include/asm/processor.h` — `this_cpu_*` primitives
- `kernel/sched/ext.c` — `scx_enable_task()`, `switching_to_scx()`
