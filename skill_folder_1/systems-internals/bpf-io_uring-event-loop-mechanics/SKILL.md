---
name: bpf-io_uring-event-loop-mechanics
description: Mechanistic internals of the BPF-driven io_uring event loop introduced in Linux 7.0/7.1. Covers queue attachment, kfuncs, SQ/CQ loop replacement, IOU_LOOP_CONTINUE semantics, registered-buffer kfunc gaps, cancellation/cleanup, and hardening surface area.
---

# BPF-Driven io_uring Event Loop Mechanics

Use this skill when studying how `io_uring`'s in-kernel event loop can be replaced by an eBPF program, what the API surface looks like, how the re-entry model works, and what kernel internals a developer should trust (or audit) when using this on a production host.

## Trigger Conditions

- User asks about `io_uring` + BPF, BPF `IORING_SETUP` extensions, `bpf_io_uring_*` kfuncs, or recent patch sets.
- Kernel version is 7.0+ and discussion centers on reducing user-space scheduling overhead for async I/O.
- You need to explain how a single `io_uring_enter()` call can run an entire async event loop without returning to user space.

## Core Concepts

### 1. Ring Buffers and Baseline Flow

`io_uring_setup()` + `mmap()` produces shared memory regions:

- SQ ring: `io_uring_sqe` array with `tail`/`head` indices.
- CQ ring: `io_uring_cqe` array with `head`/`tail` indices.

Normal flow:
1. User posts SQEs, updates `SQ->tail`.
2. `io_uring_enter()` calls `io_submit_sqes()`.
3. Kernel dispatches IOSQE_CHAIN/LINK dependencies in `io_queue_async_work()`.
4. `io_uring_enter()` waits:
   - busy-polls for pollable IOs
   - waits on `waitqueue` for completion interrupts
5. On completion, CQEs are written to CQ, `CQ->tail` advanced.
6. Control returns to user space; user reads CQ and frees SQE slots.

Key primitives:
- `io_sq_wq_worker` / io-wq threads poll SQ when `io_uring_enter()` is not called.
- Completion is delivered via:
  - `io_req_complete_post()` -> `io_cqe_queue_tail()` -> wakeup
  - or task_work if called from same task in process context.

### 2. BPF Event Loop Hook (7.0/7.1+)

With the merged Begunkov patchset, you attach a BPF struct-op program to an
io_uring instance (fd attachment is the target).

Entry point when user calls `io_uring_enter()`:
- Instead of the C event loop, kernel calls the BPF program.
- BPF sees the ring memory via `bpf_io_uring_get_region()` and can drive the
  submission/completion cycle entirely.

#### kfuncs

- `bpf_io_uring_submit_sqes()`: inspects SQ, executes bound requests. Returns the
  number of processed SQEs or negative `-EIO` for shutdown path.
- `bpf_io_uring_get_region()`: returns KMappable region handle for SQ or CQ
  traversal.

Contract semantics:
- kfuncs expect the SQ tail not to move ahead of kernel due to active
  `io_uring_enter()` reentry; BPF should call `submit_sqes()` once per loop
  iteration.
- CQE consumption is implicit: the kernel queued CQEs from earlier submits are
  visible after wait; the BPF program must re-check for new data until it
  decides to stop.

#### Loop Control

Two exit codes govern re-entry behavior:

- `IOU_LOOP_CONTINUE`: immediately re-run the BPF program.
- `IOU_LOOP_STOP`: break out, return control to user space.

This allows patterns like:
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

Because the loop lives in the kernel, a single `io_uring_enter()` can process
thousands of completions without returning to user space.

### 3. Registered Buffers and Known Gaps

Users can pin reusable buffers with `io_uring_register_buf_ring()` to amortize
pinning cost. The initial merged patchset did NOT include kfuncs for accessing
registered buffers. This was a driving critique from Caleb Mateos and others.

Separate Ming Lei series (Jan 2026) adds:
- registered buffer kfuncs
- different attachment model (per-queue vs global per-context)

This means:
- The 6.19 BPF hook is useful for SQE/CQE management, but complex buffer-pinning
  scenarios may still require an alternate patch series or explicit user-space
  orchestration.

### 4. Concurrency, Cancellation, and Cleanup

#### Cancellation Path

- If the owning task is killed, the kernel sets an io_uring cancellation flag.
- Next BPF loop iteration: kernel does NOT re-call the BPF program in the dying
  task; instead falls back to `io_uring_kill()` which cancels all pending SQEs.
- `io_uring_cancel_task_requests()` runs request cleanup, invokes `->cancel()`
  for each operation; chain-linked SQEs are unlinked.
- No double-free or CQ corruption because the BPF program is not re-run once
  cancellation wins the race.

#### Memory Model

- Ring memory is shared: BPF sees same physical pages as user space.
- User calling `munmap()` on the ring after BPF is attached:
  - kernel holds an `mm_struct` ref on the io_uring fd until close
  - BPF side does not fault because kernel mapping is stable
- Spurious wakeups: doc explicitly states BPF programs must be tolerant of
  inconsistent queue state (CQE retire vs re-post semantics).

### 5. Performance Model

Inflection points:
- Small SQD (<256): overhead dominated by BPF verifier and kfunc dispatch.
- Large/steady stream: system call elimination wins.

Real-world measurement angle:
- io_uring zero-copy TCP has inflection around 3000-byte packets (Axboe, 2026).
- BPF event-loop offload makes that worse for short-lived sockets but saves
  50–150ns per CQE processing in steady state by removing `io_uring_enter()`
  warp-around.

## 2026-06-05 Intel Update

A patch set from Jens Axboe (v7) for Linux 7.0 added cBPF filters into the
io_uring submission path. The filter is inherited across `fork()`, and once set,
only further restriction is allowed. A competing series from Ming Lei adds
registered-buffer kfuncs, with the two sets merged together for 7.1.

## 2026-06-06 Intel Update

The v7 patchset from Jens Axboe added cBPF filtering (`IORING_REGISTER_BPF_FILTER`) to the io_uring submission path in Linux 7.0. This is the opcode-restriction counterpart to the event-loop offload, not an alternative: a hardened setup typically layers both — cBPF for opcode gating + BPF event-loop for submit batching.

See the companion skill `systems-internals/iouring-bpf-filter-internals` for the submission-path mechanics, `struct io_uring_bpf_ctx` ABI, cBPF-over-eBPF rationale, fork-inheritance model, and container/seccomp implications.

## Exercises / Research Prompts

1. **Mechanistic:** Draw the state machine for `bpf_io_uring_submit_sqes()` when
   it processes a linked SQ chain with both read and write phases. Where does the
   kernel cross from submission to completion and back?

2. **Hardening audit:** Imagine an attacker who controls a BPF program attached
   to an io_uring instance; enumerate the maximum damage reachable via the
   existing kfuncs (file ops, network ops, memory region access).

3. **Design comparison:** Compare the Begunkov "replace entire loop" model with
   the Ming Lei registered-buffer attachment model. Which one enables faster
   zero-copy pubsub pipelines?

4. **Performance:** Instrument an HTTP proxy that switches between using
   `io_uring_enter()` for each batch vs a BPF loop. Where does the BPF loop
   become net-negative due to verifier/dyn-ptr overhead?

## Related Intel

Broader context stored under:
- `/home/nova/.hermes/intel/systems/2026-06-05-bpf-io_uring-event-loop.md`

Library notes:
- Source feeds tracked in `systems-intel/source-feed.md` under `eBPF / BPF`
  and `Storage Systems & Filesystems`.
- Related filter-internals skill: `systems-internals/io_uring-bpf-filter-internals`
  (covers fork-inheritance, IOU_LOOP_CONTINUE/IOU_LOOP_STOP, and the
  registered-buffer kfunc gap in the 7.0→7.1 merge window).
