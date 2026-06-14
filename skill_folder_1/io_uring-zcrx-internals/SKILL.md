---
name: io_uring-zcrx-internals
description: >
  Teach Linux io_uring zero-copy receive (ZCRX) internals at the mechanistic level:
  NIC hardware requirements, page-pool lifetime owned by io_uring, refill queue,
  freelist reference counting, the CVE-2026-43121 freelist race and atomic cmpxchg
  fix, the Large Receive Buffer (LRB) extension for >4KiB frames, scatter-gather
  consequences, and defensive kernel patterns. Emphasizes how DMA, page pools,
  higher-order allocations, and object lifetime rules interact to break or preserve
  safety invariants.
trigger: >
  questions about io_uring ZCRX, zero-copy network receive, devmem TCP differences,
  page_pool + net_iov lifetimes, io_uring networking fast paths, CVE-2026-43121,
  freelist races in kernel networking code, or NIC header/data split requirements.
---

# io_uring ZCRX Internals

## Scope
Mechanistic how-it-works of Linux io_uring zero-copy receive (ZCRX). Not a usage tutorial —
this covers object lifetime, hardware preconditions, kernel data structures, concurrency
pitfalls, and exploit-relevant failure modes.

## Prerequisites
- Linux kernel networking stack basics (`struct sk_buff`, softirq, NAPI, RSS).
- io_uring instance and SQ/CQE model.
- DMA fundamentals and page pinning.
- Atomic primitives: `atomic_read`, `atomic_dec`, `atomic_try_cmpxchg`.

## Lesson 1: What ZCRX actually eliminates
Standard TCP receive copies payload from kernel page cache to userspace buffer:
`skb_copy_datagram_iter()` or `copy_page_to_iter()` path.
ZCRX arranges for the NIC to DMA packet payload directly into userspace `mmap()`'d pages.
Kernel keeps headers in kernel memory; userspace gets payload offset via CQE extras.

Why not just `TCP_ZEROCOPY_RECEIVE`?
- Requires strict alignment and mmap of a `tcp_zerocopy_receive` area.
- Lifetime tied to socket, not io_uring instance.
- ZCRX uses io_uring regions / refill queues and avoids `mmap` on the socket fd itself.

Why not DPDK?
- DPDK bypasses kernel TCP stack entirely.
- ZCRX retains kernel TCP processing: flow control, retransmit, congestion control,
  socket options, epoll/io_uring integration, cgroup accounting.

## Lesson 2: Hardware preconditions (non-negotiable)
ZCRX does not configure the NIC; userspace does out-of-band via ethtool/netlink:

1. **Header/Data Split** — NIC must split packet at L4 boundary; headers to kernel,
   payload to userspace page.
2. **Flow Steering** — only specific flows must land on ZC Rx queues.
3. **RSS** — non-ZC flows must be steered *away* from ZC Rx-configured queues.

`ethtool` knobs (example):
- `ethtool -G eth0 tcp-data-split on`
- `ethtool -X eth0 equal 1` then `ethtool -N eth0 flow-type tcp6 ... action 1`

## Lesson 3: Object model and lifetime
The critical invariant is that the io_uring instance owns everything related to ZCRX:

- Userspace `mmap()` area: memory for payloads.
- Refill ring: shared `struct io_uring_zcrx_rqe[]` plus khead/ktail pointers mapped back.
- `struct net_iov` (`niov`): describes one payload buffer + hardware rx descriptor ref.
- Page pool (`page_pool`): provides pages; `net_iov` has a `page_pool` back-pointer.

`niov` reference counting (`user_refs`):
- Starts at some value when buffer is handed to userspace.
- Decremented when userspace releases buffer on refill ring.
- Scrub path (`io_zcrx_scrub`) runs at io_uring exit to return all outstanding buffers.

The invariant:
> For every `niov`, the final 1→0 transition must happen exactly once, and the `niov`
> must be pushed onto the freelist exactly once.

## Lesson 4: The reference-count race (CVE-2026-43121)

### Vulnerable flow
Two CPU contexts:
- **Refill path**: userspace posts consumed buffers back; kernel reads `user_refs`,
  decrements, then checks if zero.
- **Scrub path**: io_uring instance is closing; `scrub()` atomically exchanges all refs
  to zero and returns `niov`s.

Because read → dec → read is a three-step sequence, between dec and second read another
CPU can scrub the same `niov` first. Result:
1. `niov` returned to freelist by scrub.
2. Original CPU concludes refcount is zero and returns it again.
3. Freelist `free_count` now exceeds `nr_iovs`.
4. Later push writes a `u32` past end of `kvmalloc` freelist array → heap corruption.

### Why atomic_try_cmpxchg fixes it
Atomic Read-Modify-Write guarantees the compare-and-swap pair is indivisible:

```c
u32 refs = atomic_read(&niov->user_refs);
do {
    if (!refs)
        return;
} while (!atomic_try_cmpxchg(&niov->user_refs, &refs, refs - 1));
if (refs == 1)
    io_zcrx_return_niov(niov);
```

Only one winner transitions 1→0. Others observe a non-zero post-decrement value and
do not return the `niov` again.

## Lesson 5: Defensive patterns added upstream
- Root cause fix: atomic cmpxchg loop for reference transitions.
- Bounds check: `WARN_ON_ONCE(free_count >= num_niovs)` before freelist push.

These are defense-in-depth; the algorithmic invariant is the cmpxchg loop itself.

## Lesson 6: Exposure scope
- Confirmed working drivers: Broadcom bnxt, Google gve.
- WIP: Mellanox mlx5.
- Requires matching kernel/config, supported NIC, and `CAP_NET_ADMIN`.

## Lesson 7: Large receive buffer extension (LRB)
Target kernels: Linux 6.20 / 7.0+, commit `795663b4d160ba652959f1a46381c5e8b1342a53`
by Pavel Begunkov (Meta), queued via Jens Axboe `for-next`.

What changed:
- Prior to LRB, ZCRX buffers were effectively fixed at a single page (4 KiB).
- LRB allows the registered userspace ZC area to be backed by higher-order pages so
  that a single buffer holds >4 KiB of payload.
- `page_pool` allocation callback (`alloc_netmem`) now returns pages of `order >= 1`
  for ZC buffers when the NIC advertises `rx-buf-len > 4096`.
- The driver no longer populates one Rx descriptor per 4 KiB page; one descriptor may
  span multiple `bio_vec` segments.

Scatter-gather consequence:
- A ZC CQE no longer implies `off == 0` on the first `bio_vec`.
- Userspace must walk a small SG list to locate the data for that packet.
- The per-slot refill queue entry (`struct io_uring_zcrx_rqe`) still describes one
  buffer slot; with larger buffers the same number of refill entries covers more
  payload, so freemem accounting changes from "entries == packets" to
  "entries == pages".

Copy-fallback changes:
- If userspace runs out of ZC area pages, the kernel copies from `sk_buff` page frags
  into pooled pages. LRB extends this because `sk_buff` frags are still typically
  4 KiB, so the fallback must assemble a multi-`bio_vec` destination for a single
  >4KiB frame.

Performance:
- Benchmarks with a 200 Gbps-class NIC show up to ~30% CPU util improvement for a
  single TCP flow moving from 4 KiB to 32 KiB Rx buffers.

Hardware prerequisites in addition to Lesson 2:
- NIC must report larger receive buffers via ethtool (`ethtool -g`).
- `tcp-data-split` and RSS constraints still apply.
- TSO/GRO and `gso_max_size` can clip effective payload size before data reaches the
  ZC queue, so larger buffer availability only matters for frames that survive those
  stages unscathed.

## Exercises / thought problems
1. Sketch a timeline with two CPUs showing how read → dec → read interleaves with
   `atomic_xchg` in scrub to produce double-return.
2. If `nr_iovs = 1024` and freelist array is `kvmalloc`'d, roughly how far past the end
   does the 4-byte overflow write? What allocator metadata typically lives there?
3. Why does `IORING_SETUP_SINGLE_ISSUER` not prevent the race? What does it actually
   constrain?
4. Design a minimal `bpftrace` script to trace `io_zcrx_return_niov` calls and detect
   `free_count > num_niovs` violations.
5. With LRB enabled, explain why the CQE `off` field can be non-zero and how the
   userspace consumer must walk SG segments to assemble the full payload.
6. List the ways higher-order page allocation in the ZC page pool can stress the
   buddy allocator under memory pressure, and why `PP_FLAG_PAGE_FRAG` becomes load-
   bearing for correctness rather than optimization.
7. With DMABUF-backed ZCRX enabled (Linux 6.16+), walk the lifetime of a buffer that
   is shared between the networking Rx path and a V4L2 decoder. Who calls
   `dma_buf_begin_cpu_access()` and `dma_buf_end_cpu_access()`, and what can go
   wrong if the NIC DMA writes while a userspace consumer still holds the buffer
   under `DMA_BUF_ATTACH` but not `DMA_BUF_IOCTL_SYNC`?
8. Explain why the NIC's DMA mask sets an upper bound on the dma_buf physical address
   usable with ZCRX, and what kernel code (`dma_map_resource` / `dma_map_page`) is
   reached when the exporter is not DMA-coherent.
