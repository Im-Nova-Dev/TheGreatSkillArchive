---
name: iouring-bpf-filter-internals
description: Mechanistic internals of io_uring BPF filtering (cBPF) merged in Linux 7.0. Covers filter registration, attach/inheritance model, execution path relative to SQE submission, the `struct io_uring_bpf_ctx` ABI, cBPF-over-eBPF choice, security/container implications, and how it compares to the separate BPF event-loop (`struct_ops`) path. Go below "how to use" and into kernel-path mechanic details.
---

# io_uring BPF Filter Internals (Linux 7.0+)

## When to use this skill

- You are studying how io_uring opcodes are restricted without blocking the syscall entirely.
- You want to understand what happens between `IORING_REGISTER_BPF_FILTER` and the actual cBPF execution on each SQE.
- You need to know the precise fields exposed to the filter via `struct io_uring_bpf_ctx` and why cBPF was chosen over eBPF.
- You are auditing container security posture for io_uring on kernel 7.0+.

This skill covers the **opcode filter** path. It does *not* cover the BPF event-loop (`struct_ops`) path, which lets a BPF program drive submission+completion directly; for that, see `bpf-io_uring-event-loop-mechanics`.

---

## 1. The problem the filter solves (mechanistic)

### What changed structurally

io_uring's design bypasses normal syscall argument inspection:

1. Application creates a shared-memory ring (`io_uring_setup` + `mmap` of SQ/CQ).
2. SQEs encode opcode + opcode-specific arguments entirely inside that ring.
3. `io_uring_enter` only transmits `submit/flags/wait_nr` as traditional syscall args.
4. The kernel reads SQEs out of the ring internally.

Consequence:
- seccomp, Landlock, and AppArmor see only the `io_uring_enter` call, not the per-SQE opcode.
- A sandboxed process with a valid io_uring fd can issue any of 170+ opcodes (NVMe passthrough, `accept`, `sendmsg`, `openat`, `epoll_ctl`, personality switches, etc.).
- On a production system this collapsed to two choices:
  - Allow io_uring fully → open attack surface.
  - Block `io_uring_enter` → lose async I/O performance.

Linux 7.0 adds a BPF hook that runs **after SQE preparation** but **before the kernel's opcode-permission check**, granting visibility into the actual operation context.

### The regression that motivated it

Google kCTF data from 2022 showed 60% of submitted kernel exploits targeted io_uring. The common mitigation was blanket blocking via seccomp. The filter is the structural counter-measure: it enables targeted allowlists expressed as cBPF.

---

## 2. Why cBPF, not eBPF

The patchset explicitly uses classic BPF:

| Factor | cBPF advantage for io_uring filters |
|---|
| **Privilege model** | cBPF is loadable by unprivileged users via `seccomp()` — already trusted in containers. eBPF requires `CAP_BPF` or `CAP_SYS_ADMIN` for many helpers, breaking unprivileged container use cases. |
| **No verifier re-engagement** | The filter loads through the existing seccomp cBPF loader path. The eBPF verifier is not invoked in the hot submit path. |
| **No map / helper surface** | cBPF has no maps, no helper calls. The filter cannot reach back into kernel memory — the damage surface is limited to the opcode + `io_uring_bpf_ctx` fields the kernel copies into the cBPF context. |
| **Auditability** | A 10–20-instruction cBPF program is auditable. An eBPF program using maps + tail calls is not. For opcode allowlisting you don't need loops or map lookups. |

Tradeoff: the filter cannot consult runtime state (e.g., "allow `IORING_OP_WRITE` only if `user_data < 1M`"). For that you would need the separate BPF event-loop (`struct_ops`) approach or the cgroup-based inherited restriction mechanism.

---

## 3. Mechanistic detail: the filter execution path

### 3.1 Registration

New ioctl-style opcode: `IORING_REGISTER_BPF_FILTER`

Arguments (kernel ABI in `io_uring/register.c`):
- `bpf_prog_fd`: an already-loaded BPF program.
- `opcode`: which io_uring opcode the filter governs (or wildcard / per-opcode list).
- `flags`: currently defines inheritance/ordering behavior.

The kernel stores the `bpf_prog` reference (refcounted) into `struct io_ring_ctx` under a per-opcode filter list. Key field additions (v7):

```c
struct io_ring_ctx {
    // ... existing fields ...
    struct list_head bpf_filter_list;   /* per-opcode filter list head */
    // ...
};
```

Each filter node wraps a `bpf_prog *` plus the opcode it targets.

### 3.2 The ctx struct exposed to the filter

User ABI: `struct io_uring_bpf_ctx` in `include/uapi/linux/io_uring/bpf_filter.h`

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
    __u32   pdu_size;   /* v7 addition: kernel-supported ctx size */
};
```

Design note on `pdu_size`: the filter program checks this field against its own expectation of `sizeof(struct io_uring_bpf_ctx)`. If the kernel later adds fields, `pdu_size` grows, and a filter that does not understand the new layout can detect the mismatch and refuse to run. This eliminates a class of ABI-bypass bugs where old filters silently misinterpret new fields.

### 3.3 Where the filter runs in the submit path

```
io_uring_enter()
  → io_submit_sqes()
      for each SQE in batch:
        → sched_check_bpf_filter(sqe)
            walks bpf_filter_list for sqe->opcode
            runs each cBPF prog with ctx = io_uring_bpf_ctx
            if any returns 0 → sqe completed with -ECANCELED, no exec
            if all return nonzero → continue
        → [opcode-permission check, existing restrictions]
        → actual opcode dispatch
```

Critical ordering properties:
- **Filter runs before the opcode-permission check.** If the filter returns 0 (deny), the kernel does not proceed to the existing `io_check_restriction()` machinery.
- **BPF context is pre-populated from the SQE.** The kernel copies `opcode`, `ioprio`, `off`, `len`, `flags`, `user_data`, etc. into `struct io_uring_bpf_ctx` before calling the filter. The filter sees a snapshot, not a live pointer back into the ring.
- **One deny vetoes.** Multiple filters can be stacked; all must return nonzero for the SQE to proceed.

### 3.4 Inheritance across `fork()`

Series title: "Inherited restrictions and BPF filtering."

- An io_uring instance's BPF filter list is reference-counted via `bpf_prog` refs.
- On `fork()`, the child's `io_ring_ctx` is copied; `bpf_filter_list` head is populated with the same `bpf_prog` refs (count incremented).
- There is no flag to *remove* a filter after setup — only to add more. This is intentional: once a security policy is attached, it cannot be weakened by a lesser-privileged child.

This is functionally analogous to the existing `IORING_SETUP_RESTRICTION` mechanism but extends it with user-defined logic.

---

## 4. What the filter can and cannot do

### It CAN

- Allowlist / blocklist opcodes (`IORING_OP_READ`, `IORING_OP_WRITE`, `IORING_OP_ACCEPT`, etc.).
- Gate on high-level opcode parameters seen in the snapshot (e.g., `len > 0 && rw == READ`).
- Inspect `personality` (to decide whether a previously-registered `IORING_SETUP_SQPOLL` personality is acceptable).
- Check `fixed_file` / `file_index` to allow fixed-file-register-based FD access only.

### It CANNOT

- Validate that user-supplied buffer pointers are inside a registered buffer region. That validation happens later in the opcode-specific `->init()` path and is not exposed to the cBPF filter.
- Inspect eBPF maps or call helpers. The filter context contains no map pointer.
- Gate on dynamic state inside the kernel (e.g., current `cgroup` weight, memory pressure). For that use `sched_ext` or a full eBPF program.

### Practical implication for security design

- The filter is an **opcode firewall** not a **parameter firewall**.
- A well-tuned filter that blocks all opcodes except `READ`/`WRITE` reduces the attack surface to buffer-registration correctness and rw-flags manipulation.
- The risk of unknown opcodes being added in future kernels is mitigated by `pdu_size` + explicit allowlisting: "allow only what I name, deny everything else."

---

## 5. Container / sandbox interaction

### seccomp pre-7.0 behavior

```c
// Typical docker default before 7.0
SCMP_ACT_ALLOW for most syscalls
SCMP_ACT_ERRNO for io_uring_enter  (blocked)
```

Result: no async I/O inside containers.

### seccomp on 7.0+

The filter enables a replacement pattern:

```c
// 1) Allow io_uring_enter
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_io_uring_enter, 0);

// 2) Attach cBPF filter to the io_uring fd at container init
io_uring_register(fd, IORING_REGISTER_BPF_FILTER,
                  bpf_prog_fd, /*opcode=wildcard*/ -1);
```

Runtime: any attempt to issue a non-allowlisted opcode gets `-ECANCELED` on the CQE without touching seccomp.

### systemd integration angle

systemd's `SystemCallFilter=` directive in unit files can now conditionally allow `io_uring_enter` when a sandboxed service also has a matching BPF filter pre-loaded. This is a tighter sandbox than "allow everything" or "deny everything".

---

## 6. Comparison: cBPF filter path vs BPF event-loop path

| Property | cBPF opcode filter (7.0) | BPF event-loop (`struct_ops`, 7.1) |
|---|---|---|
| **Goal** | Restrict which opcodes execute | Drive submit+completion from BPF |
| **Attachment type** | `IORING_REGISTER_BPF_FILTER` per-opcode | `IORING_REGISTER_BPF_PROG` (struct_ops) |
| **Language model** | Classic BPF (cBPF) | eBPF `struct_ops` |
| **Privileges** | Unprivileged load like seccomp | Requires `CAP_BPF` / `CAP_SYS_ADMIN` |
| **Helpers / kfuncs** | None (pure cBPF) | `bpf_io_uring_submit_sqes()`, etc. |
| **Performance** | Negligible per-SQE overhead (3-5 instr) | Removes `io_uring_enter()` warp-around |
| **IoCtl exposure** | Filtered CQE might still appear in CQ | BPF controls when CQ is exposed |
| **Inheritance** | Yes, on `fork()` | Requires explicit setup per-context |
| **Production readiness** | Shipped in 7.0 | Shipped in 7.1 |

A production deployment that wants both restrictions *and* reduced syscall overhead can layer both: cBPF filter for opcode gating + BPF event-loop for submit batching.

---

## 7. Overhead and performance

### Submitter-side cost

The cBPF filter executes inside the `io_submit_sqes()` path, under the `io_ring_ctx` submit lock on the submission thread.

- **Typical opcode filter:** 3–5 cBPF instructions (compare opcode, branch to allow/deny). Overhead: ~20–40 ns per SQE.
- **Complex parameter-filter:** up to 4096 bytes of cBPF instructions. Still bounded — cBPF interpreter has no indirect branches — but worst case adds ~500 ns/SQE at high submission batch sizes.
- **Locking contention:** if the filter touches `bpf_filter_list` (only at registration/unregistration, not per-execution), it does not add to submit-path latency.

### Comparison to eBPF verifier dispatch

Had this been eBPF:
- JIT or interpreter dispatch via bpf_prog_run.
- `bpf_prog_ops` lookup + security_bpf_prog hook on each SQE.
- Extra 50–150 ns per SQE due to verifier state checks at dispatch time.

The cBPF path deliberately avoids this to keep per-SQE overhead sub-microsecond.

### Zero-copy receive and the BPF filter

`IORING_OP_RECV_ZC` is a separate feature (merged in 6.15) that allows hardware RX to fill user-supplied pages directly. The BPF filter can gate `IORING_OP_RECV_ZC` independently from normal `readv`/`writev`, enabling a policy like "allow ZC receive only for registered sockets with MSG_ZEROCOPY".

The performance delta reported for io_uring ZC vs epoll is ~38–41% throughput improvement at 10GbE+ speeds; the filter adds constant overhead that does not change with packet size.

---

## 8. Key kernel implementation files

| File | Role |
|---|---|
| `io_uring/bpf_filter.c` | Core filter walk + cBPF execution wrapper |
| `io_uring/register.c` | `IORING_REGISTER_BPF_FILTER` handler |
| `include/uapi/linux/io_uring/bpf_filter.h` | User ABI for `struct io_uring_bpf_ctx` |
| `io_uring/tctx.c` | Per-task context for filter refcount on fork |
| `kernel/fork.c` | *_IORING filter list refcount inheritance during `copy_process` |
| `io_uring/io_uring.c` | `io_sq_wq_submit_work()` — SQE dispatch gate where filter checks fire |

Default filter ABI version check:
- `pdu_size` in `struct io_uring_bpf_ctx` tells the filter what the kernel supports.
- v7 initial value encodes `opcode/flags/ioprio/off/len/rw_flags/file_index/buf_index/personality/fixed_file/rw/poll_op/op_flags/addr_len/msg_flags/addr/user_data + pdu_size`.

---

## 9. Security audit considerations

### What the filter trusts

The filter trusts the kernel's `struct io_uring_bpf_ctx` snapshot. If anything corrupts the SQE between snapshot and execution, the filter's decision is based on stale data. Threat model:

- **Concurrent submit thread:** Two threads sharing one io_uring fd. Thread A submits SQE for `IORING_OP_WRITE`, thread B submits SQE for `IORING_OP_OPENAT`. Both pass through the submit path. The filter sees each SQE independently — no cross-SQE race within a single filter invocation.
- **SQPOLL race:** When `IORING_SETUP_SQPOLL` is active, the kernel polls the SQ from a dedicated thread. The filter must handle the case where `sqe->opcode` is read but `len`/`addr` reference memory that the application is concurrently updating.

### Safe filter patterns

```c
// Pattern 1: opcode allowlist (simplest strong policy)
if (opcode != READ && opcode != WRITE && opcode != POLL_ADD && opcode != CLOSE)
    return 0;  // deny

// Pattern 2: zero-copy receive only for fixed pre-registered FDs
if (opcode == RECV_ZC && !fixed_file)
    return 0;

// Pattern 3: deny FS-changing opcodes in unprivileged context
if (opcode == OPENAT || opcode == UNLINKAT || opcode == MKDIRAT)
    return 0;
```

The filter enables policy as code with a minimal, auditable surface area.

---

## 10. References and further reading

- Jens Axboe v7 patchset announcement: https://lore.kernel.org/io-uring/20260127183311.86505-1-axboe@kernel.dk/
- LWN coverage: https://lwn.net/Articles/1056226/
- Byteiota developer guide: https://byteiota.com/linux-7-iouring-bpf-filtering-zero-copy-developer-guide/
- Linux kernel `io_uring/bpf_filter.c` — main implementation (for-7.0/io_uring branch)
- `include/uapi/linux/io_uring/bpf_filter.h` — ABI header
- io_uring man page: https://man7.org/linux/man-pages/man7/io_uring.7.html
- `bpf-io_uring-event-loop-mechanics` skill — companion on BPF `struct_ops` event loop
