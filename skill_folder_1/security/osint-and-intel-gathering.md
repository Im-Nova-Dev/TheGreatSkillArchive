# OSINT and Intel Gathering for Offensive Security

This index tracks sources, techniques, and methodologies for collecting actionable offensive security intelligence.

---

## Source Taxonomy

### Primary Technical Sources

| Source | Type | Frequency | Focus |
|--------|------|-----------|-------|
| Project Zero Blog | Blog | Bi-weekly | 0-day analysis, exploit dev |
| Theori Blog | Blog | Monthly | Kernel/RCU/browser exploits |
| MalwareTech | Blog | Irregular | Windows kernel, IPv6, RCE |
| Google Security Research | Multi | Continuous | Cross-platform vuln research |
| Microsoft Security Response | Advisory | Monthly | Patch analysis, exploit mitigation |
| Linux Kernel Mailing List (LKML) | Mailing list | Daily | Kernel patches, CVE discussions |
| GitHub Security Advisories | Feed | Continuous | OSS vulns, PoCs |
| ZDI Blog | Blog | Weekly | Vendor vulns, root cause analysis |
| **GitHub Security Blog** | Blog | Monthly | In-house exploit dev (JIT, kernel, supply chain) |
| **CrowdStrike Blog** | Blog | Weekly | In-the-wild exploitation, EK tracking |
| **Qrious Security** | Blog | Irregular | Browser JIT internals, AI-assisted fuzzing, SpiderMonkey/bindings analysis |
|| **ptr-yudai / BunkyoWesterns** | Blog | Irregular | Kernel exploit methodology, CTF writeups (cornelslop: RCU double-free, race widening, PTE overlap) |
|| **kqx** | Blog | Irregular | Kernel CTF writeups, RCU/SLUB internals (cornelslop writeup, Google kernelCTF VRP) |
|| **Penligent** | Blog | Irregular | io_uring ZCRX internals, freelist race condition analysis (CVE-2026-43121) ||
|| **GitHub Security Lab** | Blog | Monthly | GPU driver exploitation, MTE bypass, Mali CSF internals, Android kernel exploitation (CVE-2025-0072) ||
|| **FuzzingLabs** | Blog | Irregular | nf_tables exploit reproduction, inverted condition bugs, transaction abort UAF chains (CVE-2026-23111) ||
|| **STAR Labs (starlabs.sg)** | Advisory | Monthly | Kernel TLS, net/tls UAF, zero-copy anchor SKB race, cipher-suite-specific exploits (CVE-2025-39682) ||
|| **Man Yue Mo** | Blog/GitHub | Irregular | Advanced Android/mobile exploitation, MTE/hardware mitigation bypasses, GPU kernel driver UAF chains ||
| **STAR Labs (starlabs.sg)** | Blog | Monthly | Windows kernel, Cloud Filter, driver exploits |
| **Exploit Reversing (exploitreversing.com)** | Blog | Monthly | Windows kernel exploit techniques, CVE deep-dives |
| **Zedeldi Research** | Blog/GitHub | Irregular | Secure Boot bypass, firmware, bootkit research |
| **Microsoft SecureBoot Objects Repo** | GitHub | Per-release | DBX revocations, SBAT updates, shim signing |

### Secondary/Specialized Sources

| Source | Type | Focus |
|--------|------|-------|
| Kanxue BBS (看雪) | Forum | Chinese kernel/binary exploit research |
| USENIX Security / Black Hat / DEF CON | Proceedings | Academic/industry exploit techniques |
| HardenedLinux / KernelHardening | Wiki/Docs | Mitigation bypasses |
| grsecurity/PaX patches | Patch series | Advanced kernel hardening |
| syzbot dashboard | Automation | Fuzzing-found kernel bugs |
| **a13xp0p0v.tech** | Blog | Kernel exploit methodology, CVE case studies |
| **xairy/linux-kernel-exploitation** | GitHub | Curated kernel exploit links, updated bimonthly |
| **DiceCTF / b01lers / Google CTF** | CTF | Novel kernel exploit primitives in challenges |

### Intelligence Feeds

- **CISA KEV**: Known Exploited Vulnerabilities Catalog
- **NVD/NIST**: CVE metadata, CVSS, CWE mapping
- **MITRE ATT&CK**: Technique mapping for tactics
- **VulnCheck KEV/Exploit**: Exploit availability tracking
- **ExPRT.AI (CrowdStrike)**: Exploit maturity scoring, active exploitation signals

---

## Collection Techniques

### 1. Patch Diffing (Binary/Source)
- **Tooling**: `diffoscope`, `bindiff`, `ghidra`, `ida`, `quarkslab/decomp2dbg`
- **Targets**: Kernel patches (stable, -next), browser commits, firmware updates
- **Trigger**: Single-function changes, "+1 line" patches (high signal)

### 2. Commit History Mining
```bash
# Linux kernel: find RCU-related fixes
git log --oneline --grep="rcu" --grep="race" --grep="UAF" --grep="use.after.free" --since="2024-01-01"

# Look for "Fixes:" tags pointing to older commits
git log --oneline --grep="Fixes:" --since="2024-01-01" | head -50
```

### 3. Fuzzing Corpus Analysis
- syzkaller corpus → crash reproduction → root cause
- Custom fuzzers for specific subsystems (TCP, USB, filesystem)

### 4. Exploit Development Artifacts
- Public PoCs → weaponization barriers → reliability improvements
- CTF challenges → technique abstraction → real-world applicability

### 5. Academic/Industry Paper Translation
- USENIX Security, IEEE S&P, CCS, NDSS → practical exploit primitives
- Focus: Race widening (ExpRace), heap feng shui, JIT spraying, side channels

---

## Enrichment Framework (per intel item)

```json
{
  "tactic": "initial-access|privilege-escalation|defense-evasion|...",
  "target_class": "linux-kernel|windows-kernel|browser|firmware|...",
  "detection_difficulty": "low|medium|high|extreme",
  "mitre_attack": [{"technique_id": "Txxxx", "subtechnique": "..."}],
  "exploit_technique": "Named technique (ExpRace, SLUBstick, etc.)",
  "weaponization_barriers": ["KPTI", "KASLR", "SMAP/SMEP", "PAGE_TABLE_ISOLATION"],
  "reliability_factors": ["race window", "heap layout", "info leak required"]
}
```

---

## Technique Index (Cross-Reference)

| Technique | Key CVEs/Writeups | Skill Reference |
|-----------|-------------------|-----------------|
| **ExpRace (Reschedule IPI)** | CVE-2024-27394 | `red-teaming/rcu-exploitation-techniques` |
| **RCU Grace Period Manipulation** | CVE-2024-27394, CVE-2023-0461 | `red-teaming/rcu-exploitation-techniques` |
| **SLUB/SLAB Heap Feng Shui** | CVE-2023-20938, CVE-2022-23222 | `security/kernel-heap-exploitation` |
| **Double-Fetch / TOCTOU** | CVE-2024-50264, CVE-2017-2636 | `security/double-fetch-toctou` |
| **TCP/IP Stack Exploitation** | CVE-2024-38063, CVE-2021-24086 | `security/tcpip-stack-exploitation` |
| **JIT Spraying / Type Confusion** | Browser 0-days (CVE-2024-xxxx) | `security/browser-jit-exploitation` |
| **JIT Incorrect Side-Effect Modeling** | CVE-2023-3420 (TurboFan StackCheck) | `security/browser-jit-exploitation-techniques` |
| **Concurrent Compilation Race Exploit** | CVE-2023-3420 (Chrome 95+) | `security/browser-jit-exploitation-techniques` |
| **JIT Baseline IC Type Confusion (Union Punning)** | CVE-2025-14325 (SpiderMonkey Baseline IC) | `security/browser-jit-exploitation-techniques` |
| **netfilter nf_tables Double-Free** | CVE-2024-1086 | `security/netfilter-uaf-detection-and-defense` |
| **Kernel Heap Feng Shui via skb Reclaim** | CVE-2024-1086, CVE-2022-25636 | `security/kernel-heap-exploitation` |
| **modprobe_path Overwrite LPE** | CVE-2024-1086, Dirty Pipe | `security/linux-kernel-page-cache-lpe-primitives` |
| **Hardware Fault Injection** | Rowhammer (CVE-2025-6202), VoltPillager | `security/hardware-fault-injection` |
| **Side-Channel (Spectre/Meltdown variants)** | Transient execution attacks | `security/transient-execution-attacks` |
| **RCU Double-Free via Concurrent Reader-Writer** | DiceCTF 2026 cornelslop | `security/linux-kernel-rcu-uaf-exploitation` |
| **MADV_DONTNEED + mprotect() Race Widening** | DiceCTF 2026 cornelslop | `security/kernel-double-fetch-toctou-exploitation` |
|| **Multi-Core SLUB Cross-Cache (SLAB_NO_MERGE)** | DiceCTF 2026 cornelslop | `security/linux-kernel-rcu-uaf-exploitation` |
|| **RCU Callback Queue Pollution** | DiceCTF 2026 cornelslop | `security/linux-kernel-rcu-uaf-exploitation` ||
||| **PTE Overlap for Arbitrary File Write** | DiceCTF 2026 cornelslop | `security/linux-kernel-rcu-uaf-exploitation` ||
||| **io_uring ZCRX Freelist Race (4-byte OOB Write)** | CVE-2026-43121 | `security/io-uring-zcrx-exploitation` ||
||| **io_uring ZCRX Scrub/Refill `user_refs` Race** | CVE-2026-43121, CVE-2026-43174 | `security/io-uring-zcrx-exploitation` ||
||| **Mali CSF Queue Rebind Double-Map UAF + MTE Tag Oracle** | CVE-2025-0072 | `security/mali-gpu-mte-bypass-exploitation` ||
||| **GPU Memory Pool Tier Grooming (Context → Shared → Buddy)** | CVE-2025-0072 | `security/mali-gpu-mte-bypass-exploitation` ||
||| **nf_tables Inverted Genmask Check (Catchall Abort UAF)** | CVE-2026-23111 | `security/nf-tables-catchall-inverted-uaf` ||
||| **TLS Zero-Copy Anchor SKB Re-Queue UAF** | CVE-2025-39682 | `security/tls-anchor-skb-uaf-exploitation` ||
|| **WNF/ALPC/Pipe_attribute Heap Feng Shui** | CVE-2024-30085 (cldflt.sys) | `security/windows-kernel-heap-feng-shui` ||
| **Cloud Filter Reparse Point Overflow** | CVE-2024-30085 | `security/windows-kernel-driver-exploitation` |
| **Token Privilege Bit Manipulation via ALPC** | CVE-2024-30085 | `security/windows-token-manipulation` |
| **Secure Boot Chain-of-Trust Bypass via Unverified SquashFS + kexec** | CVE-2025-47827 (IGEL OS 10) | `red-teaming/secure-boot-bypass-techniques` |
| **Microsoft 3rd Party UEFI CA Trust Abuse** | CVE-2025-47827, CVE-2024-7344 | `red-teaming/firmware-exploitation-fundamentals` |
| **kexec-based Kernel Replacement Rootkit** | CVE-2025-47827 | `red-teaming/linux-kernel-rootkit-techniques` |

---

## Automation / Cron Integration

This index is maintained by the scheduled intel collection job. Each run:
1. Finds one substantive topic (CVE, technique, TTP)
2. Enriches with MITRE, target class, detection difficulty
3. Saves to `~/.hermes/intel/cybersecurity/YYYY-MM-DD-topic.json`
4. Updates or creates relevant teaching skill
5. Appends new technique/source to this index

---

## Last Updated
2026-06-06 — Added **FuzzingLabs** and **STAR Labs** as key sources for nf_tables transaction abort exploitation and kernel TLS zero-copy UAF research; added Technique Index entries for **nf_tables Inverted Genmask Check (Catchall Abort UAF)** (CVE-2026-23111) — single-character `!` negation in `nft_map_catchall_activate()` allows unprivileged UAF via transaction abort phase, exploitation via `seq_operations` KBASE leak → `msg_msg-2k` heap leak → ROP stack pivot; and **TLS Zero-Copy Anchor SKB Re-Queue UAF** (CVE-2025-39682) — content-type mismatch on zero-length TLS record causes `strp->anchor` SKB to be illegally queued into `ctx->rx_list` when `darg.zc==1`, corrupting `frag_list` and refcount leading to UAF on socket close; requires TLS 1.2 AES-CCM-128 cipher suite and precise record sequence; referenced skills: `security/nf-tables-catchall-inverted-uaf` (new), `security/tls-anchor-skb-uaf-exploitation` (new); previously: GitHub Security Lab and Man Yue Mo as key sources for hardware mitigation bypasses (MTE) and GPU driver exploitation; added Mali CSF queue rebind double-map UAF (CVE-2025-0072) with GPU memory pool tier grooming and MTE tag oracle via DMA; added Technique Index entries for "Mali CSF Queue Rebind Double-Map UAF + MTE Tag Oracle" and "GPU Memory Pool Tier Grooming (Context → Shared → Buddy)" referencing new skill `security/mali-gpu-mte-bypass-exploitation`; previously: DiceCTF 2026 cornelslop techniques: RCU double-free exploitation chain with race window widening (MADV_DONTNEED + mprotect()), multi-core SLUB cross-cache under SLAB_NO_MERGE, RCU callback queue pollution for callback timing control, and PTE overlap for arbitrary file write (overwrite /bin/umount); added io_uring ZCRX freelist race (CVE-2026-43121) 4-byte OOB write via double-free of niov; added sources: ptr-yudai/BunkyoWesterns (cornelslop writeup), kqx (cornelslop/kernelCTF writeups), Penligent (io_uring ZCRX deep dive); updated Technique Index with 5 cornelslop techniques + 2 io_uring ZCRX techniques; referenced skills: linux-kernel-rcu-uaf-exploitation, kernel-double-fetch-toctou-exploitation, io-uring-zcrx-exploitation (new).