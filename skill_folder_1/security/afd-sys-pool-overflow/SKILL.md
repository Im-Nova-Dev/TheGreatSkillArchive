---
name: afd-sys-pool-overflow
title: AFD.sys Kernel Pool Overflow Exploitation
description: Teach Windows kernel pool overflow exploitation through afd.sys (Ancillary Function Driver for WinSock), covering IOCTL analysis, pool Feng Shui, and CVE-2026-21236 case study for red teams and CTFs
tags: [windows-kernel, pool-overflow, driver-exploitation, afd, red-team, ctf]
related_skills:
  - name: windows-driver-exploit-development
    overlap: share kernel pool internals, double-fetch, and pool Feng Shui
    why_prefer_this: use when the vulnerability surface is an IOCTL-facing kernel network driver and the goal is a concrete AFD.sys exploitation pathway
---

# AFD.sys Kernel Pool Overflow Exploitation

Use when teaching or practicing user-to-kernel exploitation through 'afd.sys' (Ancillary Function Driver for WinSock), especially when the vulnerability class is a kernel pool overflow, out-of-bounds copy, or size-check omission in an IOCTL/socket handler.

## Why AFD.sys Is Worth Studying
- 'afd.sys' is the kernel-side implementation of the Windows Winsock API. User sockets flow through it via 'IOCTL's, so direct kernel input validation flaws appear here without relying on third-party drivers.
- It interacts with TCP, UDP, Raw sockets, and SAN/RDMA endpoints. San/RDMA handlers carry a larger, sparser code surface that has historically shipped bounds-check defects.
- It is an ideal teaching vehicle for pool overflow exploitation, because it produces deterministic pool allocations that are groomable from usermode, similar to anti-malware filter drivers but without requiring an installed AV product.

## Known Concrete Case: CVE-2026-21236
- Affected component: 'afd.sys'
- CVE: CVE-2026-21236 (Windows Kernel Elevation of Privilege)
- Disclosure date: 2026-02-11
- Researcher: Emily Liu (NCC Group)
- Root cause: 'AfdSanConnectHandler' performs a 'memcpy' from a usermode-controlled buffer into a kernel pool allocation without validating destination buffer size.
- Exploitation path:
  1. Create an 'AF_INET' socket and acquire the associated kernel 'AFD_ENDPOINT' object via 'NtCreateFile'.
  2. Configure and submit the 'AfdSanConnectHandler' IOCTL with a crafted source buffer and an oversized length argument.
  3. Overflow the target 'NonPagedPool' or 'NonPagedPoolNx' chunk, corrupting adjacent pool metadata or object headers.
  4. Use the corruption for arbitrary kernel memory read/write.
  5. Achieve privilege escalation by stealing the access token of a SYSTEM process or modifying current process token privileges.
- Mitigation added: explicit boundary validation using the IRP stack-allocated length before 'memcpy'.

## Teaching Exercises
1. **Pool allocation behavior mapping**
   - Instrument kernel pool behavior with 'gflags /i afd.sys +ust' and WinDbg.
   - Correlate specific IOCTLs to pool tag allocations and free patterns.

2. **Reproducing CVE-2026-21236**
   - Build a PoC using Python ('ctypes' or 'win32api') to send the vulnerable IOCTL.
   - Observe pool corruption in WinDbg and validate with a targeted crash signature.

3. **Pool Feng Shui via AFD.sys**
   - Use non-SAN IOCTLs to flood 'NonPagedPoolNx' with predictable-sized allocations.
   - Groom the pool so that the SAN connect handler overflow hits a target object (e.g., a controlled file object header).

4. **Detection evasion**
   - Understand how pool tag validation and lookaside list integrity checks trigger on corruption.
   - Plan exploitation around standard Windows pool hardening to avoid immediate bugcheck.

5. **Defense-in-depth**
   - Draft detection rules for Sysmon/ETW around high-frequency SAN connect attempts or 'AfdSanConnectHandler' IOCTL usage.
   - Design driver hardening guidance: enable Driver Signature Enforcement (DSE), restrict access to device objects via SDDL.

## Required Tools
- IDA/Ghidra for 'afd.sys' reverse engineering.
- WinDbg + local kernel debugging.
- Python + 'ctypes' / 'win32api' for usermode IOCTL harness.
- 'poolmon.exe' (Windows Performance Toolkit) for pool tag profiling.

## Mapping to General Skill
This AFD.sys-focused skill is most useful when teaching a red team or CTF track where the attacker's surface is known to include a Winsock-facing kernel component. It is designed to complement 'windows-driver-exploit-development', not replace it.
