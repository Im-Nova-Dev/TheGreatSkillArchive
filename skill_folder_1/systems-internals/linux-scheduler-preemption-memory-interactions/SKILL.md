---
name: linux-scheduler-preemption-memory-interactions
description: Teach Linux scheduler preemption modes, especially PREEMPT_LAZY, and how memory subsystem choices like huge pages interact with user-space spinlocks to produce or eliminate regressions such as the Linux 7.0 PostgreSQL case.
---

# Linux Scheduler Preemption and Memory Subsystem Interactions

## Core topic
Linux scheduler preemption policies (`PREEMPT_NONE`, full/realtime preemption, `PREEMPT_LAZY`) and their mechanistic effect on user-space synchronization overhead, depending on page size and memory pressure.

## What is PREEMPT_LAZY?
- New default in Linux 7.0, designed to reduce preemption frequency.
- Preemption is deferred until one of:
  1. Time slice exhausted
  2. Task blocks explicitly
  3. Next scheduler tick
- Reduces context switch overhead, keeps CPUs in useful work longer.

## Scheduler comparison table
| Config | When it preempts | Typical use | Latency |
|--------|------------------|-------------|---------|
| PREEMPT_NONE | Slice end only | Throughput/server kernels | High worst case |
| Full/realtime preempt | On any higher-priority wakeup | Hard-RT / PREEMPT_RT | Low worst case |
| PREEMPT_LAZY | Slice end, block, or tick | Balanced server | Intermediate |

## Memory subsystem coupling
- Huge pages reduce TLB misses and page-fault overhead.
- Shorter critical sections mean less chance that a deferred preemption hits a spinlock holder.
- Without THPs, longer critical sections + more context switches = higher lock-hold preemption probability.

## Regression archetype
- PostgreSQL `BufferPool` spinlock hold time depends on:
  - Page size / TLB reach
  - NUMA balancing and THP collapse behavior
  - CPU frequency / memory latency asymmetry
- Kernel ABI additions such as time-slice extension are not automatic fixes; DB maintainers generally prefer userspace tunables.
- Fix may be memory config change (enable THPs) rather than scheduler revert.

## Observability
- `ftrace` to show preempt frequency.
- Perf/bpftrace to count user-space spin cycles.
- Benchmark with `pgbench` / custom spinlock benchmark across page-size and scheduler configs.

## Teaching exercises
- Compare `need_resched` counts on identical workload under `PREEMPT_NONE`, full, and lazy preemption kernels.
- Show how MM behavior shifts the regression severity surface for a given scheduler policy.
