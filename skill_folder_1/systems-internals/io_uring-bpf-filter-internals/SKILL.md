---
name: io_uring-bpf-filter-internals
description: Mechanistic internals of the io_uring BPF filter patchset merged in Linux 7.0/7.1: cBPF/struct_ops attachment, SQE submission filtering, IOU_LOOP_CONTINUE/IOU_LOOP_STOP semantics, registered-buffer kfunc gaps, fork-inheritance rules, and the cancellation/cleanup contract. Complements bpf-io_uring-event-loop-mechanics with a focus on the filter design, security surface, and performance inflection points.
---

# io_uring BPF Filter Internals (Linux 7.0/7.1)

Use this skill when the task requires mechanistic explanation beyond "how to use BPF with io_uring". Focus: what the filter is, where it runs, what state it observes, and what invariants the kernel enforces (or does not).

## Trigger Conditions
- Discussion of Linux 7.0 io_uring BPF support, `IORING_SETUP_ATTACH_BPF`, or `bpf_io_uring_*` kfuncs.
- Need to reason about fork-inherited filters, cBPF program lifetime, or SQE filtering in containers.
- Debugging a performance regression or security boundary involving io_uring + BPF.

## 1. What is the io_uring BPF filter?

Starting in Linux 7.0, an io_uring instance can have a cBPF struct_ops program attached to it. The program executes inside the kernel's io_uring event loop rather than in user space. This is not a classic packet-filter; it is an **operation filter and submission-loop driver** for the SQ/CQ rings.

Key structural point: the BPF program sees the shared SQ and CQ ring memory via `bpf_io_uring_get_region()`. It is not a separate abstraction layer; it literally operates on the same `io_uring_sqe` array and `io_uring_cqe` array that user space mmap'd.

## 2. Attachment and lifetime

- Attachment is to the io_uring instance fd (`struct io_ring_ctx`).
- Program is attached via `io_uring_register()` / BPF syscall path with a struct_ops BPF program type specific to io_uring.
- **Fork semantics:** the filter is inherited across `fork()`. Child inherits the parent's BPF program identity. If the child unregisters its own filter, the child no longer runs a filter, but the parent's instance is unaffected.
- Once a filter is installed on an instance, **only further restrictions** are allowed; the kernel prevents widening the allowed operation set. This guarantees monotonic policy tightening.

## 3. The execution model: a single io_uring_enter() runs the BPF loop

Normal path (no BPF):
```
io_uring_enter()
  -> io_submit_sqes()        // drain SQ, execute bound requests
  -> wait for completion
  -> return to user space
```

With BPF filter:
```
io_uring_enter()
  -> call BPF program instead of default event loop
  -> BPF program:
       bpf_io_uring_submit_sqes()
       process completions
       return IOU_LOOP_CONTINUE or IOU_LOOP_STOP
```

This turns one system call into an in-kernel event loop. In steady state, the process does not return to user space between batches.

## 4. kfuncs surface

- `bpf_io_uring_get_region(ring_type)`: returns a KMappable region handle for SQ or CQ traversal. Ring memory is shared with user space mmap.
- `bpf_io_uring_submit_sqes()`: inspects the SQ, executes bound requests. Returns number of processed SQEs, or negative `-EIO` on shutdown path.

**Invariants the BPF program must honor:**
- SQ tail must not move ahead of kernel due to active `io_uring_enter()` reentry. BPF should call `submit_sqes()` once per loop iteration.
- CQE consumption is implicit: new CQEs from earlier submits are visible after wait. BPF must re-check until it decides to stop.
- No blocking operations in BPF program.

## 5. Loop control semantics

| Return value | Kernel behavior |
|---------------|-----------------|
| `IOU_LOOP_CONTINUE` | Immediately re-run the BPF program |
| `IOU_LOOP_STOP` | Break out, return control to user space |

This is the re-entry primitive that eliminates syscall overhead. A typical pattern:
```c
int bpf_prog(void *ctx)
{
    int ret = bpf_io_uring_submit_sqes();
    if (ret < 0)
        return IOU_LOOP_STOP;
    if (all_work_done())
        return IOU_LOOP_STOP;
    return IOU_LOOP_CONTINUE;
}
```

## 6. Registered buffer kfuncs (Ming Lei series, converging in 7.1)

Users can pin reusable buffers with `io_uring_register_buf_ring()` to amortize pinning cost. The initial 7.0 BPF filter patchset **did not include kfuncs for accessing these registered buffers**. This is the #1 design gap flagged by reviewers (Mateos and others).

The Ming Lei series adds:
- registered-buffer kfuncs so the BPF loop can access pre-registered buffers without user-space assistance
- a different attachment model (per-queue vs global per-context)

Design tension: the "replace entire loop" model assumes the BPF scheduler owns the submission path; registered buffers assume explicit buffer management. The patchset mediates this via optional, not-yet-default-enabled kfuncs.

## 7. Cancellation and cleanup contract

When the owning task is killed:
1. Kernel sets the io_uring cancellation flag.
2. In the next BPF loop iteration, kernel does **not** re-call the BPF program.
3. Instead it falls back to `io_uring_kill()` which cancels all pending SQEs.
4. `io_uring_cancel_task_requests()` runs request cleanup and invokes `->cancel()` for each operation.
5. Chain-linked SQEs are unlinked.

**Implication:** a BPF program attached to an io_uring instance does not need to be kill-safe. The kernel handles the race by simply not re-invoking the program once cancellation wins.

## 8. Memory model and race behavior

- Ring memory is shared between BPF program and user space.
- User calls `munmap()` on ring pages after BPF is attached:
  - kernel holds an `mm_struct` reference on the io_uring fd until `close()`
  - BPF side does not fault because kernel mapping is stable
- **Spurious wakeups:** kernel documentation explicitly states BPF programs must be tolerant of inconsistent queue state (CQE retire vs re-post semantics). Do not assume linear CQE ordering.

## 9. Security and sandboxing considerations

- A container that creates an io_uring instance and then drops privileges **still retains the ability to install a BPF program** on that instance unless BPF itself is restricted by the container runtime.
- The BPF program can drive submission/completion entirely in-kernel; functionally similar to a ring0 sidecar.
- **Inherited filters** across `fork()` create a useful policy-inheritance primitive if orchestrated carefully. Most PaaS sandbox designs have not yet fully modeled io_uring+BPF attack surface.
- Filter runs **before** SQE execution, but not before FD creation. A dangerous op that opens an unintended path is still reachable if user space already opened its FDs before installing the filter.

## 10. Performance inflection points

| SQD size | Dominant cost |
|----------|---------------|
| < 256 | BPF verifier + kfunc dispatch |
| large / steady | syscall elimination wins |
| zero-copy TCP < 3000-byte pkt | dyn-ptr + verifier overhead can erase gain |
| zero-copy TCP large steady | 50-150ns saved per CQE vs io_uring_enter() |

Real-world measurement guideline (Axboe 2026): benchmark at message sizes matching your actual traffic, not just maximum throughput. The inflection around 3000-byte packets is TCP-specific. For storage/block workloads the break-even is typically much higher because IO sizes are already large.

## 11. Open design tensions / unresolved items

- **Begunkov "replace entire loop"** vs **Ming Lei "registered-buffer-oriented attachment"**: not incompatible, but they have conflicting ownership assumptions for buffer refill. The 7.1 merge window is the intended resolution point.
- Registered-buffer kfuncs likely land as **optional and disabled-by-default** in 7.1 due to security review concerns.
- `bpf_ringbuf_reserve()` semantics for io_uring regions under multi-producer / single-consumer correctness are still under discussion.
- Containers and io_uring isolation: no finalized kernel-side mechanism prevents a container process from installing a BPF program that interferes with sibling containers' io_uring instances.

## 12. Kernel source pointers

- `fs/io_uring.c` — main io_uring subsystem
- `kernel/bpf/` — BPF verifier, kfunc call sites
- `include/linux/io_uring.h` — `io_uring_setup` flags, SQE/CQE structs
- `tools/sched_ext/` — related BPF struct_ops examples
- `io_uring/` mailing list thread: "BPF filter v7" (Axboe, 2026-01)

## 13. Exercises

1. **Mechanistic:** Trace the code path from `io_uring_enter()` to the BPF program invocation. At what exact point does the kernel switch from user-visible behavior to BPF-driven behavior? Identify the `ops` field that selects the event loop.

2. **Fork analysis:** Draw the reference-counting lifecycle for an io_uring fd + attached BPF program across a `fork()`. When does the BPF program attach count increment?

3. **Filter audit:** Given a container that calls `io_uring_setup()` followed by `bpf()` to attach a filter, enumerate what system calls this filter can modify, block, or accelerate. Where is the sandbox boundary?

4. **Performance:** Design an experiment to measure the break-even SQD where BPF event-loop offload becomes net-negative because of verifier/dyn-ptr overhead. What tracepoints would you use?

## Related Intel
- `/home/nova/.hermes/intel/systems/2026-06-05_io_uring_bpf_filter_registered_buffer_kfuncs.md`
- Existing skill: `bpf-io_uring-event-loop-mechanics` (broader event-loop coverage)
