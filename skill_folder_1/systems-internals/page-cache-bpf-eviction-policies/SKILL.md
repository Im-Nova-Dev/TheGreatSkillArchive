---
type: skill
name: page-cache-bpf-eviction-policies
summary: Teach Linux page cache internals and how eBPF can customize eviction policies, including cache_ext / struct_ops mechanics, folio lifecycle, active/inactive list management, per-cgroup policy isolation, and real workload tuning.
description: Mechanistic teaching module on Linux page cache internals, the active/inactive LRU approximation, and how eBPF-based `cache_ext` allows custom insertion/eviction policies via `struct_ops` hooks, folio LRU reuse, and per-cgroup attachment.
version: 2026-06-05
---

# Page Cache BPF Eviction Policies

Use when teaching or analyzing how to customize Linux page-cache eviction behavior using eBPF, and how the underlying shrinker / active-inactive list machinery works.

## Learning Objectives

1. Explain why Linux's default page-cache eviction policy is an **LRU approximation** rather than true LRU.
2. Describe the active / inactive list split and the `mark_page_accessed()` promotion path.
3. Identify the two problems that make changing the policy hard: global invasiveness and lack of isolation.
4. Walk through how `cache_ext` uses `struct_ops` and eBPF eviction lists to provide insertion and eviction policies.
5. Explain the **folio LRU reuse trick** and why it removes the need for a separate valid-pages hash table.
6. Describe how per-cgroup policy attachment works at the `struct cgroup_bpf` layer.
7. Evaluate trade-offs of custom policies against MGLLU, `fadvise()`, and application-level caching.

## Lesson Outline

### 1. The Page Cache I. How Workloads Get Stuck

The Linux page cache uses two FIFO-like lists — *active* and *inactive* — approximated via LRU. Core rules:
- Newly read folios go to the *inactive* tail.
- `mark_page_accessed()` rotates them toward the *active* tail.
- Reclaim scans *inactive* first, freeing coldest pages.

This heuristic leaks for:
- HTAP mixes (transactional GET + large SCAN)
- Extreme skew: 99% GET and 1% SCAN where 1% of volume is SCAN but SCAN pages evict hot GET pages.
- Tiny recurrent transactions where promotion lag leaves cache useful only for the largest process.

### 2. Prior Solutions and Their Failure Modes

| Mechanism | Customizable | Isolated | Simple | Root cause of failure |
|-----------|--------------|----------|--------|------------------------|
| Global policy change | ✅ | ❌ | ❌ | Requires core shrinker rewrite; MGLRU still non-default after years upstream |
| `fadvise()` / `posix_fadvise()` | ❌ | ❌ | ✅ | Only 6 flags; several are no-ops on major kernels |
| Application cache (Redis, SQLite) | ✅ | ✅ | ❌ | Doubles memory pressure; bypasses kernel IO scheduling and readahead |

### 3. cache_ext: The Design

`cache_ext` inserts hooks **inside the shrinker path** without rewriting the policy itself.

**Insertion policy** (`bpf cache_ext insert`)  
Decides which list a folio is added to. Default behavior mirrors current kernel: go to inactive.  
Custom example: SCAN data goes to a dedicated SCAN list so it never fights GET folios.

**Eviction policy** (`bpf cache_ext evict`)  
Chooses which folio to free when memory pressure hits.  
Custom example: LFU counter via a pinned eBPF map keyed by inode.

**Eviction lists**  
Named per-cgroup lists tracked as LRU-ordered lists inside eBPF. When the shrinker asks for a victim, the BPF program returns a folio from its custom list.

### 4. The Folio LRU Reuse Trick

This is the mechanistic crux.

`struct folio` contains:

```c
struct list_head lru;   // used by the built-in shrinker
```

The kernel shrinker already walks `folio->lru` through the page list. If `cache_ext` had separate tracking structures, a folio could exist on **both** a `cache_ext` list and the kernel's LRU list simultaneously, breaking shrinker assumptions.

cache_ext's solution: when a folio is placed on a `cache_ext` eviction list, the `lru` field is repurposed as the list node for that custom list. The folio is therefore **on exactly one list at any time**:
- Normal path: on kernel LRU.
- Custom path: on `cache_ext` list.

This eliminates the need for an auxiliary hash table (`valid_folios`) that was tried in earlier prototypes.

### 5. Per-Cgroup Attachment via `struct_ops` + `bpf_map_attach()`

The new API:

```c
int bpf_map_attach(int map_fd, int target_fd, enum bpf_attach_type type);
```

- `map_fd` is the `struct_ops` map representing the cache_ext policy object (insert + evict callbacks).
- `target_fd` is a cgroup file descriptor.
- `type` is a new BPF link type describing a `cache_ext` attachment.

Kernel stores the attachment in `struct cgroup_bpf`, similar to how `sched_ext` policies are attached to cgroups.  
Enables:  
- Container runs an LFU policy.  
- Host runs a scan-aware policy.  
- Both fed by the same global page cache but isolated by eviction behavior.

### 6. Measured Behavior

- GET/SCAN isolation by PID: 70% higher GET throughput, 57% lower p99 latency.
- S3-FIFO / Twitter trace / LHD / LFU policies on YCSB: up to 37% improvement.
- Per-cgroup mixed workloads: 50% and 80% improvements over baseline.

### 7. Open Issues (as of LSFMM/BPF 2026)

- shrinker hook acceptance: MM maintainers need confidence that BPF programs in the reclaim critical path can't trigger OOM storms or livelocks.
- MGLRU coexistence: if MGLRU finally becomes default, will custom policies migrate onto MGLRU generations, or remain an alternative?
- Refcount races: despite reuse of `lru`, the eBPF program boundary makes it easy to drop a reference too early or too late; the prototype relies on verifier discipline plus careful kernel-side refcounting.

## Exercises

1. Trace `mark_page_accessed()` in the kernel tree and show where active/inactive rotation happens. (Look in `mm/filemap.c` and target `activate_page()`.)
2. Read `mm/vmscan.c` shrink_active_list / shrink_inactive_list and explain how the approximation degenerates for write-heavy workloads.
3. Sketch the `cache_ext` `struct_ops` layout: two function pointers plus a context, and show how `bpf_map_attach()` binds it to a cgroup.
4. Simulate (in Python or C) an LFU window with a scan spike. Show why LRU approximation catastrophically evicts hot GET pages.
5. Propose a safe BPF verifier rule set to prevent an eviction program from returning an already-freed folio.

## Source Material

- cache_ext LPC 2024 slide deck: `https://lpc.events/event/19/contributions/2165/attachments/1878/4026/cache_ext_lpc.pdf`
- cache_ext GitHub: `https://github.com/cache-ext/cache_ext`
- LSFMM/BPF 2026 “Custom page-cache policies with BPF”: `https://lwn.net/Articles/lsfmmbpf2026/`
- Linux kernel `struct_ops` tutorial: `https://eunomia.dev/tutorials/features/struct_ops/`
- Linux sched_ext docs: `https://docs.kernel.org/scheduler/sched-ext.html`
