# Teaching elevator: io_uring Zero-Copy Receive Buffer Mechanics

Lecture format for an OS internals course covering networking and I/O subsystems.
Prerequisites: userspace/kernel boundary, DMA concepts, `io_uring` submission/completion rings, memory barriers.

---

## Opening hook

Most students learn io_uring as "asynchronous read/write via shared rings." The surprising power of io_uring (and the reason it beats epoll/POSIX AIO for networking) is that the kernel can hand you *the physical DMA address* of a packet, not a copy. The buffer is yours from instant the NIC writes it.

Show the LPC 2023 paper: "Zero Copy Rx with io_uring." One sentence guts the model:

> Data lives in userspace; the kernel is a notification service.

This lecture explains what that means at the byte level.

---

## Module 1: Why normal socket RX copies at all

Review socket() -> recv() path:
1. NIC DMA writes to kernel page -> fills `sk_buff`.
2. Data is copied/carved into user buffer via `tcp_copy_to_user`.
3. Cost: two memory domains (kernel page, user page), extra cache lines, extra TLB.

`TCP_ZEROCOPY_RECEIVE` exists but has the wrong shape:
- Requires aligned 4KB or larger blocks.
- Needs a kernel mmap'ed FIFO.
- Uses `iovec`-array protocol, still a data-plane copy in some paths.

io_uring ZC Rx removes the copy entirely *and* removes the mmap-to-an-fd complexity.

---

## Module 2: The hardware contract (NIC must do this)

Hand out a slide with three mandatory NIC features:
1. **Header/data split** at L4 boundary.
   - Why: kernel TCP stack needs headers to maintain connection state.
   - What hardware does: L2/L3/L4 metadata to internal SRAM, payload to DRAM pointed by `page->addr`.
2. **Flow steering** to a dedicated HW Rx queue.
3. **RSS** that excludes non-ZC flows from that queue.

If one of these is missing, ZC Rx cannot start. Point out the `ethtool` checklist verbatim.

---

## Module 3: The five uAPI objects

Walk this table slowly:

| Object | Kernel role | Userspace role |
|---|---|---|
| Data area | DMA target | Read packets from |
| Refill ring | Reclaim freed ZC pages | Post freed buffers |
| `area_reg` | Maps area into network path | Provides mmap'd pointer + len |
| `region_reg` | Maps refill ring | Provides ring buffer region |
| `ifq_reg` | Binds area+region to a HW queue + ifindex | Says "queue 1 on eth0" |

Derive the math for ring size with the class:
```c
ring_size = rq_entries * sizeof(struct io_uring_zcrx_rqe) + PAGE_SIZE;
ring_size = ALIGN_UP(ring_size, PAGE_SIZE);
```
Ask: why + PAGE_SIZE? -> answer: ring header lives before the array to keep cache-line alignment of the hot head/tail fields.

---

## Module 4: Receiving one packet (step by step)

1. Application submits `IORING_OP_RECV_ZC` with `IORING_RECV_MULTISHOT`.
2. Kernel sees no active SQE -> issues a "prepared receive" on the NIC's ZC HW queue.
3. NIC DMA writes payload into the *next free* ZC page from the page pool.
4. NAPI pulls completion, posts CQE.
5. CQE followed by `io_uring_zcrx_cqe = { buf_off , area_id }`.
6. Application computes payload address: `area[area_id] + (buf_off & mask)`.
7. Application processes payload.
8. After processing, application advances refill-ring tail, giving that page back to the kernel.
9. Kernel's page pool refill posts the page back to the NIC HW Rx ring.

Emphasize: **(6)** is *not* a `memcpy`. The application pointer IS the DMA'd memory.

---

## Module 5: The freelist race (why this matters for security)

Show the CVE-2026-43121 frame:
- Between steps (7) and (8), the application can be preempted, or can have another thread re-use the refill-ring slot via a TOCTOU.
- If the application accesses the page after (8) (use-after-free to kernel page pool), it can overwrite page freelist metadata because the same physical page is now reserved for the NEXT packet from the NIC.
- Result: heap spray via forged freelist pointers, or simple 4-byte corruption invisible to userspace sanitizers.

Teach mitigation pattern:
```c
void *pkt = area + offset;
/* read only */
consume_pkt(pkt, len);
/* barrier: ensure all loads from the ZC page happen before re-enqueue */
atomic_thread_fence(memory_order_acquire);
refill_and_advance_tail(page);
```

---

## Module 6: Large buffer extension — the buffer size dilemma

Linux 7.0 support for 32KB+ buffers raises a subtle PR question:
- Default 4KB page = lots of CQEs/RQEs = more scheduler wakeups = more CPU overhead.
- 32KB buffer = fewer ring events = less CPU but:
  - Higher latency variance if the NIC batches to 32KB.
  - Larger DMA-to-memory cache footprint per flow — less L1/L2 reuse.
  - `IORING_ZCRX_AREA_SHIFT` must change; all existing code assuming shift=12 is broken.

Walk through computing the new ring size for 200Gbps with 32KB buffers and N=1024.

---

## Module 7: Comparison to DP-DPDK-AF_XDP triangle

Draw three columns:
- **XDP/AF_XDP:** kernel still copies from NIC page into the xsk umem, but xsk is simpler; zero heap allocation in path *if* the frame fits in a pre-allocated chunk.
- **DPDK:** full bypass, no headers seen by kernel, no firewall/cgroups/netns.
- **io_uring ZC Rx:** headers stay in kernel for TCP/iptables/cgroup accounting; payload is a pointer with asynchronous completion semantics.

Link this to the `IORING_SETUP_SQPOLL` + `DEFER_TASKRUN` flags: the kernel chooses batch/time-driven completion draining, which is the right semantics for high-rate NICs where per-packet CQ processing is too expensive.

---

## Module 8: EEVDF / scheduler interaction

Key insight: multishot ZC Rx with 100k+ completions/s means the application thread and softirq share a CPU budget. Under:
- **EEVDF**: deadline can be pushed by ZC throughput because long `recv` loops hold CPU without `need_resched`; EEVDF only checks at tick or explicit yield in fair class.
- **Lazy preemption** (Linux 7.0 default): the combination defers reschedule until slice exhaustion. Multishot completions can run unbounded.
- **Result**: latency-sensitive receivers must yield via `io_uring_submit_and_wait_cancel` or `sched_yield` inside the polling loop to let EEVDF recompute.

---

## Module 9: Debugging recipe

1. Strip down: single core for app + softirq, single HW queue.
2. Confirm: `ethtool -S eth0 | grep zc` or driver-specific counters.
3. In `ftrace`: enable `napi_gro_receive`, `page_pool_refill`, and `io_uring_zcrx_complete` if tracepoints exist.
4. Watch the refill ring head/tail with `bpftrace`:
```c
tracepoint:io_uring:io_uring_zcrx_complete
{
   printf("area=%d off=%d\n", args->area_id, args->buf_off);
}
```
5. Monitor buffer occupancy:
   `ring_tail - ring_head = ~in-flight; if this grows unbounded, application is slower than NIC+DMA.`

---

## References section

- `networking/iou-zcrx.html` (kernel docs, Linux 7.1-rc6)
- LWN Articles/1004591: patchset v10 summary
- Phoronix: "IO_uring Zero-Copy Large Receive Buffer Support"
- Netdev 0x17 paper: "Zero Copy Rx with io_uring" (LPC 2023 PDF)
- David Wei's patches: `[PATCH net-next v10 00/22]`
- io_uring zcrx example tooling: `kperf` / patched `liburing`
