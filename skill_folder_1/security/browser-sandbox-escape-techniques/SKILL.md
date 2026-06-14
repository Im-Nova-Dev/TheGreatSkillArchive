---
name: browser-sandbox-escape-techniques
title: Browser Renderer Sandbox Escape Techniques
description: |
  Teach browser sandbox escape methodologies for red team/CTF: Win32k primitive abuses from renderer context,
  token manipulation, browser-specific syscall filters, exploitation from zero-byte length gadgets, and detection evasion.
---

# Browser Renderer Sandbox Escape Techniques

## When to Use This Skill
Use when you need to understand how sandboxed renderers can escalate privileges on Windows, macOS, or Linux,
how to reason about small arbitrary write primitives exploitable from browser context, or how modern mitigations
change sandbox escape tradecraft.

## Learning Objectives
1. Understand the browser sandbox model and renderer separation on major engines.
2. Learn common kernel primitive abuses reachable from renderer sandboxes.
3. Study token manipulation and alternate LPE strategies without token theft.
4. Map renderer escape techniques to MITRE ATT&CK techniques.
5. Diagnose detection blind spots for sandbox escapes and how to harden browsers.

## Prerequisites
- Windows kernel basics: handles, tokens, processes, `NtQuerySystemInformation` classes.
- x64 calling conventions and exploit primitives: arbitrary write, info leak.
- Familiarity with Chromium / Firefox sandbox architecture and broker/renderer model.

## Core Topics

### 1. Renderer-to-Kernel Attack Surface
- Key reachable APIs: `NtQuerySystemInformation`, `NtSetInformationProcess`, `NtUser*` family via `csrss.exe`
  delegation or GDI objects, `NtDuplicateObject` for handle abuse.
- Sandbox restriction surfaces: restricted tokens, Low Integrity, Win32k lockdown, syscall filtering,
  Chromium’s `SandboxWin32k` and Mozilla’s `UtilityProcess` separation.

### 2. 12-Byte Write Primitive (CVE-2026-40369 Pattern)
- Zero-length length bypass: `ProbeForWrite()` is no-op when `Length == 0`.
- 3× 32-bit writes may evade many memory-protection heuristics if targeted carefully.
- Practical target selection: process tokens, `PsGetCurrentProcess()` offsets, debug registers.

### 3. Token Forgery vs Token Theft
- Token theft via process handle is classic; forgery via `NtCreateToken`/`NtSetInformationToken`
  lets you build a clean SYSTEM token and avoid stealing from another process.
- Requirements: `SeCreateTokenPrivilege` implication and security descriptor crafting.
- Split role: user-mode payload does token structure assembly; kernel write sets privilege bits or fields.

### 4. Information Leakage from Renderer Sandbox
- WNF / shared memory / side-channel objects to leak kernel pointers.
- Timing side-channels for ASLR defeats.
- Using browser-internal objects with kernel-backed handles to probe memory.

### 5. Detection and Mitigation
- ETW/PP Monitoring: watch for large arrays of `NtQuerySystemInformation` from renderer with unusual classes.
- Kernel callback filtering for zero-length write paths in sensitive syscalls.
- Chromium flags: `--no-sandbox` vs `--disable-seccomp-filter-sandbox` trade-offs (baseline understanding).
- OS-level hardening: WDAC, VBS, HVCI, Kernel DMA Protection.

## MITRE ATT&CK Mapping
- **T1068**: Exploitation for Privilege Escalation (kernel vuln).
- **T1556**: Modify Authentication Process (token forgery).
- **T1003.006**: OS Credential Dumping — token manipulation variant.
- **T1059.003**: Command and Scripting Interpreter — Windows Command Shell if post-exploitation uses `cmd.exe`.

## CTF/Competition Guidance
- In Pwn2Own-style scenarios, prefer reliability over maximum stealth if rules allow.
- For wargames: prepare both a token-theft fallback and a token-forgery primary.
- Build heap / memory layout stability around the small write primitive.

## Exercises
1. Review `ExpGetProcessInformation` decompiled logic; identify which writes matter most for token fields.
2. Map the minimal renderer privileged operation set to a sandbox escape tree.
3. Write a minimal detector concept that flags suspicious `NtQuerySystemInformation` class `0xFD` use
   from a renderer process using ETW.
4. Compare CVE-2026-40369 to CVE-2026-6309 (Chrome Viz UAF) for kill-chain differences.

## References
- See intel item `/home/nova/.hermes/intel/cybersecurity/cve-2026-40369-browser-sandbox-escape.md`
- VoidSec writeup: https://voidsec.com/cve-2026-40369-browser-sandbox-escape/
- GitHub exploit reference: https://github.com/orinimron123/CVE-2026-40369-EXPLOIT
- Anthropic Mythos browser sandbox escape chain research: https://red.anthropic.com/2026/mythos-preview/
