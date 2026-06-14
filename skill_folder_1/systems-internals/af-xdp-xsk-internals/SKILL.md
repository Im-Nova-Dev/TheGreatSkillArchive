---
name: af-xdp-xsk-internals
description: >
  Teach Linux AF_XDP / XSK zero-copy and copy-mode internals at the mechanistic
  level: XDP_REDIRECT routing via XSKMAP, UMEM shared-UMEM ownership, the FILL /
  RX / TX / COMPLETION ring state machine, ndo_bpf/ndo_xdp_xmit driver hooks,
  XDP_ZEROCOPY vs XDP_SKB fallback, multi-buffer frame fragmentation, and
  need_wakeup / busy-poll interactions. Targets kernel developers, high-performance
  networking engineers, and systems programmers who need to read
  tools/testing/selftests/bpf/xsk.h, libbpf/xsk.c, and driver ndo_xdp code.
trigger: >
  questions about AF_XDP, XSK, zero-copy user-space networking, XDP_REDIRECT to
  XSKMAP, UMEM rings, XDP_ZEROCOPY vs XDP_COPY, multi-buffer packets, ndo_bpf /
  ndo_xdp_xmit, shared UMEM, need_wakeup, busy-poll XDP, or high-performance
  packet receive/transmit in kernel 6.x.
---

# AF_XDP / XSK Internals

## Scope
Mechanistic how-it-works of Linux AF_XDP sockets. Not a usage guide—covers data
structures, ring protocols, driver contract, fallback paths, and concurrency
pitfalls at the boundary between the kernel network stack and user-space datapath.

## Prerequisites
- XDP hooks (`xdp_frame`, `xdp_buff`, `XDP_PASS`, `XDP_DROP`, `XDP_REDIRECT`).
- eBPF maps, especially `BPF_MAP_TYPE_XSKMAP`.
- `struct sk_buff` / NAPI / softirq model.
- `poll()` / busy-poll / busy-read user-visible semantics.
- DMA, page pinning, and netdev refcounting.

---

## Lesson 1: What AF_XDP actually sells
AF_XDP sockets bypass most of the kernel network stack by having an XDP program
redirect frames into a user-space visible region (UMEM). Two planes:
- Control plane: bind XSK to `(netdev, queue_id)`; install XDP program; populate
  XSKMAP entries.
- Data plane: FILL/RX/TX/COMPLETION rings move packets through a shared memory
  window without per-packet syscalls.

Differentiation from ZCRX: ZCRX stays in the socket path with io_uring as the
transport. AF_XDP is socket-free in the sense that classical sockets aren’t
involved—the transport to and from user-space is a BPF redirect plus mmap’d rings.

---

## Lesson 2: UMEM and frame geometry
`struct xsk_umem` owns a contiguous `mmap()` region subdivided into fixed-size
frames. Typically 2KiB or 4KiB, configured through `XDP_UMEM_REG`.

Key fields and invariants:
- `frame_size`: only powers-of-two, typically 2048 or 4096; larger than MTU
  frames that exceed `frame_size` become multi-buffer.
- `frame_headroom`: bytes left unused at buffer start for metadata (e.g., a
  virtio-net header).
- `headroom + actual_len` must fit the frame; otherwise the buffer is rejected
  during FILL add.

Shared UMEM:
- `XDP_SHARED_UMEM` allows multiple XSKs on the same netdev/queue or different
  queues/netdevs to reuse the same UMEM and FILL/COMPLETION rings.
- Only one process/thread may drive the FILL and COMPLETION rings for a given
  UMEM—they are single-producer/single-consumer.
- Violating this serialization causes lost refills or double-return of frames to
  the driver.

---

## Lesson 3: Ring protocols
Four rings total. All are mmap’d, power-of-two sized, single-producer/single-consumer.

- **FILL**: user-space pushes free frame addresses into kernel.
  The kernel masks lower `log2(frame_size)` bits in aligned-mode; unaligned mode
  leaves addresses untouched. Batched `xsk_ring_prod__reserve()` / `xsk_ring_prod__submit()`
  sequences allow submitting multiple frames per wake.
- **RX**: kernel posts `struct xdp_desc { addr, len }` indicating where a newly
  received packet lives in UMEM.
- **TX**: user-space posts `struct xdp_desc` requesting transmission.
- **COMPLETION**: kernel returns formerly-TX UMEM addresses for reuse only after
  the driver reports successful DMA.

The invariant: frames in COMPLETION may be re-queued via FILL. Frames in RX must
be returned by user-space through FILL after consumption. If user-space exceeds
FILL capacity, the driver runs out of RX slots and silently drops frames.

---

## Lesson 4: XDP_REDIRECT → XSKMAP routing mechanics
An XDP program decides where packets go:
- `bpf_redirect_map(&xsk_map, index, 0)` redirects to the XSK bound at map index.
- The kernel checks that the XSK is bound to the same `(netdev, queue_id)` as
  the current packet; otherwise the packet follows `XDP_ABORTED` / `XDP_PASS`.
- The redirect is aborted if the target XSK has zero fill slots.

`ndo_xdp_xmit` is invoked in zero-copy mode for TX from user space.

---

## Lesson 5: XDP_ZEROCOPY vs XDP_COPY vs XDP_SKB fallback
Bind-time selection via `sockaddr_xdp.sxdp_flags`:

- `XDP_ZEROCOPY` requests zero-copy: the NIC DMA writes directly into UMEM
  frames. Requires `ndo_bpf` and driver-reported zero-copy capability.
- `XDP_COPY` forces software copy into UMEM. Bind fails if the driver can’t
  support copy-mode (unusual; most support both modes via `XDP_SKB`).
- When zero-copy is impossible, the kernel uses `XDP_SKB` and allocates a real
  `sk_buff`, copies into UMEM, and then posts RX descriptor—but this adds a
  sk_buff allocation and an extra memcpy per packet.

The bind-failure path:
- `bind()` returns `-ENOTSUP` for `XDP_ZEROCOPY` if the driver reports
  `XDP_OPTIONS_ZEROCOPY` unsupported.
- If the caller doesn’t handle this and falls back naively to XDP_SKB, it
  unintentionally enters the high-overhead path.

Why `IORING_SETUP_SINGLE_ISSUER` analogy: in XDP, the umpire is the
`FILL/COMPLETION` serialization rule; any multi-thread app must pin the ring
management thread.

---

## Lesson 6: Multi-buffer frames in zero-copy mode (driver behavior)
When `len > frame_size`, the driver must scatter the packet across multiple
UMEM frames:

1. `xdp_desc` for the first frame: `len` is still the total packet length.
2. Additional follow-on frames are chained using `xdp_desc` back-to-back with
   the `XDP_PKT_CONTD` flag set.
3. User-space must walk the chain, stitch buffers together, and then return all
   frames back to FILL at once. Forgetting one frame silently orphans it.
4. In copy-mode, the kernel performs the defrag for you.

Drivers that advertise `XDP_OPTIONS_ZEROCOPY` still require this user-space
defrag if they support multi-buffer frames (notable on Mellanox mlx5 and Intel
i40e with jumbo frames).

---

## Lesson 7: Driver model hooks and memory ordering
- `ndo_bpf(xsk, xdp, xdp_prog)`: installs XDP program; responsible for verifying
  compatible XDP flags.
- `ndo_xdp_xmit(dev, queue, xdp_frame, flags)`: transmits via XDP path; returns
  `NETDEV_TX_OK` or `NETDEV_TX_BUSY`. In zero-copy mode there is a page-pin /
  DMA requirement similar to ZCRX.
- `xsk->dev` pointer is RCU protected; lookups must be under `rcu_read_lock()`.

Memory-ordering constraint:
- Kernel writes UMEM frame contents from NIC DMA before placing `xdp_desc` in RX.
- User-space must not consume the frame until the CPU sees RX (implicitly
  enforced by the ring order, but explicit barrier may be needed if the UMEM is
  accessed from outside the ring consumer loop).
- FILL ring entries must be visible to the kernel before returning from the
  userspace `sendmsg()`/`write()` path that pushes them; typically an implicit
  barrier from the syscall is sufficient.

---

## Lesson 8: need_wakeup and busy-poll budget interaction
`XDP_USE_NEED_WAKEUP` attaches a flag to FILL and TX rings:
- FILL flag set: kernel RX is backpressured; user-space must `poll()` to wake
  the driver’s NAPI/poll thread before more RX can flow.
- TX flag set: TX ring needs a wake; user-space must call `sendmsg()` or trigger
  `ndo_xdp_xmit` drain.

Busy-poll (`SO_PREFER_BUSY_POLL`, `busy-poll` budget on netdev):
- Busy poll and need_wakeup can conflict: if userspace polls with a large
  budget, the kernel deprioritizes FILL wakers. Tuning `rx_busy_poll` 50us
  + `need_wakeup` reduces unnecessary syscalls on lightly loaded servers.

---

## Lesson 9: Debugging AF_XDP and common failure signatures
- `bind() -> -ENOTSUP` for `XDP_ZEROCOPY`: check `ethtool -k` for `rx-hashing`
  and `rx-vlan-filter`, and `ethtool -i` for driver-supported XDP modes.
- RX stalls: FILL ring is empty; verify single-producer rule and check ring
  consumer index progression with `bpftrace`.
- TX stalls: `ndo_xdp_xmit` returns `NETDEV_TX_BUSY`; check for backlog or
  `XDP_USE_NEED_WAKEUP` assertion.
- Multi-buffer fragments: driver publishes `XDP_PKT_CONTD`; you must walk the
  RX ring sequentially and stitch frames.

```bpftrace
tracepoint:skb:skb_copy_datagram_iovec
/args->sk && comm == "xsk_app"/
{
  @bad_fallback[comm] = count();
}
```

---

## Lesson 10: Exercises / thought problems
1. Draw the timeline for a single packet in zero-copy mode, from NIC DMA into
   UMEM, through XDP_REDIRECT/XSKMAP, to user-space RX ring, and back through
   FILL after consumption. Mark the driver and user-space memory barriers.
2. Why can two threads concurrently producing into the same FILL ring cause
   corruption? How would you extend libxdp to add a thread-safe front-end?
3. With shared UMEM across 4 XSKs on different queues, why is only one FILL
   ring producer allowed per netdev/queue tuple? What would break if you allowed
   two producers?
4. Explain why multi-buffer zero-copy mode forces user-space defrag; why doesn’t
   the kernel expose the chained `xdp_desc` frames via a special ring layout
   instead of packing them contiguously in UMEM?
5. If a user-space transmitters drops `ndo_xdp_xmit`, write an eBPF tracepoint
   to count `NETDEV_TX_BUSY` returns for an XSK’s TX ring and measure the
   correlation with FILL ring depth.
6. `XDP_OPTIONS_ZEROCOPY` has a known kludge: some drivers expose it only when
   the queue is in an “up” state. What race exists between `netdev_up` and
   `xsk_bind()`?