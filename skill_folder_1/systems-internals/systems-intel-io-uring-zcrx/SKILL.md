---
name: systems-intel-io-uring-zcrx
description: "Teach io_uring zero-copy receive (ZCRX): kernel-to-user copy elimination via direct DMA into userspace pages"
category: systems-internals
tags: [io_uring, networking, zero-copy, kernel, DMA, high-performance]
version: 1.0
---

# Teaching: io_uring Zero-Copy Receive (ZCRX)

## Learning Objectives
- Explain how ZCRX eliminates kernel-to-user copy on RX path
- Describe NIC hardware requirements (header/data split, flow steering, RSS)
- Walk through io_uring registration and buffer management uAPI
- Analyze performance characteristics vs epoll/TCP_ZEROCOPY_RECEIVE

## Prerequisites
- io_uring basics (submission/completion queues, SQE/CQE)
- Linux networking stack (sk_buff, NAPI, softirq)
- DMA and memory mapping concepts
- NIC hardware offload basics

## Core Concepts

### What ZCRX Actually Does
```
Traditional RX:     NIC → DMA → kernel pages → copy → userspace pages
ZCRX RX:           NIC → DMA → userspace pages (payload only)
                    Headers → kernel pages (normal TCP processing)
```

**Key distinction**: Kernel TCP stack still processes headers. Unlike DPDK/XDP, no kernel bypass.

### Hardware Requirements (Must Configure via `ethtool`)
| Feature | Purpose | ethtool Command |
|---------|---------|-----------------|
| Header/Data Split | Split at L4 boundary | `ethtool -G eth0 tcp-data-split on` |
| Flow Steering | Direct specific flows to ZC queues | `ethtool -N eth0 flow-type tcp6 ... action 1` |
| RSS | Steer non-ZC flows away | `ethtool -X eth0 equal 1` |

### io_uring Setup Flags (Required)
```c
IORING_SETUP_SINGLE_ISSUER | IORING_SETUP_DEFER_TASKRUN | IORING_SETUP_CQE32
```

### Memory Registration Flow
1. `mmap` anonymous area for DMA buffers
2. `mmap` refill ring (shared kernel↔user ringbuf)
3. `io_uring_register_ifq()` with interface index, RX queue, area/region descriptors
4. Kernel returns offsets → map refill ring head/tail/rqes pointers
5. Submit `IORING_OP_RECV_ZC` with `IORING_RECV_MULTISHOT`
6. Process 32-byte CQEs (16B ordinary + 16B `io_uring_zcrx_cqe`)
7. Recycle buffers via refill ring (atomic tail update + `IO_URING_WRITE_ONCE`)

## Teaching Flow (90 min)

### 1. Motivation (10 min)
- Copy bottleneck at 100Gbps+: `memcpy` burns CPU cycles
- `TCP_ZEROCOPY_RECEIVE` limitations: strict alignment, mmap overhead
- DPDK/XDP: kernel bypass, operational complexity

### 2. Hardware Deep Dive (20 min)
- Header/data split: NIC firmware capability, L3/L4 parsing
- RSS indirection table + flow steering: programmable filtering
- Queue topology: why ≥2 queues, how ZC queues carved out

### 3. uAPI Walkthrough (30 min)
- Memory area: chunked, physically contiguous, page-aligned
- Refill ring: custom ringbuf design, kernel fills offsets
- Registration struct hierarchy: area_reg → region_reg → ifq_reg
- CQE layout: 32 bytes, `io_uring_zcrx_cqe` fields (off, len, flags)
- Buffer recycling: token-based, area_offset + rq_area_token

### 4. Performance Analysis (15 min)
| Scenario | epoll | ZCRX | Delta |
|----------|-------|------|-------|
| App/softirq different cores | 82.2 Gbps | 116.2 Gbps | +41% |
| App/softirq same core | 62.6 Gbps | 80.9 Gbps | +29% |

- Why cross-core wins: softirq not competing with app for cache
- Why not higher: header processing still in kernel, interrupt overhead

### 5. Driver Landscape (10 min)
- bnxt (Broadcom): primary target, Taehee Yoo patches
- gve (Google): should work
- mlx5 (Mellanox): WIP

### 6. Failure Modes & Debugging (5 min)
- Copy fallback: ZC memory exhaustion, header split failure
- `ethtool -S` counters for ZC queue stats
- `io_uring` register debugfs

## Failure Modes & Security: CVE-2026-43224 (sgtable leak on mapping failures)

### Root Cause
Commit `439a98b972fbb` ("io_uring/zcrx: deduplicate area mapping") introduced a missing cleanup path in `io_zcrx_map_area()`:

```c
static int io_zcrx_map_area(struct io_zcrx_ifq *ifq, struct io_zcrx_area *area)
{
    // ...
    if (!area->mem.is_dmabuf) {
        ret = dma_map_sgtable(ifq->dev, &area->mem.page_sg_table,
                              DMA_FROM_DEVICE, IO_DMA_ATTR);
        if (ret < 0)
            return ret;  // sgtable INITIALIZED but NOT freed → LEAK
        // ...
    }
    ret = io_populate_area_dma(ifq, area, sgt, offset);
    if (ret == 0)
        area->is_mapped = true;
    return ret;
}
```

When `io_populate_area_dma()` fails (only on `PAGE_POOL_32BIT_ARCH_WITH_64BIT_DMA` builds), the initialized `page_sg_table` is leaked because cleanup in `io_zcrx_unmap_area()` is gated by `is_mapped` (only set on success).

### Fix (commits a983aae39776, ef075c1464ac, f1ae40332431)
```c
ret = io_populate_area_dma(ifq, area, sgt, offset);
+ if (ret && !area->mem.is_dmabuf)
+     dma_unmap_sgtable(ifq->dev, &area->mem.page_sg_table,
+                       DMA_FROM_DEVICE, IO_DMA_ATTR);
if (ret == 0)
    area->is_mapped = true;
```

### Impact
- **Scope**: 32-bit arch with 64-bit DMA kernel builds only
- **Type**: Kernel memory leak → resource exhaustion (DoS)
- **Attack vector**: Local, io_uring permissions, repeated `io_uring_register()` inducing mapping failures

### Detection
```bash
# Check kernel config for affected architecture
zcat /proc/config.gz | grep PAGE_POOL_32BIT_ARCH_WITH_64BIT_DMA

# Monitor slab growth on zcrx workloads
watch -n 5 'cat /proc/slabinfo | grep sg_table'

# Correlate DMA errors with memory pressure
dmesg -T | grep -i "dma.*fail\|io_populate_area_dma"
```

## References
- Kernel docs: https://docs.kernel.org/networking/iou-zcrx.html
- LWN v10: https://lwn.net/Articles/1004591/
- Git pull: Jens Axboe, netdev list
- **CVE-2026-43224 Intel Report**: `intel/systems/2026-06-06_io_uring-zcrx-sgtable-leak.md`
- **Fix commits**: a983aae39776, ef075c1464ac, f1ae40332431
- **Introducing commit**: 439a98b972fbb

## Exercises
1. **Setup**: Configure `ethtool` for header/data split + RSS on test NIC
2. **Register**: Write minimal ZCRX registration (area + refill ring + ifq_reg)
3. **Receive**: Submit multishot RECV_ZC, process CQEs, recycle buffers
4. **Benchmark**: Compare throughput vs epoll on same hardware
5. **Debug**: Inject memory pressure, observe copy fallback behavior
6. **Security Audit**: Verify kernel includes fix commits; check for `PAGE_POOL_32BIT_ARCH_WITH_64BIT_DMA` config; monitor `sg_table` slab cache under zcrx load