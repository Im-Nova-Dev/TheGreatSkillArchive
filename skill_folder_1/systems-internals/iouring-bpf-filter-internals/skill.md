---
name: iouring-bpf-filter-internals
description: Mechanistic internals of the Linux io_uring BPF cBPF filter path (IORING_REGISTER_BPF_FILTER) — how programs are attached, how filter hooks are evaluated on each SQE, fork-inheritance semantics, refcounting, and bugs that arise from cBPF-vs-eBPF mismatch.
triggers:
  - io_uring bpf filter
  - IORING_REGISTER_BPF_FILTER
  - cBPF io_uring
  - io_uring bpf internals
  - io_submit_sqes filter
  - kernel bpf filter
  - io_uring cBPF edge cases
---

# iouring-bpf-filter-internals

> Focus: kernel implementation mechanics, not user-space helper libraries.
> Last updated: 2026-06-06

## 1. Context: why io_uring needs a filter

io_uring separates the submission path from the completion path. By design, user-space batches system-call work into a shared-memory submission queue (SQ). The ring is poll-driven or IRQ-driven; threads or libraries may share one ring across pid/uid or inside containers.

A BPF filter on that ring is a kernel-side programmable gate for each SQE: it can inspect opcode + arguments and reject submission before `io_submit_sqes` proceeds. Two design constraints make this nontrivial:

1. **Performance**: filters run inline on the submission hot-path.
2. **Safety**: there is no full userspace context inside `io_submit_sqes()`; the filter can only see struct fields carved into flat byte arrays.

## 2. Registration: from io_uring_register to a live filter

### 2.1 syscall entry and argument unpacking

User-space calls:

```
io_uring_register(ring_fd, IORING_REGISTER_BPF_FILTER,
                  &reg, sizeof(reg));
```

where `reg` contains a BPF program file descriptor and an indicator specifying cBPF or eBPF class. Kernel entry point is `sys_io_uring_register` in `io_uring.c`. A major mechanical detail:

- The kernel does **not** treat `IORING_REGISTER_BPF_FILTER` as idempotent for an already-registered ring. Re-register overwrites the existing filter list for the ringfd instance.

### 2.2 BPF program refcounting

After validation, the kernel calls `bpf_prog_inc_ref` on the passed FD to take ownership. This by itself is a footgun:

- If the user closes the FD after registration, the kernel keeps the program alive.
- If the user `bpf()` close/replace the program through another path, the io_ring's reference keeps the old program live — but replay or reattach races can arise when the user sends new programs that interact with maps the old program still uses.

### 2.3 Ring-internal filter object insertion

On success, the kernel appends a filter record to the ring's filter list. Each filter record stores:

- `bpf_prog *` pointer
- `filter_type` (`IORING_REGISTER_BPF_FILTER` family)
- flags such as fork-clone behavior (see §5)

The filter list is not visible to poll/completion; it is consulted only in the submission path.

## 3. Submission hot-path: io_submit_sqes and the filter hook

### 3.1 The sequence of checks

Inside `io_submit_sqes()`:

1. Get `struct io_kiocb` for the SQE.
2. Walk the ring's filter list in insertion order.
3. For each filter, call into the BPF runtime: `bpf_prog_run` with a constructed `struct io_uring_bpf_ctx`.
4. If any filter returns a reject code, abort the submission of this SQE.

The struct passed to BPF is a flat layout:

```
struct io_uring_bpf_ctx {
    __u8  opcode;
    __u8  flags;    // IOSQE_* bits
    __u16 ioprio;
    __u32 len;
    __u64 addr;
    __u64 off;
    __u32 rw_flags;
    __u32 buf_index;
    __u16 personality;
    __u16 pad0[3];
    __u32 file_index;   /* fixed file slot or ~0U */
    // ... follow-on fields for specific opcodes ...
};
```

This is critical system-design: the filter can read but not safely write SQE memory. Writing is not forbidden by the verifier, but the kernel does not commit any BPF-side mutation.

### 3.2 Return value semantics

The cBPF return register is interpreted as a boolean-style verdict. Zero means pass (no rejection), nonzero means reject. The io_uring layer encodes the rejection in `sqe->flags`? No, actually: the kernel returns `-EACCES` to `io_uring_enter()` for the individual failing SQE. Rejection is per-SQE, not per-ring.

This means a multi-SQE `io_uring_enter()` batch can be partially applied. User-space must check nonblock vs blocking io_uring_enter semantics carefully — any return value other than a sum of submitted CQEs can indicate partial completion.

### 3.3 cBPF vs eBPF

The registration interface allows legacy cBPF programs. Internally, the runtime converts cBPF to eBPF via the kernel's classic-to-Socketfilter conversion path, then verifies as eBPF. To a mechanistic reader, this has consequences:

- cBPF has no verifier precision tracking; if the program reads past `io_uring_bpf_ctx`'s defined fields, the kernel treats it as an error conversion step.
- The conversion drops the original cBPF class, so `tc` or `socket filter` semantics do not apply; only the io_uring subclass is honored.
- cBPF maps interact with eBPF verifier constraints: if the cBPF references a map, the bridge may not support all map types.

## 4. Verifier and safety concerns unique to this path

### 4.1 Pointer-width subtleties

The `addr` and `off` fields are 64-bit even on 32-bit kernels if the system uses 64-bit io_uring structures. eBPF verifiers on 32-bit platforms will truncate the upper 32 bits when the cBPF→eBPF bridge passes the field. This is a silent bug class for AnyIO programs that validate buffer alignment.

### 4.2 Reference tracking on maps

Modern eBPF mapping types (arena, ringbuf, hash map) interact with BPF semantics. The io_uring filter path does not add any special pins:

- If the BPF program uses an arena map, the `bpf_fd` is stored in the BPF program only. The io_uring ring does not pin the map.
- Consequently, if user-space closes the BPF map FD while the ring lives, the program's `bpf_map_*` helper calls can return `-EBUSY` or `-ENOENT` depending on whether the map is pinned elsewhere.

### 4.3 Helper call limitations

`bpf_prog_run` for io_uring filters allows a restricted helper set. The common footgun:

- `bpf_get_current_pid_tgid()` and `bpf_get_current_uid_gid()` are allowed.
- `bpf_ringbuf_output()` and `bpf_event_output()` are legal, but each submission may sleep — violating softirq constraints.
- Any helper that calls `might_sleep()` from inside the ring's submission context triggers a might_sleep splat. This is why `bpf_loop()` + sleepable helpers are not permitted in ring filters.

## 5. fork(2) and clone semantics

### 5.1 The child inherits the filter list mechanically

When the parent forks after registering a filter:

- The child gets its own `io_ring` struct via `copy_process()`. The ring's filter list is copied shallowly.
- Both parent and child reachable: the `bpf_prog_inc_ref()` is honored so the program stays live in both rings.
- However, the filter verifier does not re-run in the child context. PID, UID, and cgroup hooks computed during program load remain same-as-parent.

### 5.2 Security implication: map ownership split

In a container/runtime sandbox scenario:

- The parent might open the ring and register a filter that looks at `bpf_get_current_uid_gid()`.
- On `clone(CLONE_FILES)`, the child shares FD table but has new PID. The filter still returns "parent UID" because the verifier-seeded helper calls read the kernel's current creds — meaning a shared-ring child can bypass policy that the filter is supposed to enforce per-isolation-domain.

### 5.3 Fix attempts and gaps

- Fix attempts in kernel patches (2025-2026) added `IORING_SETUP_ATTACH_FILTER` semantics to revalidate filters in child on `clone(CLONE_THREAD|CLONE_SIGHAND|CLONE_VM)`. These only partially close the gap; a cooperative or uncooperative child running in separate memory can delete or replace the filter before the next submission.

## 6. Interaction with container sandboxing and seccomp-bpf

The cBPF filter path is distinct from io_uring's `IORING_REGISTER_ENABLE_RINGS` + fdinfo-based security model.

A common misassumption: developers think seccomp-bpf automatically filters io_uring syscalls after ring setup. It does, for the *enter* syscall itself. But it does not see individual SQEs inside the shared memory ring. The io_uring BPF filter is the only native gate inside the ring's logical ring buffer.

This means any malicious thread that calls `io_uring_enter(..., IORING_ENTER_GETEVENTS)` but whose SQEs are crafted by unprivileged code must depend on filter programs for intra-ring validation.

## 7. Known bug classes and CVEs in this path

### 7.1 Reference-counting races on map and program churn

If user-space issues:

```
bpf(BPF_PROG_DETACH, ... old prog fd ...);
close(old_prog_fd);
```

while a queue of submissions is pending in a ring whose filter points to that program, the kernel still runs the detached-but-not-yet-freed program for in-flight SQE checks. The program's map pointers can race with raced map reclamation. This class of bug was observed in 6.15+ and patched by pinning the program `bpf_kallsyms` reference until all pending submissions drain.

### 7.2 Shadow-SQE memory exhaustion

Every filter that calls `bpf_ringbuf_output()` allocates a per-cpu/perf ringbuf. If the filter runs for every SQE of a high-throughput workload, this can exhaust the task's locked-memory budget — leading to `ENOMEM` inside the submission path and partial batch completion.

### 7.3 Fork concurrency and filter list races

Two threads in child/parent both calling `io_uring_enter()` can race on the shared filter list's refcount. The mechanical execution is:

- Parent: `io_uring_enter` enters `io_submit_sqes()` → walks filter list.
- Child: `io_uring_enter` concurrently walks + updates filter list during child-initiated re-registration.

The `filter_refs` atomic counter is not protected by the same lock as the filter list pointer in allo implementations. A patch is pending for 7.1 to switch to `rcu_list` iteration with `synchronize_rcu()` on unregister.

## 8. Mechanistic mental model

```
sys_io_uring_register
 └─ IORING_REGISTER_BPF_FILTER
     └─ copy_from_user(filter reg)
         ├─ bpf_prog_get(uprog_fd)  // take ownership
         └─ ring->filters.append(...)
             io_uring_enter → io_submit_sqes
                 for each SQE:
                     for each filter in ring->filters:
                         ctx = compose io_uring_bpf_ctx from sqe
                         verdict = bpf_prog_run(filter, &ctx)
                         if verdict != 0
                             reject SQE (-EACCES)
```

Key invariants:
- Filter runs once per SQE; reject is per-SQE.
- Filter context is a snapshot of SQE fields at submit time.
- None of SQE memory is mutated by filter.
- Refs are counted transparently over `io_uring_close`.

## 9. Code references and how to explore

Core files:
- `io_uring/io_uring.c`: `sys_io_uring_register`, `io_submit_sqes`, `io_unregister_bpf`.
- `kernel/bpf/syscall.c`: BPF program refcounting for registered FD.
- `include/uapi/linux/io_uring.h`: `IORING_REGISTER_BPF_FILTER`, `struct io_uring_bpf_ctx`.
- `tools/include/uapi/linux/bpf.h`: cBPF-to-eBPF bridge fields.

Good sequence to read:
1. Search for `IORING_REGISTER_BPF_FILTER` case in `sys_io_uring_register`.
2. Walk `io_install_bpf_filter()`.
3. Walk filter execution in `io_submit_sqes()`.
4. Trace `bpf_prog_run()` for non-sleepable context; cross-check `might_sleep()` helper list in `kernel/bpf/helpers.c`.

## 10. Tuning / debugging pitfalls

| Symptom | Likely cause |
|---|---|
| io_uring_enter returns `-EACCES` for some but not all SQEs | cBPF filter rejecting by opcode; not a kernel bug. Inspect filter program's instruction path. |
| submits block after `IORING_SETUP_SINGLE_ISSUER` removed | filter list deeply nested with BPF helper calls that trace-schedule. |
| child process filters inherited after Docker `unshare` | shallow ring copy in `copy_process`; need explicit `io_uring_register(...DEREGISTER...)` post-fork. |
| `-ENOMEM` under load | filter's `bpf_ringbuf_output()` or `bpf_perf_event_output()` alloc path choked on locked memory. |
