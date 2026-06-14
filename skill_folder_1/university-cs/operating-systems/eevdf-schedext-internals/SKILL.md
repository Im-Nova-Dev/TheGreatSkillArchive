1|---
2|name: eevdf-schedext-internals
3|description: >-
4|  Teach Linux EEVDF scheduler internals at the mechanistic level: virtual run time (VRT),
5|  lag, eligible filtering by lag >= 0, virtual deadline computation, deferred dequeue
6|  for sleeping tasks, and how these concepts map to observable scheduling behavior.
7|  Includes reference to sched_setattr(), scheduler debugging via bpftrace/perf, and
8|  distinction between EEVDF and legacy CFS/SCHED_DEADLINE. Targets kernel developers,
9|  performance engineers, and advanced systems programmers who need to read scheduler
10|  code and trace events.
11|trigger: >-
12|  questions about EEVDF scheduler internals, EEVDF vs CFS, virtual deadline scheduling,
13|  VRT/lag mechanics, sched_setattr(), Linux 6.6+ scheduler debugging, latency-sensitive
14|  Linux scheduling, or scheduler tracepoints.
15|---
16|
17|# EEVDF Scheduler Internals
18|
19|## Scope
20|Mechanistic how-it-works of Linux's default CPU scheduler from 6.6+ (EEVDF). Not a
21|high-level overview — covers the data structures, invariants, concurrency constraints,
22|and debugging interfaces that let you reason about *why* a specific task ran (or did not)
23|at a specific moment.
24|
25|## Prerequisites
26|- CFS familiarity: `struct sched_entity`, `struct cfs_rq`, vruntime.
27|- `sched_setattr()` and scheduling policy constants (`SCHED_NORMAL`, `SCHED_BATCH`,
28|  `SCHED_IDLE`, `SCHED_DEADLINE`).
29|- Linux kernel locking basics: `rq_lock()`, `task_rq_lock()`, seqlock usage for
30|  `load_balance()` / `nr_migrations`.
31|- `bpftrace` or `perf sched` event names.
32|
33|## Lesson 1: What changed from CFS
34|CFS picked the leftmost task in a red-black tree sorted by vruntime. EEVDF adds one
35|predicate before tree-walk:
36|
37|1. **Eligibility filter**: only tasks with `lag >= 0` are eligible. Lag = `vruntime - ideal_vruntime`; positive lag means the task is owed CPU. Sleeping tasks are still on the tree but marked `deferred_dequeue` if their lag was negative when they went to sleep.
38|2. **Virtual deadline (VD)**: each eligible task computes `vd = vruntime + requested_time_slice`. EEVDF selects the task with the *earliest* VD among eligible tasks.
39|
40|Result: latency-sensitive tasks requesting short slices naturally run before burn tasks,
41|without explicit priority.
42|
43|### Invariants
44|- `vruntime` never decreases for a given task (monotonicity).
45|- `ideal_vruntime` tracks the average vruntime of all runnable tasks on the rq.
46|- `lag = se->vruntime - ideal_vruntime` is meaningful even when the task is not on
47|  the CPU.
48|
49|## Lesson 2: Virtual runtime and time slice math
50|- Normalized vruntime: `se->vruntime = calc_delta_fair(delta, se)`.
51|  - `calc_delta_fair()` divides wall-clock delta by `se->load.weight` (NICE_0_LOAD / nice_weight).
52|- Requested time slice (`slice`) can be set via `sched_setattr({ .sched_rr = 1, .sched_rr_period = ..., .sched_rr_runtime = ... })` for SCHED_RR, but for SCHED_NORMAL / SCHED_BATCH the scheduler derives slice from `sched_nr_migrate_{low,high}` and task weight.
53|- Virtual deadline = `vruntime + slice`. A task requesting a 1 ms slice will have a
54|  tighter VD than a task requesting 200 ms slice, *all else equal*.
55|
56|### Experiment with bpftrace
57|```bpftrace
58|tracepoint:sched:sched_switch
59|/args->prev_prio != args->next_prio/
60|{
61|  printf("prev=%s (prio=%d vruntime=%llu) -> next=%s (prio=%d vruntime=%llu)\n",
62|    args->prev_comm, args->prev_prio, args->prev_vruntime,
63|    args->next_comm, args->next_prio, args->next_vruntime);
64|}
65|```
66|
67|## Lesson 3: Deferred dequeue and lag decay for sleeping tasks
68|When a task goes to sleep with `lag < 0` (it ran too long already):
69|
70|1. It is left on the red-black tree.
71|2. A flag `deferred_dequeue` is set on the `sched_entity`.
72|3. On the next enqueue (wakeup), the scheduler evaluates whether to dequeue a
73|   deferred-dequeue task first based on its lag and the new ideal vruntime.
74|
75|Current implementation (7.1-rc6) uses *VRT-based decay*:
76|- While sleeping, the task's `vruntime` stops advancing.
77|- When work is enqueued, the scheduler computes a decay factor and "renews" the
78|  sleeping task's lag so it does not remain deeply negative forever.
79|
80|This is the tradeoff at the heart of ongoing discussion:
81|- Decay is a feedback mechanism to allow cpu-bound tasks to "pay back" their excess
82|  without newly waking tasks starving the system.
83|- If decay is too slow, cpu-bound tasks accumulate negative lag and get brief cpu
84|  bursts on every wake event.
85|
86|## Lesson 4: Preemption and virtual deadline comparison
87|A running task can be preempted if a newly enqueued task has an earlier VD:
88|
89|```c
90|if (dl_se->vd < curr->se.vd)
91|    resched_task(rq->curr);
92|```
93|
94|Key point: this is a *soft* deadline comparison, not a hard deadline, because
95|`vruntime` of the running task advances in real time. The running task's VD is
96|recomputed on every `update_curr()` tick. This means the preemption check is
97|re-evaluated periodically.
98|
99|## Lesson 5: Debugging and introspection
100|- `perf sched record` + `perf sched latency` — shows task sleep/wakeup latencies and
101|  migration counts.
102|- Tracepoint `sched:sched_switch` gives prev/next vruntime.
103|- `sched_debug` sysctl dumps CFS and EEVDF runqueues when a stall is detected.
104|- `bpftrace` attachment to `sched:sched_wakeup` and `sched:sched_waking` can reveal
105|  wakeup chains and migrations.
106|
107|### Detecting deferred-dequeue tasks
108|```bpftrace
109|tracepoint:sched:sched_wakeup
110|/args->flags & PF_DEAD || (args->flags & PF_WQ_WORKER && args->prio < 100)/
111|{
112|  @deferred[(int)args->pid] = count();
113|}
114|```
115|
116|In practice you want to correlate `sched_waking` with vruntime in `sched_switch`.
117|
118|## Lesson 6: Relationship to SCHED_DEADLINE
119|SCHED_DEADLINE and EEVDF both use deadline concepts but at different layers:
120|
121|| Dimension | EEVDF (SCHED_NORMAL/BATCH) | SCHED_DEADLINE |
122||-----------|----------------------------|-----------------|
123|| Deadline semantics | Soft; tasks can miss VD | Hard; admission-controlled |
124|| Admission control | None | `dl_overflow()` checks utilization |
125|| Runtime enforcement | No | `dl_runtime` budget enforced |
126|| Recovery | Lag decay for sleeping tasks | Throttled until next period |
127|| Use case | General-purpose latency | Real-time audio, robotics |
128|
129|If an application needs hard deadlines it must use `SCHED_DEADLINE`, not EEVDF.
130|
131|## Lesson 7: sched_setattr() tunable knobs
132|```c
133|struct sched_attr {
134|    uint32_t size;
135|    uint32_t sched_policy;
136|    uint64_t sched_flags;
137|    int32_t  sched_nice;
138|    uint32_t sched_priority;
139|    uint64_t sched_runtime;
140|    uint64_t sched_deadline;
141|    uint64_t sched_period;
142|};
143|```
144|
145|Relevant flags for latency tuning:
146|- `SCHED_FLAG_KEEP_POLICY` / `SCHED_FLAG_KEEP_PARAMS`
147|- `SCHED_FLAG_UTIL_CLAMP` for `uclamp_*` (used by EEVDF to bias task placement)
148|- `SCHED_FLAG_RECLAIM` for deadline reclaim (interaction with deadline server)
149|- `sched_period` + `sched_runtime` only matter for SCHED_DEADLINE; they are ignored
150|  in SCHED_NORMAL but turning on `SCHED_FLAG_DL_OVERRUN` enables the overrun handler
151|  that can raise `sched_nice` dynamically.
152|
153|## Lesson 8: sched_ext recovery mechanics (Linux 6.19)
154|sched_ext is a separate scheduler class implemented in BPF. Kernel safety guarantees
155|require that a misbehaving BPF scheduler cannot hang the machine. Linux 6.19 hardened
156|this recovery path after lockups were reproduced with schedulers that placed tasks with
157|conflicting affinity onto a single shared DSQ.
158|
159|### Bypass mode and per-CPU DSQs
160|When the kernel detects that CPUs are scanning a shared DSQ looking for tasks they
161|cannot run (due to `task->nr_cpus_allowed` or cgroup affinity), it activates bypass
162|mode: each CPU gets a private per-CPU DSQ so scanning stops. A built-in load-balancer
163|then migrates tasks to CPUs that can actually run them.
164|
165|### Hardlockup detector integration
166|The scheduler hooks into the existing hardlockup detector. If a CPU stops making
167|forward progress in the scheduling path for >`CONFIG_HARDLOCKUP_DETECTOR_TIMEOUT`
168|seconds, recovery intervention is attempted:
169|1. Switch the offending CPU to its per-CPU bypass DSQ.
170|2. Dump scheduler state via the `sched_ext_dump` tracepoint (also reachable via
171|   SysRq-D).
172|3. If the task queue still appears stalled, trigger the standard fallback: abort the
173|   BPF scheduler and revert all tasks to the underlying fair scheduler (EEVDF).
174|
175|### Observable signals
176|- `/sys/kernel/sched_ext/<scheduler>/events` includes `SCX_EV_BYPASS_DURATION` and
177|  `SCX_EV_BYPASS_DISPATCH` counters. Rising `BYPASS_DURATION` on a multi-socket
178|  system is a strong indicator of affinity-heavy workloads under sched_ext.
179|- `SCX_EV_DISPATCH_LOCAL_DSQ_OFFLINE` counts times a local DSQ became unreachable
180|  because the target CPU went offline; sched_ext must then redirect to the global
181|  DSQ or a per-CPU DSQ on an online sibling.
182|
183|### Implication for custom BPF scheduler authors
184|Never create a DSQ that mixes tasks with heterogeneous CPU affinity. Either:
185|- Use separate DSQs keyed by `task->nr_cpus_allowed` mask, or
186|- Honor `SCX_OPS_SWITCH_PARTIAL` so only `SCHED_EXT` tasks enter your DSQ and you
187|  can control their placement without fighting the fair scheduler's affinity logic.
188|
189|### Distinction from EEVDF deferred-dequeue
190|- EEVDF deals with *temporal* unfairness via lag and vruntime.
191|- sched_ext recovery deals with *spatial* unfairness via DSQ selection and affinity
192|  scanning. A task that survives both layers may still be placed on a CPU at a
193|  different power/performance domain than EEVDF would choose, because sched_ext
194|  decides CPU assignment before EEVDF computes slice/VD.
195|
196|+## Lesson 9: NEXT_BUDDY reintroduction and performance regression (Linux 6.19)
197|+
198|+NEXT_BUDDY was re-enabled in Linux 6.19 by commit `e837456fdca8` ("sched/fair:
199|+Reimplement NEXT_BUDDY to align with EEVDF goals") after being originally disabled
200|+when EEVDF replaced CFS. It was promptly disabled by default in `tip/tip.git
201|+sched/urgent` (commit `4f70f106bca1a56bd66d00830ac91680bd754974`) because it caused
202|+regressions in:
203|+
204|+- MySQL client/server on separate hosts — realistic production workload
205|+- SPECjbb — lower peak metrics; root cause unclear whether genuine drop or peak
206|+  measurement point shift
207|+- DayTrader — considered representative of real production workloads
208|+- Nginx HTTPS — early December 2025 bisect suspect
209|+
210|+The regression patch message explicitly notes the reimplementation was "not expected
211|+to be a universal win without a crystal ball instruction but the reported regressions
212|+are a concern even if gains were also reported."
213|+
214|+### Mechanistic explanation
215|+
216|+NEXT_BUDDY records a precomputed candidate for the next wake-up preemption. Under
217|+EEVDF, this candidate must be chosen from the set of tasks with `lag >= 0` and
218|+earliest virtual deadline, not just minimum vruntime. The rewrite in commit
219|+`e837456fdca8` appears to have missed a placement interaction: when NEXT_BUDDY
220|+selects a candidate with a slightly later VD but much lower vruntime, EEVDF's
221|+enqueue path may assign a shorter effective slice to wakee tasks, causing the
222|+MySQL and Nginx regressions where wakeup-heavy client/server patterns dominate.
223|+
224|+### Disable path
225|+
226|+The fix sets a tunable knob so NEXT_BUDDY defaults to off while preserving the
227|+rewrite in the tree for future re-enablement after the candidate-selection path is
228|+fixed to account for EEVDF eligibility semantics. Production systems on 6.19 should
229|+confirm their kernel either carries the disable patch or has NEXT_BUDDY disabled via
230|+the relevant sysctl/kconfig knob.
231|+
232|+### Upstream references
233|+
234|+- Disabling patch: `4f70f106bca1a56bd66d00830ac91680bd754974` in `tip/tip.git sched/urgent`
235|+- Baseline reintroduction: `e837456fdca8`
236|+- Phoronix regression report: https://www.phoronix.com/review/linux-619-sched-regress
237|+- LWN release notes: https://lwn.net/Articles/1057667/
238|+
239|+### Exercise thought point
240|+
241|+When analyzing a scheduler regression, NEXT_BUDDY candidate selection interacts with
242|+EEVDF's `eligible_time` and `deadline` in ways that CFS vruntime-only selection did
243|+not. Why might a workload with frequent small wakeups (MySQL client polling) regress
244|+when NEXT_BUDDY is enabled, while a CPU-bound batch workload may still improve?
245|+
246| ## Exercises / thought problems
247| 1. Draw the timeline for two tasks: A runs 100 ms, sleep 50 ms, run 50 ms; B runs
248|   200 ms continuously. Assume both are SCHED_NORMAL, nice 0, slice 4 ms.
249|   Compute vruntime and lag for both after first 150 ms of wall time.
250| 2. Instrument a running kernel to dump `ideal_vruntime` and `nr_running` on each
251|   `sched_switch`. Plot lag history for a CPU-bound workload vs an interactive shell
252|   workload. What does EEVDF's deferred-dequeue path do when the interactive task
253|   wakes after a 30-second sleep?
254| 3. Design a `bpftrace` script that alerts if any task on a given CPU has `lag < -100ms`
255|   (normalized vruntime) for more than 10 ms wall-clock time. Discuss false-positive
256|   scenarios.
257| 4. On a hybrid Intel system, measure P-core vs E-core `capacity_orig`. Explain why an
258|   E-core-bound SCHED_NORMAL task with nice=0 may have *lower observed throughput* than
259|   a P-core-bound task at the same nice value, even with identical slice and frequency.
260| 5. Given a misbehaving BPF scheduler that dispatches many GPU/compute tasks with
261|   `cpuset` restriction to a single global DSQ, simulate the per-CPU DSQ migration
262|   logic in bypass mode. Which `SCX_EV_*` counters increase, and how does the
263|   hardlockup detector decide to abort back to EEVDF?
264| 6. Why does `CONFIG_SCHED_CLASS_EXT` place sched_ext between `SCHED_IDLE` and
265|   `SCHED_NORMAL` in the scheduling-class priority chain? What would happen if
266|   sched_ext had higher priority than fair scheduling?
