---
title: AF_XDP and io_uring ZC Rx Internals
description: Mechanistic deep dive into AF_XDP/XSK zero-copy packet path, SPSC ring semantics, XDP_NEED_WAKEUP busy-poll tuning, and the io_uring zero-copy receive refill queue plus freelist race conditions.
triggers:
  - AF_XDP
  - XSK
  - io_uring zero copy receive
  - ZC Rx
  - page pool refill
  - zero copy network
  - busy poll need_wakeup
  - freelist race
  - net_iov
  - SPSC ring
  - io_recvzc
  - dma map page
  - packet bypass
---

# AF_XDP and io_uring ZC Rx Internals

## Scope and rules of engagement

This note is about *how* packets get from NIC DMA to userspace without copies, and where the invariants actually live. It is not a tutorial on libbpf or liburing setup. Target audience: systems engineers and advanced CS students.

Key mechanical topics covered:
- UMEM layout, chunk encoding, and mmap'd ring geometry.
- SPSC ring assumptions, what the kernel checks, and what bugs arise when those assumptions break.
- AF_XDP zero-copy path prerequisites: driver support, header/data split, and `XDP_NEED_WAKEUP` semantics at the driver/kernel boundary.
- io_uring ZC Rx (`io_recvzc`) page-pool refill and the freelist "four bytes past the edge" descriptor race.

---

## 1. AF_XDP memory substrate: UMEM and rings

### 1.1 UMEM layout

- User allocates a contiguous virtual memory region and registers it via `XDP_UMEM_REG`.
- The region is divided into equal-size frames (chunks). Only power-of-2 sizes between 2048 and system page size are supported at this time (~4096).
- Each chunk can carry a headroom at the start for metadata. The rest holds packet payload.
- The kernel does not allocate its own copies when in zero-copy mode; the packet data in UMEM is the *same* memory the NIC DMA'd into.
- UMEM lifetime is decoupled from individual XSKs. One UMEM can back multiple XSKs, but rings are each singly owned. FILL/COMPLETION rings are shared per UMEM; RX/TX rings are per socket.

### 1.2 Ring mechanics

- Four rings, all SPSC (single producer / single consumer), power-of-2 sized, mmapped from the socket fd.
- Each ring uses producer/consumer pointer pairs. The kernel and userspace each own one side; the mapping is established via `XDP_MMAP_OFFSETS`.
- Ring entries on RX are `struct xdp_desc { __u64 addr; __u32 len; __u32 options; }`.
- `addr` encodes an offset into UMEM. In *aligned chunk mode* the log2(chunk_size) LSBs are ignored by kernel and driver. That means chunk address 0x...2000, 0x...2002, ...0x...3000 all resolve to the same 2K frame when `chunk_size=2048`. This is the single biggest source of descriptor confusion: the address you read from RX may not be exactly the one you put on FILL, but it designates the same frame.

### 1.3 SPSC correctness criteria

- No locks on the fast path because exactly one writer and one reader exist.
- Required ordering constraints:
  - Producer writes descriptor, then `smp_wmb()`, then advances producer index.
  - Consumer reads producer index, `smp_rmb()`, then reads descriptor.
- Losing either barrier means the consumer sees stale data or sees a new descriptor only after the producer has already overwritten it.
- Driver rx path is *concurrent* with user-space fill path, which is why FILL ring correctness depends on the kernel's consumption of descriptors being strictly ordered with respect to the hardware.

---

## 2. AF_XDP zero-copy path: from NIC DMA to user-space

### 2.1 Hardware prerequisites

- **Native XDP support**: The driver must implement the XDP ndo operation. Otherwise the socket falls back to `XDP_SKB` copy mode.
- **Header/data split**: To keep packet headers in kernel memory while delivering payload to UMEM, modern NICs split packet buffers at a configurable offset. This is required because the kernel's network stack still needs to parse headers (TCP options, VLAN, etc.).
- **Flow steering / RSS**: Desired flows are steered to specific hw rx queues that have UMEM backing instead of the default skb allocator. Configuration of steering is outside the AF_XDP path; user programs typically use ethtool or tc to match flows.
- **DMA coherence**: The NIC writes to the UMEM frame using DMA. UMEM must reside in DMA-coherent memory, and the driver must perform the appropriate `dma_map_page`/`dma_unmap_page` dance around the transfer.

### 2.2 Zero-copy rx queue entry flow

1. User-space publishes empty UMEM frame addresses on the FILL ring.
2. The kernel's AF_XDP core and the driver's rx path drain FILL into a driver-internal freelist.
3. On packet arrival, the hw dma writes payload into the frame. Header data is copied into a kernel skb fragment for layer 3+ processing.
4. The driver posts an `xdp_desc` onto the XSK's RX ring with ` addr = frame_offset + headroom` and `len = payload len`.
5. User-space reads the RX ring, consumes the packet in-place, then places the same frame address back onto the FILL ring for reuse.

### 2.3 `XDP_NEED_WAKEUP` and busy-poll semantics

- When the user process does not call `poll()`/`epoll()` continuously, the kernel may signal the NIC that the rx queue is idle. This typically causes the NIC to stop DMA'ing new packets into UMEM, since the driver's freelist is empty.
- `XDP_NEED_WAKEUP` is a socket option flag that tells the kernel to track whether the hw rx queue has been "tickled" recently.
- If the driver sees the FILL ring is empty and `XDP_NEED_WAKEUP` is on, it sets an internal `need_wakeup` counter. The kernel then broadcasts a wakeup event to the user-space poller. The user-space then refills FILL and issues the `sendto()`/`poll()` wakeup syscall that tells the NIC to resume DMA.
- The cost model: if your userspace is polling aggressively (busy poll), you usually *disable* `XDP_NEED_WAKEUP` and rely on constant rx interrupts to keep the queue fed. If you use epoll wakeups, you need it.
- The busy-poll path uses `sock_flag` bits and netdev `priv_flags` to short-circuit the wakeup checks on the hot path.

---

## 3. io_uring ZC Rx: page-pool refill and the freelist race

### 3.1 Design goals

- Allow a socket `read()` to act purely as a *notification*: the data already resides in user memory, made reachable by a DMA from the hw rx queue; the `read()` just returns the buffer location and length.
- Object lifetime is bound to an io_uring instance, not to traditional `struct sk_buff`.
- Uses a new request type: `io_recvzc`.

### 3.2 Page-pool refill mechanics

- A zero-copy page pool is created. Unlike the traditional net page pool, this variant supplies user pages.
- Driver exposes a hw rx queue that can be populated from this user-backed page pool (via `page_pool_refill_*` helpers and the netdev memory provider API).
- New shared refill queue: completed buffers flow back to the page pool and can be handed out to the hw rx queue again.
- Refcounting is done via `net_iov` (network I/O vector) structures, which track both kernel and user references. The `page_pool_ref_netmem` helpers manage the transition between refcount domains.

### 3.3 The "four bytes past the edge" freelist race

This is the subtle kernel bug/class of defect that arises because:

- Descriptor chunks are power-of-2 aligned. The freelist uses the lower bits of a dma address to encode flags or next-pointer state when in aligned mode.
- When an `xdp_desc` address is masked to resolve to a chunk, the freelist entry is the last few bytes of that chunk's metadata region.
- A race can occur if:
  1. A user-space process recycles a frame back to FILL before the driver has finished consuming the previous rx descriptor.
  2. The driver writes a new `xdp_desc` header word-length (4 bytes) past the expected boundary because of alignment or a stale freelist tail pointer.
- The visible consequence is descriptor corruption on the next slot: `len` overwritten, `addr` pointing to the wrong frame, or kernel OOPS due to `dma_unmap_page` on the wrong page.
- The fix pattern is to fence the freelist cursor with an explicit pointer-size write and to mask `addr` on both producer and consumer sides using `chunk_mask = ~(chunk_size - 1)`. Losing the mask on either side produces the off-by-one descriptor smash.

### 3.4 Refcount domain crossing

- A buffer in UMEM is visible to:
  1. The NIC (via DMA)
  2. The kernel network stack (as a page in the page pool)
  3. User-space (as application memory)
- The kernel and userspace maintain distinct references. The socket/io_uring core keeps a per-IO reference. The kernel must not free or re-dma a page while user-space still holds a valid reference to it.
- The `net_iov` structure carries this state. When `io_recvzc` completes, the reference is transferred back to the user-space address space, and the page pool releases its dma mapping only after all kernel-side users are done.

---

## 4. Cross-cutting invariants

| Property | AF_XDP path | io_uring ZC Rx |
|---|---|---|
| Copy elimination | Yes, driver DMA directly into UMEM | Yes, via user-backed page pool |
| Kernel users of packet data | Header split into skb fragment | Header split into skb fragment (similar path) |
| User notification mechanism | RX ring mmap + epoll | `io_recvzc` CQE |
| Buffer return to hw queue | FILL ring | Shared refill queue |
| Key prerequisite | Native driver XDP + header/data split | Header/data split + hw queue bound to zc page pool |
| C-State sensitivity | High; busy poll removes CPU idle | High; same rx softirq path |

---

## 5. Debug and verification approaches

- Verify driver fill correctness with `xdpdump` or `AF_XDP bpf_link` tracepoints.
- Use `bpftrace` on `xdp:redirect_err` to confirm no tail drops on FILL exhaustion.
- Inspect netdev memory provider state via `ethtool -S` if exposed by the driver.
- For io_uring ZC Rx, enable `CONFIG_DEBUG_NET` and check `net/core/page_pool_user.c` for refcount checks.
- Reproduce the freelist race by running two processes sharing UMEM where one process refills at maximum speed while the other drains RX with an artificial sleep before refill. Core dump / kasan will flag the descriptor corruption.

---

## 6. References and further reading

- LWN article on io_uring ZC Rx v10: https://lwn.net/Articles/1004591/
- Kernel docs: io_uring ZC Rx: https://docs.kernel.org/networking/iou-zcrx.html
- Kernel docs: AF_XDP internals
- Penligent write-up: io_uring ZCRX freelist race, "Four Bytes Past the Edge"
- arXiv 2402.10513: Understanding Delays in AF_XDP-based Applications (busy poll / need_wakeup combination)
- SoK: Challenges and Paths Toward Memory Safety for eBPF (Oakland 2025)
