---
name: iouring-bpf-filter-and-submission-path
description: Teach the Linux io_uring kernel submission path and the BPF cBPF opcode filter introduced in Linux 7.0. Mechanistic treatment covers ring buffers, SQE/CQ ring layout, BPF filter registration/inheritance, the io_uring_bpf_ctx ABI, execution ordering, and how this fixes the io_uring seccomp gap — suitable for advanced operating systems coursework and security-aware systems programming.
triggers:
  - io_uring BPF filter
  - IORING_REGISTER_BPF_FILTER
  - io_uring submission path
  - io_uring internals
  - cBPF io_uring
  - io_uring security
  - io_uring container
---

# io_uring Kernel Submission Path and BPF cBPF Filter (Linux 7.0+)

## Prerequisites / level expectation

- Comfortable with kernel/userspace shared memory and memory-mapped ring buffers.
- Understands how seccomp/cBPF restricts syscalls.
- Has read `man7/io_uring.7` or equivalent introduction.

---

## 1. The ring shares memory with the kernel — why syscall inspection alone failed

`io_uring_setup()` returns an fd. The caller then `mmap`s two regions:

- **SQ ring** — array of `io_uring_sqe` plus index head/tail.
- **CQ ring** — array of `io_uring_cqe` plus index head/tail.

The application fills SQEs in the shared SQ memory and bumps `tail`. The kernel consumes them, executes the opcodes, writes CQEs into the CQ, and bumps `tail`.

The key structural problem: the actual **opcode + arguments** live exclusively inside that shared ring buffer. When the application later calls `io_uring_enter()`, the kernel sees only a handful of `io_uring_enter` flags (submit count, wait flags). Traditional seccomp filters that inspect syscall arguments therefore see *no* per-opcode information.

### Consequence (pre-7.0)

- Running a process with `seccomp` + `CAP_NET_BIND_SERVICE` and `io_uring_enter` allowed meant the process could issue any opcode: `IORING_OP_OPENAT`, `IORING_OP_NEWNAME` (on some configs), socket ops, `IORING_OP_ACCEPT`, `IORING_OP_EPOLL_CTL`, etc.
- Google's Docker default, GKE Autopilot, and ChromeOS all responded by blocking `io_uring_enter` entirely.

---

## 2. io_uring kernel submission path (step-by-step)

```
user: write SQE into mmap'd SQ ring
user: smp_store_release(SQ->tail)

user: io_uring_enter(fd, to_submit, min_complete, flags, sig, sz)
    → do_io_uring_enter()
        → io_submit_sqes(ctx, to_submit)
            for each SQE:
                sqe = get_sqe(...)
                ctx->check_bpf_filter(sqe)        ← NEW in 7.0
                ...
                io_opcode_to_ops(sqe->opcode)->init()
                io_queue_sqe(ops, ...)
```

After the SQE is accepted, the kernel drives the async I/O:

1. For pollable I/O, the kernel arms `poll()`/epoll machinery.
2. The `io-wq` worker pool (or SQPOLL kernel thread) triggers completion.
3. `io_req_complete_post()` writes CQE into CQ ring.
4. If a waiter is blocked in `io_uring_enter`, the kernel wakes it.

The filter hooks **between step 0 and step 1** in the sequence above.

---

## 3. The cBPF filter mechanics

### 3.1 Registration

`IORING_REGISTER_BPF_FILTER` attaches a BPF program to an io_uring ring context:

- accepts a `bpf_prog_fd` already loaded via `seccomp(SECCOMP_SET_MODE_FILTER)` or the `bpf()` syscall.
- the kernel calls `bpf_prog_inc_ref()` so the prog survives past the registering process.
- the prog reference is stored in `struct io_ring_ctx::bpf_filter_list`, per opcode.

### 3.2 ABI: `struct io_uring_bpf_ctx`

```c
struct io_uring_bpf_ctx {
    __u16   opcode;
    __u16   flags;
    __u32   ioprio;
    __u64   off;
    __u32   len;
    __u32   rw_flags;
    __u32   file_index;
    __u32   buf_index;
    __u16   personality;
    __u16   fixed_file;
    __u8    rw;
    __u8    poll_op;
    __u8    op_flags;
    __u8    addr_len;
    __u8    msg_flags;
    __u8    __pad[2];
    __u64   addr;
    __u64   user_data;
    __u32   pdu_size;   /* added in v7, tells filter what kernel exposes */
};
```

Fields the kernel pre-populates from the SQE snapshot. The filter sees this copy, not live ring memory.

Selection rationale:
- The smallest useful view that lets an allowlist judge the opcode category (read, write, accept, openat…) and parameters like `len`, `rw`, and whether the FD is fixed-file-register.
- Not large enough to encode a full `msghdr` or `open_how`; those details stay inside the opcode-specific `init()` path later.

### 3.3 Execution path

```
for each SQE in the submit batch:
    ctx->check_bpf_filter(sqe)
        walks bpf_filter_list for sqe->opcode
        for each attached filter program:
            call cBPF program with ctx = &local copy of io_uring_bpf_ctx
            if *any* filter returns 0:
                io_complete_sqe(sqe, -ECANCELED)
                skip io_opcode_to_ops()->init()
                continue to next SQE in the batch
        if all nonzero:
            proceed to opcode dispatch
```

- Return convention: non-zero = allow, zero = deny. The cBPF program always returns a 32-bit `a_reg` value from the interpreter.
- Multiple stacked filters: one veto blocks; all-must-allow semantics.

### 3.4 `pdu_size` and forward-compatibility

The v7 patch adds `pdu_size` to the bottom of the struct. The filter can verify:

```c
if (ctx->pdu_size < EXPANDED_IO_URING_BPF_CTX_SIZE)
    return 0;
```

This prevents a silent ABI mismatch when a future kernel adds fields like `uring_op_specific` flags the filter doesn't know about.

---

## 4. Why cBPF, mechanistically

Three reasons are visible in the patchset and mailing-list discussion:

1. **Argument model.** cBPF has no maps, no helper functions, no indirect calls. An attacker who controls the cBPF prog (via seccomp, in unprivileged containers) cannot escape the opcode+parameters the kernel put in `io_uring_bpf_ctx`. With eBPF the filter could call `bpf_map_lookup_elem()` and consult runtime state, raising the blast radius if the map is writable by another privileged entity.

2. **Load path.** The filter uses the existing `seccomp` cBPF loader. No BPF syscall, no CAP_BPF. Container runtimes and systemd units can attach the filter at container init without elevated privileges.

3. **Hot path cost.** The cBPF interpreter in the `io_submit_sqes` path is ~30 instructions. The eBPF interpreter/JIT runs a larger setup (prog refcount, `bpf_prog_ops` lookup, `security_bpf_prog` LSM, tail-call handling). For an io_uring submit rate of 1M opcodes/sec, the extra 100–150 ns of eBPF dispatch is ~10–15% CPU.

The tradeoff is clear: cBPF cannot consult runtime state, but it wins on security simplicity and submit-path latency.

---

## 5. Inheritance across `fork()`

Series title: "Inherited restrictions and BPF filtering." Mechanism:

1. `copy_process()` clones `io_ring_ctx`. The `bpf_filter_list` head pointer is copied.
2. For each filter node in the list, `bpf_prog_inc_ref()` runs again.
3. The child io_uring context starts with the parent's filters already attached.
4. There is *no* operation to remove a filter once attached from userspace.

This design prevents privilege-deescalation attacks: a child that drops to an unprivileged user cannot weaken the parent's filter list. The only operation allowed post-setup is adding *more restrictive* filters.

---

## 6. Comparison: cBPF opcode filter vs BPF `struct_ops` event-loop

| Property | cBPF filter (7.0) | BPF event-loop (7.1, `struct_ops`) |
|---|---|---|
| Purpose | Restrict which opcodes execute | Drive submission+completion from BPF |
| Attachment | `IORING_REGISTER_BPF_FILTER` | `IORING_REGISTER_BPF_PROG` (`struct_ops`) |
| Language | cBPF (no maps, no helpers) | eBPF `struct_ops` |
| Load privilege | Unprivileged (seccomp-style) | Root / `CAP_BPF` |
| Performance | +20–40 ns per SQE; constant | Removes `io_uring_enter()` warp-around, −50–150 ns per CQE in steady-state |
| Security model | Opcode allowlist / blocklist | Direct kernel path control |
| Production use | Container io_uring enablement now viable | Enterprise fast-path I/O (PostgreSQL 18) |

A hardened production setup typically uses both: cBPF filter to gate opcodes + BPF event-loop for batch I/O efficiency.

---

## 7. Container security posture on 7.0+

```c
// Inside container init, after io_uring fd is created:
struct bpf_program *allow_rw = load_cbpf_filter();  // via seccomp()
io_uring_register(fd, IORING_REGISTER_BPF_FILTER,
                  allow_rw->fd, SQE_OP_READ | SQE_OP_WRITE | SQE_OP_POLL_ADD);
```

Result:
- Any thread in the container that calls `io_uring_enter` can only submit `READ`/`WRITE`/`POLL_ADD`.
- Any attempt to `accept()` or `openat()` through io_uring returns `-ECANCELED` in the CQE.
- The policy cannot be removed by the container after init.

Systemd can express the same via `SystemCallFilter=@io-uring` plus an `ExecStartPre=` that loads the cBPF filter onto the service's dropped-capability sandbox.

---

## 8. Kernel-path exercises

1. **Trace the filter walk.** Insert a `bpftrace` probe on `io_submit_sqes` to count filter checks per opcode:
   ```bash
   bpftrace -e 'kprobe:io_submit_sqes { @op[args->sqe->opcode] = count(); }'
   ```
   Compare with the number of actual CQEs to see the filter-to-execution ratio.

2. **Draft an opcode allowlist.** Write a cBPF program that only allows:
   - `IORING_OP_READ` with `len < 128K`
   - `IORING_OP_WRITE` with `len < 128K`
   - `IORING_OP_POLL_ADD`
   - `IORING_OP_NOOP` (for keepalive/polling loops)
   Every other opcode and any read/write larger than 128K is denied.

3. **Audit the ABI stability boundary.** Identify which fields in `struct io_uring_bpf_ctx` could grow without breaking an existing filter. Trace how `pdu_size` guards against silent ABI drift.

4. **Inheritance analysis.** Start a process, create an io_uring instance, attach a filter, then `fork()`. From the child, attempt to submit a blocked opcode. Confirm the child inherits the deny and cannot unilaterally weaken it.

5. **Compare to the event-loop path.** Read `io_uring/bpf_filter.c` and `io_uring/bpf_event_loop.c` (or `bpf_io_uring_*` kfunc landings). Note the difference between how the filter's return code feeds into `io_complete_sqe()` (immediate CQE error) versus how the `struct_ops` event-loop defers the CQE until the BPF program calls submit+wait.

---

## 9. References

- Jens Axboe v7 patchset: https://lore.kernel.org/io-uring/20260127183311.86505-1-axboe@kernel.dk/
- LWN "Inherited restrictions and BPF filtering for io_uring": https://lwn.net/Articles/1056226/
- Byteiota developer guide: https://byteiota.com/linux-7-iouring-bpf-filtering-zero-copy-developer-guide/
- `io_uring/bpf_filter.c` (7.0, for-7.0/io_uring branch)
- `include/uapi/linux/io_uring/bpf_filter.h`
- io_uring man page: https://man7.org/linux/man-pages/man7/io_uring.7.html
- Related: `io_uring/bpf_event_loop` and `bpf-io_uring-event-loop-mechanics` skill for the BPF `struct_ops` path
- Related: `bpf-jit-alignment-and-atomic-tearing` skill for eBPF JIT correctness context
