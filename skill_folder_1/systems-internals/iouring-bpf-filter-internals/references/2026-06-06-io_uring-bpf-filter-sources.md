# io_uring cBPF Filter — Source Reference Notes

Date: 2026-06-06
Scope: sources and key signal used to build the `iouring-bpf-filter-internals` teaching note.

## Primary sources

- Jens Axboe, "[PATCHSET v7] Inherited restrictions and BPF filtering for io_uring", linux-io-uring mailing list, 2026-01-27.
  - https://lore.kernel.org/io-uring/20260127183311.86505-1-axboe@kernel.dk/
  - 18 files changed, 788 insertions. Added `io_uring/bpf_filter.c`, `include/uapi/linux/io_uring/bpf_filter.h`, fork inheritance in `kernel/fork.c`, and `IORING_REGISTER_BPF_FILTER` in `io_uring/register.c`.

- LWN, "Inherited restrictions and BPF filtering for io_uring", 2026-01-27.
  - https://lwn.net/Articles/1056226/
  - Summarizes the v7 patchset. Notes the cBPF design choice and the `pdu_size` forward-compatibility field.

- Byteiota, "Linux 7.0 io_uring: BPF Filtering Ends the Security Debate", 2026-04-21.
  - https://byteiota.com/linux-7-iouring-bpf-filtering-zero-copy-developer-guide/
  - Developer-oriented guide covering seccomp pre/post-7.0, container posture, and the other 7.0 io_uring features (`IORING_OP_RECV_ZC`, IOPOLL hash-table upgrade). Overhead numbers for io_uring ZC vs epoll come from this guide.

## Kernel files referenced

- `io_uring/bpf_filter.c` — per-SQE cBPF walk and allow/deny decision.
- `io_uring/register.c` — `IORING_REGISTER_BPF_FILTER` handler.
- `include/uapi/linux/io_uring/bpf_filter.h` — `struct io_uring_bpf_ctx` ABI.
- `io_uring/tctx.c` — per-task context used for filter refcount handling.
- `kernel/fork.c` — filter refcount inheritance during `copy_process()`.
- `io_uring/io_uring.c` — SQE dispatch gate where filter checks fire.

## ABI excerpt: `struct io_uring_bpf_ctx` (v7)

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
    __u32   pdu_size;
};
```

## Signal strength

High. Merged in 7.0 (April 2026), authored by the io_uring maintainer, security impact is concrete, and the ABI is small enough to teach mechanistically.
