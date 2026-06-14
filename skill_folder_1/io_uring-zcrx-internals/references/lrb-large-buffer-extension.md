# io_uring ZCRX Large Receive Buffer Extension

- Source article: https://www.phoronix.com/news/IO-uring-zcrx-Large-RX
- Kernel commit: 795663b4d160ba652959f1a46381c5e8b1342a53
- Queued in: Jens Axboe `for-next` branch, `for-7.0/io_uring-zcrx-large-buffers`
- Target merge: Linux 6.20 / 7.0
- Author: Pavel Begunkov (Meta)

## Key performance claim
Up to ~30% CPU utilization improvement for a single TCP flow when moving from 4 KiB to 32 Ki Rx buffers on a 200 Gbps-class NIC (kernel comment in patch).

## Mechanistic notes for future teaching material
- ZCRX page pool moves from single-page entries to higher-order pages; `order >= 1` is now visible in the ZC fast path.
- This means `PP_FLAG_PAGE_FRAG` is now load-bearing not just as an optimization but for handling partial-page tail use. Recommend mentioning this in any buffer-pool teaching material that covers page pools.
- Userspace CQE handling must change: `off` is no longer guaranteed to be zero on the first bio_vec.
- Refill queue accounting now implicitly maps "entries" to pages rather than packets.

## Relationship to other patches
- CVE-2026-43121 fix (commit `003049b1c4fb8aabb93febb7d1e49004f6ad653b`, stable 6.18.16+) is orthogonal to LRB. The LRB patchset does not reintroduce the freelist race but does touch `page_pool` and `net_iov` fields.
- LRB is a prerequisite for later ZCRX work: THP support and dmabuf support both expect the ZC area to support buffers larger than a single page.

## Hardware boundary
NIC must expose larger-than-page Rx buffers via `ethtool -g`. Not all supported ZCRX NICs will benefit; if `rx-buf-len` is stuck at 4096, LRB code path is not exercised.

## Questions for teaching material
1. If `nr_iovs = 1024` and buffers become 32 KiB each, what happens to refill queue churn and why does this matter for userspace cache locality?
2. How does `PP_FLAG_PAGE_FRAG` interact with higher-order page allocation when a packet payload is smaller than the full page?
3. Why does LRB not remove the need for header/data split or RSS isolation?
