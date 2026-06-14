---
name: windows-kernel-lpe-primitives
description: Windows kernel-mode local privilege escalation primitives, including user-mode interaction pitfalls, driver attack surfaces, and detection considerations.
---

# Windows Kernel-Mode LPE Primitives

This skill covers offensive concepts for identifying, exploiting, and detecting local privilege escalation bugs in Windows kernel-mode components.

## 1. Attack Surface Overview
Kernel-mode drivers expose IOCTLs, named objects, symbolic links, callbacks, and network stacks (e.g., HTTP.sys, AFD.sys). Low-privileged attackers target these surfaces to reach kernel execution.

## 2. User-to-Kernel Data Path Pitfalls
- **C-string truncation**: `strcat`, `sprintf`, and similar functions stop at the first null byte. Kernel exploit payloads often contain binary pointers with embedded nulls. Use `memcpy`, explicit lengths, or raw socket writes.
- **Buffer size miscalculation**: Validate whether the kernel path uses byte counts or character counts.
- **Type confusion**: Ensure user-mode structures match kernel-mode structure packing (`#pragma pack` and 64-bit alignment).

## 3. NTFS Driver Attack Surface (Case Study: CVE-2025-32707)
- The Windows NTFS driver (`ntfs.sys`) is loaded on boot and processes every file metadata operation on NTFS volumes.
- It is exposed via `NtFsControlFile`/`FsRtl` fast-IO paths, not just conventional IOCTLs.
- **CVE-2025-32707**: Out-of-bounds read in NTFS when parsing malformed file metadata. A local, unauthenticated attacker can trigger disclosure of kernel memory, leading to KASLR bypass and subsequent SYSTEM privilege escalation.
- Exploitation pattern:
  1. Craft a file with manipulated NTFS attribute fields (`$FILE_NAME`, `$DATA`, or `$INDEX_ROOT`).
  2. Force the driver to parse attributes via `NtCreateFile`/`NtQueryInformationFile`.
  3. The bug causes an out-of-bounds read in kernel pool memory, leaking `ntoskrnl.exe` base and pool layout.
  4. With KASLR defeated, chain to an arbitrary write primitive (often a separate, co-located pool overflow) and overwrite `_EPROCESS->Token` and `PreviousMode`.
- Detection beats:
  - NTFS handle operations (Event IDs 4656/4663 with `File Name` patterns pointing to temporary/artifact files).
  - Sysmon Event ID 10 (`CreateRemoteThread`) referencing `ntfs.sys` topic.
  - Crash dumps with `NTFS` frames and abnormal function pointers.
  - ETW tracing of `NtFsControlFile` and `FsRtl*` routines.
- Detection difficulty: Medium–High (local-only, low forensic footprint pre-exploit).
- Mitigation: Apply KB5002695; restrict NTFS volume access for low-privilege users where possible; monitor for unusual privilege escalations chained to NTFS I/O.

## 4. HTTP.sys Specifics
- The local HTTP service (`net start http`) listens on TCP/80 by default.
- Attackers can send crafted requests containing binary headers/body to trigger kernel bugs.
- Mitigation: restrict service start, monitor for unexpected `http` service changes, and patch.

## 5. Detection Strategies
- Monitor service creation: Windows Event ID 7040 / 7045 for HTTP service changes.
- ETW/kernel tracing for HTTP.sys IOCTL or request handling anomalies.
- Crash triage: commented BSODs with HTTP.sys in the stack trace are strong indicators.

## 6. Exploit Reliability Notes
- Null-byte truncation in payload transmission causes failed exploitation or random memory access.
- Field-tested PoCs often include build scripts to produce raw binary payloads; avoid text-oriented helpers.
- Blue-pill/BSOD is a common early result; reliable code execution may require additional primitives (arbitrary write, ROP, SMEP bypass).

## 7. Remediation and Hardening
- Apply vendor patches promptly.
- Remove or disable unneeded kernel services.
- Use HVCI/VBS and kernel-mode code signing policies to raise the bar.

## 8. References
- EDB-ID 52546 — Windows 11 24H2 HTTP.sys LPE (CVE-2026-21250)
- ZeroPath analysis of CVE-2025-32707: https://zeropath.com/blog/windows-ntfs-cve-2025-32707-privilege-escalation
- Microsoft Security Advisory for CVE-2025-32707: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32707
- Windows Internals Part 1 & 2
- Microsoft Security Response Center advisories for HTTP.sys
