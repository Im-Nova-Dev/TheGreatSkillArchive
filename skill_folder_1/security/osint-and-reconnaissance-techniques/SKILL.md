---
name: osint-and-reconnaissance-techniques
description: Osint And Reconnaissance Techniques. Includes cyber threat intelligence collection, CVE research, and offensive security reconnaissance.
version: 1.1.0
---

## Last Updated
2026-06-06 — Added CVE-2024-1086 (nf_tables double-free → Dirty Pagedirectory KSMA technique) and CVE-2026-43121 (io_uring ZCRX freelist race 4-byte OOB write); added sources: Penligent (io_uring ZCRX deep dive), pwning.tech (nf_tables exploit methodology); added 6 new techniques to index (IP fragmentation race widening, PCP draining order conversion, kernel PTE overlap, io_uring user_refs race); intel items saved to 2026-06-06_cve-2024-1086_nftables_double_free.md and 2026-06-06_cve-2026-43121_io_uring_zcrx_race.md
## Framework
1. Define target boundary: application, OS, firmware, supply chain.
2. Identify technical sources: NVD, CISA KEV, vendor advisories, MSRC, Exploit-DB, GitHub PoC.
3. Identify signal-rich non-standard sources: Reddit `netsec`, `r/ReverseEngineering`, Twitter/X infosec community, Telegram breach channels, Pwn2Own writeups, conference talks (Black Hat, DEF CON, BlueHat).
4. Capture metadata: CVE ID, fixed versions, CVSS, PoC availability, MITRE mapping.

## Targeted CVE/Intel Research Routine
- Query with exact CVE ID.
- Capture mechanism: “how does the bug reach privileged context?”
- Identify detection signals: event IDs, WMI filters, process lineage anomalies.
- Find public PoC/secondary references: researcher blogs, GitHub, Packet Storm.

## Trusted Path Abuse Enumeration (Red Team Focus)
Windows-specific systematic discovery pattern:
1. Identify SYSTEM-level or highly privileged process file interactions (Update Stack, scheduled tasks, COM services, Windows Installer).
2. List ACLs on directories and file paths the privileged process reads/loads from:
   - `Get-Acl`, `icacls`, WinObj / WinBkg.
   - Sysinternals `procmon` filters on process name + `Path` column.
3. Check Junction/Symlink safeties:
   - Does the path exist by default?
   - Is creation of `Directory` or `Junction` possible by standard users?
   - Is `SeCreateSymbolicLinkPrivilege` required for symlinks? If yes, junction (`mklink /J`) often bypasses the privilege check.
4. Abuse patterns:
   - Replace directory with junction pointing to attacker-controlled content.
   - Drop payloads in locations writeable by standard users: `C:\inetpub\wwwroot`, temp paths, INetCache.
5. Post-exploitation considerations:
   - EDR/Defender heuristics: low-noise because process is Microsoft-signed and expected behavior.
   - Persistence: if update job is recurring, same junction re-enables SYSTEM spawn regularly.

## Exploit Development Signal Collection
- Binary exploitation: double fetch, use-after-free, LFH, pool feng shui, ROP, JIT-spray, type confusion.
- OS internals: page cache races, splice/algif_aead, IOCTL validation gaps, **signal race manipulation (signal 33/NPTL)**, **kernel-hack-drill methodology**.
- Detection-aware development: prefer low-noise primitives (junctions, hardlink abuse, COM hijack) for red teams; avoid obvious shellcode patterns when detection is prioritized.

## Avoid
- Trusting unsourced social media claims without corroborating advisory.
- Skipping CVSS/AV/AUX vectors when triaging for operational use.

---

## Last Updated
2026-06-06 — Added NVIDIA GPU kernel stack UAF exploit chain (CVE-2025-23280, CVE-2025-23300) from Quarkslab; added Quarkslab to primary sources; extended technique index with vmalloc stack UAF, heap feng shui, random_kstack_offset bypass, red-black tree data-only exploitation, partial fix call-site audit; added Proprietary Driver Audit collection technique; intel item saved to 2026-06-06-nvidia-gpu-kernel-stack-uaf-exploit.json
Each intel item must be enriched with:

| Field | Purpose | Example |
|-------|---------|---------|
| **MITRE ATT&CK** | Tactic + Technique IDs | T1068 (Exploitation for Privilege Escalation), T1590.002 |
| **Target Class** | Kernel version, config, OS, deployment | Linux 5.x-6.x, CONFIG_NET_SCH_SFQ + CONFIG_USER_NS |
| **Detection Difficulty** | Low/Medium/High + rationale | High — requires netlink qdisc manipulation, no file write |
| **Exploit Maturity** | Concept / PoC / Weaponized / In-the-wild | Weaponized (public exploit + stabilization) |

**Detection Difficulty Rubric:**
- **Low**: Visible in standard logs (auditd, syslog, EDR telemetry), file writes, network connections
- **Medium**: Requires specific kernel tracing (ftrace, eBPF), unusual syscall sequences, or memory analysis
- **High**: Purely in-kernel manipulation (qdisc, slab, page cache), no userspace artifact, requires custom sensors

---

## Last Updated
2026-06-06 — Added NVIDIA GPU kernel stack UAF exploit chain (CVE-2025-23280, CVE-2025-23300) from Quarkslab; added Quarkslab to primary sources; extended technique index with vmalloc stack UAF, heap feng shui, random_kstack_offset bypass, red-black tree data-only exploitation, partial fix call-site audit; added Proprietary Driver Audit collection technique; intel item saved to 2026-06-06-nvidia-gpu-kernel-stack-uaf-exploit.json
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
| **Kernel Stack UAF via vmalloc** | CVE-2025-23280, CVE-2025-23300 | `security/proprietary-kernel-module-exploitation` |
| **vmalloc Heap Feng Shui (fork/v4l2/purge)** | CVE-2025-23280 | `security/proprietary-kernel-module-exploitation` |
| **random_kstack_offset Bypass via Shaping** | CVE-2025-23280 | `security/proprietary-kernel-module-exploitation` |
| **Red-Black Tree Data-Only Exploitation** | CVE-2025-23280 | `security/proprietary-kernel-module-exploitation` |
| **Partial Fix Call-Site Audit** | NVIDIA Oct 2025 bulletin | `security/proprietary-kernel-module-exploitation` |
| **nf_tables Double-Free → Dirty Pagedirectory (KSMA)** | CVE-2024-1086 | `security/netfilter-uaf-detection-and-defense` |
| **IP Fragmentation Race Widening** | CVE-2024-1086 | `security/netfilter-uaf-detection-and-defense` |
| **PCP Draining Order Conversion** | CVE-2024-1086 | `security/kernel-heap-exploitation` |
| **Kernel PTE Overlap for Arbitrary Phys R/W** | CVE-2024-1086 | `security/netfilter-uaf-detection-and-defense` |
| **io_uring ZCRX Freelist Race (4-byte OOB Write)** | CVE-2026-43121 | `security/io-uring-zcrx-exploitation` |
| **io_uring ZCRX Scrub/Refill `user_refs` Race** | CVE-2026-43121, CVE-2026-43174 | `security/io-uring-zcrx-exploitation` |

---

## Last Updated
2026-06-06 — Added NVIDIA GPU kernel stack UAF exploit chain (CVE-2025-23280, CVE-2025-23300) from Quarkslab; added Quarkslab to primary sources; extended technique index with vmalloc stack UAF, heap feng shui, random_kstack_offset bypass, red-black tree data-only exploitation, partial fix call-site audit; added Proprietary Driver Audit collection technique; intel item saved to 2026-06-06-nvidia-gpu-kernel-stack-uaf-exploit.json
The scheduled cron job executes autonomously every run:

1. **Collect**: Web search for recent (6-12 month) deep-technical writeups using signal-rich queries:
   - `site:github.com OR site:googleprojectzero.blogspot.com OR site:zerodayinitiative.com "CVE-2024" OR "CVE-2025" "exploit" OR "writeup" OR "heap feng shui" OR "double-fetch" OR "ROP chain" OR "JIT spraying"`
   - Broaden to adjacent domains when thin: reverse engineering, forensics, malware analysis, OS internals, hardware hacking, radio/wireless, applied crypto attacks

2. **Extract**: Full content via `web_extract` (not summaries) — preserves code, offsets, gadget addresses

3. **Enrich**: Apply framework above; map to MITRE; assess detection difficulty

4. **Persist**: Save to `/home/nova/.hermes/intel/cybersecurity/<CVE-ID>-<short-name>.md`

5. **Index**: Append entry to `references/intel-sources.md` (this skill's references directory)

---

## Last Updated
2026-06-06 — Added NVIDIA GPU kernel stack UAF exploit chain (CVE-2025-23280, CVE-2025-23300) from Quarkslab; added Quarkslab to primary sources; extended technique index with vmalloc stack UAF, heap feng shui, random_kstack_offset bypass, red-black tree data-only exploitation, partial fix call-site audit; added Proprietary Driver Audit collection technique; intel item saved to 2026-06-06-nvidia-gpu-kernel-stack-uaf-exploit.json
Maintained in `references/intel-sources.md` — update each run with new valuable sources.

### Primary Technical Blogs / Researcher Sites
- **a13xp0p0v.tech** (Alexander Popov) — Kernel exploit methodology, CVE case studies, kernel-hack-drill tooling, immortal signal race technique
- **Doyensec Blog** (blog.doyensec.com) — Multi-part exploit series (CVE-2025-37947 ksmbd)
- **SSD Secure Disclosure** (ssd-disclosure.com) — Advisory + full exploit chain (CVE-2025-0927 HFS+)
- **Google Project Zero** (googleprojectzero.blogspot.com) — Industry-standard root cause + exploit
- **Zero Day Initiative** (zerodayinitiative.com/advisories) — Vendor-coordinated disclosure timeline
- **Quarkslab Blog** (blog.quarkslab.com) — Proprietary driver exploitation (NVIDIA GPU, vmalloc internals), GPU kernel UAF chains, heap shaping techniques
- **Penligent** (penligent.ai) — io_uring ZCRX internals, freelist race condition analysis (CVE-2026-43121)
- **pwning.tech** — nf_tables exploit methodology, Dirty Pagedirectory KSMA technique (CVE-2024-1086)

### Aggregation / Curation Repos
- **xairy/linux-kernel-exploitation** (GitHub) — Bimonthly updated link collection, CVE-tagged
- **0xMarcio/cve** (GitHub) — PoC exploits for recent CVEs (CVE-2024-1086 universal LPE)
- **tylzars/awesome-vrre-writeups** (GitHub) — Curated vulnerability research writeup list

### Vendor / Authority Feeds
- **CISA Known Exploited Vulnerabilities (KEV)** Catalog — Ground truth for in-the-wild exploitation
- **Ubuntu Security Notices** / **Debian Security Advisories** — Distro-specific fix status
- **LWN.net Kernel Coverage** — Technical analysis of mainline fixes

### Conference / CTF Archives
- **Black Hat / DEF CON / BlueHat** talk materials (PDFs, slides, whitepapers)
- **Pwn2Own** / **Tianfu Cup** / **QuantumCTF** writeups — Weaponized chains

---

## Last Updated
2026-06-06 — Added NVIDIA GPU kernel stack UAF exploit chain (CVE-2025-23280, CVE-2025-23300) from Quarkslab; added Quarkslab to primary sources; extended technique index with vmalloc stack UAF, heap feng shui, random_kstack_offset bypass, red-black tree data-only exploitation, partial fix call-site audit; added Proprietary Driver Audit collection technique; intel item saved to 2026-06-06-nvidia-gpu-kernel-stack-uaf-exploit.json
- **Tool bug resilience**: `write_file` may fail with "missing required field 'content'" despite content being optional in schema. Workaround: create empty file first with `write_file(content="")`, then patch. Or use `skill_manage(action='write_file', file_path='references/...')` for skill-internal files.
- **Search breadth vs. depth**: Broad queries ("CVE-2025 exploit") return noise; precise technique queries ("heap feng shui 2024 site:github.com") + author sites (syst3mfailure, doyensec, a13xp0p0v) yield signal.
- **Extraction over summary**: `web_extract` returns LLM-summarized content for long pages; for exploit code/offsets, verify against original or search for GitHub PoC repos.
- **Intel directory structure**: Ensure `/home/nova/.hermes/intel/cybersecurity/` exists before writing (first run creates it).
- **Immortal signal technique**: Signal 33 (NPTL reserved) via `timer_create`/`timer_settime` interrupts `connect()` without killing exploit process — novel race widening primitive for kernel UAF exploitation.
