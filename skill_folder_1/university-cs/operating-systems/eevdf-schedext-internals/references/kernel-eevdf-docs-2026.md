# EEVDF Kernel Documentation Notes
Source: https://docs.kernel.org/scheduler/sched-eevdf.html (7.1.0-rc6)

## Core Overview
- Full name: Earliest Eligible Virtual Deadline First (EEVDF)
- First introduced in 1995 scientific publication
- Linux adoption: transitioned to EEVDF in 6.6 (2024), replacing CFS for normal scheduling classes
- Implementation basis: Peter Zijlstra 2023 proposal

## Core Scheduling Logic
1. Each task assigned a virtual run time (VRT)
2. Calculate lag: `lag = vruntime - ideal_vruntime`
   - Positive: task is owed CPU
   - Negative: task exceeded allocation
3. Task selection:
   - Filter: `lag >= 0` (eligible)
   - Compute virtual deadline (VD): `vruntime + requested_time_slice`
   - Select task with earliest VD

## Lag Management for Sleeping Tasks
- Current implementation uses VRT-based "decaying" lag
- Tasks on runqueue marked for deferred dequeue
- Lag decays gradually over VRT while deferred
- Prevents brief sleeps from resetting negative lag

## Advanced Features
- Preemption: tasks can preempt if VD earlier than running task's VD
- Time slice control: applications can request specific slices via `sched_setattr()`
