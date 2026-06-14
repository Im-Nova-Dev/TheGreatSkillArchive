# Linux Kernel Netfilter nf_tables UAF Detection and Defense

Use when analyzing, detecting, or teaching kernel privilege escalation paths that abuse netfilter nf_tables use-after-free bugs.
Use when preparing CTF-style Linux kernel challenges involving UAF in the kernel datapath.
Use when hardening containerized or multi-tenant Linux hosts against local privilege escalation.

## Case Study: CVE-2024-1086 — Actively Exploited netfilter Double-Free (Jan–May 2024)

### Executive Summary
**CVE-2024-1086** is a **use-after-free / double-free** in `nf_tables` (netfilter) allowing **local privilege escalation (LPE)**. Initially CVSS 7.8 High (Jan 31, 2024); **actively exploited in the wild** by mid-April 2024; added to **CISA KEV May 30, 2024**. CrowdStrike ExPRT.AI rates **Critical — "Actively Used"**.

### Root Cause
- **Component:** `nf_tables` in `net/netfilter/nf_tables_core.c`
- **Flaw:** Reverted commit caused `nft_verdict_init()` to interpret upper 16 bits of `NF_DROP` verdicts as errno (e.g., `-EPERM`, `-EHOSTUNREACH`) or 0
- **Mechanism:**
  1. `nft_verdict_init()` marks verdict as `NF_DROP` with crafted upper 16 bits
  2. `nf_hook_slow()` treats non-zero as error → frees packet (`skb`)
  3. Verdict resembles `NF_ACCEPT` → continues processing → **double-free** of same `skb`

### Exploitation Chain (Public PoC)
| Step | Action | Technique |
|------|--------|-----------|
| 1 | Prerequisite: `kernel.unprivileged_userns_clone=1` (default on Debian/Ubuntu) | T1068 |
| 2 | Trigger double-free via crafted `nf_tables` rule | T1068.001 |
| 3 | Scan physical memory for kernel base → **bypass KASLR** | T1070.001 |
| 4 | Groom heap: reclaim freed `skb` slab with `nft_set`/`nft_expr` (heap feng shui) | T1211 |
| 5 | Achieve arbitrary kernel read/write via corrupted objects | T1068.001 |
| 6 | Overwrite `modprobe_path` kernel variable | T1574.006 |
| 7 | Trigger `modprobe` → drop **root shell** | T1059.004 |

### Real-World Stability
> "The targeted Linux host becomes unstable after closure of the root shell... eventually causes the system to crash."
> "A more sophisticated threat actor... can almost certainly modify the exploit to prevent the system from crashing post-exploitation."

### Affected Kernel Versions
| Range | Status |
|-------|--------|
| 6.7 → < 6.7.3 | Vulnerable |
| 6.2 → < 6.6.15 | Vulnerable |
| 3.15 → < 6.1.76 | Vulnerable |
| 6.8-rc1 | Vulnerable |

### Indicators of Compromise (Behavioral)
- Unprivileged user creating `nf_tables` rules via `nft` CLI or netlink API
- Repeated `NF_DROP` verdicts with anomalous upper 16-bit values
- `modprobe_path` modification (kernel variable write)
- Physical memory scan: sequential `pread` on `/dev/mem` or `/proc/kcore`
- Sudden root shell spawn from unprivileged context
- System instability/crash following privilege escalation

### MITRE ATT&CK Mapping
| Technique ID | Technique Name | Phase |
|--------------|----------------|-------|
| T1068 | Exploitation for Privilege Escalation | Privilege Escalation |
| T1068.001 | Kernel Exploit | Privilege Escalation |
| T1574.006 | Dynamic Linker Hijacking | Privilege Escalation |
| T1059.004 | Unix Shell | Execution |
| T1490 | Inhibit System Recovery | Impact |
| T1070.004 | File Deletion | Defense Evasion |

---

### Core Concept

nf_tables allows unprivileged userspace to create tables, chains, and expressions. A UAF can arise when the kernel drops a reference to an expression or object while it is still reachable through another chain or rule that is being processed. If an attacker races a deletion and a lookup, freed memory can be reclaimed by attacker-controlled allocations, often `user_key_payload` or `user_struct`, leading to controlled object lifetime and arbitrary code execution in kernel context.

## Advanced Exploitation: CVE-2024-1086 Deep Dive (Dirty Pagedirectory / KSMA)

### Root Cause (Sanitization Failure)
- **Component**: `nft_verdict_init()` in `net/netfilter/nf_tables_core.c`
- **Flaw**: Accepts positive drop error `1` (`NF_ACCEPT`) in verdict
- **Mechanism**:
  1. User sets verdict to `NF_DROP` with drop error `1` (overlaps with `NF_ACCEPT`)
  2. `nf_hook_slow()` frees `skb` on `NF_DROP`
  3. Returns `NF_GET_DROPERR()` = `1` → interpreted as `NF_ACCEPT`
  4. Caller continues packet processing → **double-free** of same `skb`

### Novel Exploitation Primitives
| Primitive | Details |
|-----------|---------|
| **Double-free** of `struct sk_buff` | In `skbuff_head_cache` slab |
| **Double-free** of `skb->head` | Dynamic: kmalloc-256 → order-4 buddy pages (64KB) |
| **IP Fragmentation Abuse** | Delay 2nd free via IP fragment queue (red-black tree); timeout controlled via `/proc/sys/net/ipv4/ipfrag_time` |
| **PCP Draining (Order-4 → Order-0)** | Drain per-CPU pagecache (16k PTE spray) → buddy refill splits freed order-4 page into 16 order-0 pages in PCP |
| **Dirty Pagedirectory (KSMA)** | Double-allocate PMD page and PTE page to same physical address → arbitrary physical R/W via PTE overlap |

### Dirty Pagedirectory Technique (Kernel-Space Mirroring Attack)
```
Userland VMA Ranges:
- PMD area:  0x40000000 - 0x80000000   (mm->pgd[0][1])
- PTE area:  0x8000000000 - 0x10000000000 (mm->pgd[1])

Double-alloc: mm->pgd[0][1] == mm->pgd[1] (same physical page)
→ mm->pgd[0][1][x][y] (userland page) == mm->pgd[1][x][y] (PTE entry)
```

**Exploitation Flow:**
1. Write malicious PTE value (PFN + flags) to userland page in PMD area
2. Same bytes interpreted as PTE in PMD area
3. Dereference by reading corresponding page in PTE area
4. **Result**: Arbitrary physical R/W with controlled permissions

### KernelCTF Freelist Corruption Check Bypass
- `skbuff_head_cache->offset == 0x70` → freelist ptr overlaps `skb->len`
- After 1st free: `skb->len` overwritten with partial next ptr
- Packet parsing corrupts it further before 2nd free
- **Bypass**: Free "innocent" skb *after* corrupted one → masks corruption

### Exploit Characteristics
- **Data-only** (no code execution in kernel)
- **Fileless execution** via `memfd_create`
- **99.4% success rate** (n=1000) on v5.14–v6.6.14 with `unprivileged_userns_clone=1`
- **Kernel panic** post-exploit (intentional side-effect); root shell persists with disk access

## Typical Attack Primitives

1. **Object recycling via user_key_payload**
   - Allocate many user keyrings or payloads to gain a controlled heap layout.
   - Trigger UAF so the freed expression/set object is reallocated as attacker-controlled data.
   - Achieve arbitrary read/write via crafted payload contents and IPC/overwrite techniques.

2. **KASLR / SMEP / SMAP bypasses**
   - Leak kernel base via exposed pointers in the reused object or via side channels.
   - Use ROP/JOP chains within kernel text when code execution is achieved.

3. **Container escape relevance**
   - Unprivileged container userspaces often still have access to netfilter ioctls.
   - A UAF in this path can break out of the container to the host root namespace.

## Affected Kernel Subsystems

- `net/netfilter/nf_tables.c`
- `net/netfilter/nf_tables_offload.c`
- Ancillary table, expression, and set allocators under `include/net/netfilter/`

## Detection Strategy

- **Audit logging**:
  - Watch for unprivileged processes issuing `NFNL_SUBSYS_NFTABLES` requests that create then rapidly delete tables, sets, or expressions.
  - Correlate with follow-up `set` updates, especially batch expressions and anonymous payloads.

- **eBPF / kprobes**:
  - Trace key object alloc/free pairs with lifetime measurement.
  - Alert on reuse of an address that was freed but still referenced by an in-flight rule.

- **EDR / Sigma heuristics**:
  - Unexpected privilege transitions without `execve` of setuid binaries.
  - Unusual mounts or namespace changes coming from a user namespace but system-wide user ID 0.
  - Abnormal socket or netlink interaction patterns before the privilege change.

- **Runtime instrumentation**:
  - Use `lockdep` / `KASAN` / `kmemleak` with `SLUB_DEBUG` on test/staging systems to reproduce races.
  - Capture `sysfs` `trace_events` around `nft_*` and `kmalloc`/`kfree`.

## Mitigation Guidance

- Kernel hardening patches:
  - Backport fixes that replace unsafe reallocation paths and add refcount validation.
  - Deploy kernel lockdown / CONFIG_SECURITY_YAMA guidelines that restrict unprivileged netfilter namespaces where viable.

- Runtime restrictions:
  - Drop `CAP_NET_ADMIN` in user namespaces where netfilter is not required.
  - Seccomp profiles that deny `ioctl` with `NFNL_SUBSYS_NFTABLES` for low-trust workloads.
  - gVisor/Kata/other OCI runtimes that virtualize netfilter when untrusted code is present.

- System-wide defense:
  - Keep kernels patched (CVE-2024-1086 and related UAFs).
  - Monitor CISA KEV; place compensating controls where patching is delayed.

## MITRE ATT&CK Mapping

- T1068: Exploitation for Privilege Escalation
- T1210: Exploitation of Remote Services (when reachable via network services)
- T1059.004: Command and Scripting Interpreter: Unix Shell (post-exploitation)
- T1053.003: Scheduled Task/Job: Cron (persistence)

## Practical Exercises / CTF Relevance

1. **UAF reproduction lab**:
   - Build a minimal reproducer using `nf_tables` netlink interface.
   - Observe the race between object deletion and retrieval.

2. **Heap feng shui practice**:
   - Allocate spray objects to control heap layout and force reuse.
   - Measure heap adjacency with `proc/slabinfo` instrumentation.

3. **Detection drill**:
   - Write a Sigma/eBPF rule to flag suspicious nftables ioctl sequences.
   - Test against a simulated exploit run in a disposable VM snapshot.

4. **Container escape scenario**:
   - Allow unprivileged netfilter in an isolated user namespace, exploit the UAF, and map the escape path.

## Mapping to Other Skills

- `double-fetch-kernel-exploitation`: TOCTOU concepts complement UAF race patterns.
- `linux-kernel-page-cache-lpe-primitives`: page-cache corruption primitives are an alternate LPE class.
- `apparmor-lpe-exploitation`: confinement bypasses that chain with kernel UAFs.
- `browser-exploit-chain-analysis`: sandbox escape chains often add kernel UAF as the final step.
