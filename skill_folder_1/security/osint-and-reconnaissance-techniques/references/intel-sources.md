# Curated Intel Sources — OSINT & Reconnaissance

*Updated: 2026-06-06 (cron run)*

---

## Primary Technical Blogs / Researcher Sites

| Source | Focus | Notable Recent Coverage |
|--------|-------|-------------------------|
| **syst3mfailure.io** | Linux kernel exploitation, qdisc, slab, page cache | CVE-2025-37752 "Two Bytes of Madness" (SFQ OOB write, 262KB OOB) |
| **Doyensec Blog** (blog.doyensec.com) | Multi-part exploit development, kernel, browser | CVE-2025-37947 ksmbd OOB write (3-part series, buddy allocator grooming) |
| **SSD Secure Disclosure** (ssd-disclosure.com) | Full exploit chains, advisory + PoC | CVE-2025-0927 HFS+ slab OOB (bug since 2005, cross-cache RB tree corruption) |
| **Google Project Zero** (googleprojectzero.blogspot.com) | Root cause + exploit, industry standard | Various 0-days, Chrome, Windows, Android, iOS |
| **Zero Day Initiative** (zerodayinitiative.com/advisories) | Coordinated disclosure, vendor timelines | Published advisories feed |
| **GRUB/GRUB2 / Bootloader Research** (various) | Early boot, UEFI, Secure Boot bypass | CVE-2025-0678, CVE-2025-0679 (shim) |

---

## Aggregation / Curation Repositories

| Repo | Update Cadence | Content |
|------|----------------|---------|
| **xairy/linux-kernel-exploitation** (GitHub) | Bimonthly | Categorized CVE links, exploit availability, kernel version ranges |
| **0xMarcio/cve** (GitHub) | Per-CVE | PoC exploits, e.g., CVE-2024-1086 universal LPE (v5.14–v6.6) |
| **tylzars/awesome-vrre-writeups** (GitHub) | Community PRs | Curated list of vulnerability research writeups |
| **Jalexander798/JA_Tools-Cybersecurity-Resource-2** (GitHub) | Ongoing | Personal collection of blog posts, writeups, tools |

---

## Vendor / Authority Feeds

| Feed | Use Case |
|------|----------|
| **CISA Known Exploited Vulnerabilities (KEV)** Catalog | Ground truth for in-the-wild exploitation; prioritize patching |
| **Ubuntu Security Notices** (ubuntu.com/security/notices) | Distro fix status, backport info |
| **Debian Security Advisories** | Same, for Debian-based |
| **Red Hat Security Data API** | Enterprise distro coverage |
| **LWN.net Kernel Coverage** (lwn.net/Kernel/Index) | Technical analysis of mainline fixes, commit-level detail |

---

## Conference / CTF Archives (High-Signal)

| Venue | Why It Matters |
|-------|----------------|
| **Black Hat USA / EU / Asia** | Weaponized chains, novel primitives, vendor responses |
| **DEF CON** (Main Track + Villages) | Red team tooling, hardware, RF, satellite, automotive |
| **BlueHat** (Microsoft) | Windows kernel, Hyper-V, Azure, mitigation deep dives |
| **Pwn2Own** (Toronto, Vancouver, Automotive) | Full chains against hardened targets (Chrome, Safari, Windows, VMware, Tesla) |
| **Tianfu Cup** | Chinese researcher chains, often novel Linux/Android kernels |
| **Hardwear.io** | Hardware/firmware/embedded exploitation |
| **OffensiveCon / ZeroNights / REcon** | Reverse engineering, binary exploitation, tooling |

---

## Search Query Templates (Proven Effective)

```bash
# Deep Linux kernel exploitation (last 6–12 months)
"CVE-2024" OR "CVE-2025" "Linux kernel" exploit writeup "double-fetch" OR "use-after-free" OR "race condition" OR "slab out-of-bounds" site:github.com OR site:googleprojectzero.blogspot.com OR site:zerodayinitiative.com

# Heap/LFH/JIT techniques
"heap feng shui" OR "LFH" OR "Low Fragmentation Heap" OR "JIT spraying" OR "ROP chain" OR "COOP" OR "JOP" OR "SROP" exploit technique 2024 2025

# Hardware / side-channel
Rowhammer OR "DRAM bit flip" OR "Spectre" OR "Meltdown" OR "microarchitectural" OR "side-channel" 2024 2025 new variant

# Web / auth bypass
"CSRF token bypass" OR "token smuggling" OR "session fixation" OR "OAuth flow hijack" OR "SAML injection" OR "JWT algorithm confusion" 2024 2025 writeup
```

---

## Enrichment Checklist (Per Intel Item)

- [ ] CVE ID / Advisory URL
- [ ] Root cause mechanism (one sentence)
- [ ] MITRE ATT&CK: Tactic + Technique IDs
- [ ] Target class (kernel version, config flags, OS, deployment)
- [ ] Detection difficulty (Low/Medium/High + rationale)
- [ ] Exploit maturity (Concept / PoC / Weaponized / In-the-wild)
- [ ] Public PoC / exploit repo URL
- [ ] Fix commit / vendor advisory
- [ ] Detection signals (auditd, eBPF, WMI, kernel logs, memory forensics)
- [ ] Related CVEs / variant family

---

## File Layout (Intel Directory)

```
/home/nova/.hermes/intel/cybersecurity/
├── CVE-2025-37752-two-bytes-of-madness.md
├── CVE-2025-37947-ksmbd-oob-write.md
├── CVE-2025-0927-hfsplus-slab-oob.md
├── ...
└── README.md  (index of all items)
```

Each file follows the enrichment checklist as frontmatter + narrative body.