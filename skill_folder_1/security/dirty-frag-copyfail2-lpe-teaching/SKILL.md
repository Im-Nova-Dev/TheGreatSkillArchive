---
name: dirty-frag-copyfail2-lpe-teaching
description: Teach Dirty Frag / CopyFail2 (CVE-2026-43284, CVE-2026-43500) as a concrete Linux kernel LPE case study. Covers page-cache write primitives via xfrm-ESP and RxRPC, deterministic exploitation, malware adoption (Multiverze), detection via YARA, eBPF, and auditd, CTF-style exercises, patch/mitigation workflows, and how the technique extends prior CopyFail/Dirty Pipe lineages.
metadata: {"triggers":["dirty frag","copyfail2","cve-2026-43284","cve-2026-43500","page cache lpe","xfrm esp rxrpc privilege escalation"], "difficulty":"advanced", "att&ck":["T1068","T1210","T1105","T1059.004","T1070.006"], "cves":["CVE-2026-43284","CVE-2026-43500"]}
---

# Dirty Frag / CopyFail2 LPE Teaching

Use this skill when teaching offensive kernel exploitation, red-teaming Linux, writing detection for page-cache abuse, or running exploit-dev/CTF exercises on LPE chains.

## 1. Concepts to Reinforce
- **Page-cache corruption as an exploitation primitive** legitimate kernel paths (xfrm-ESP, RxRPC) writing to page-cache-backed memory not exclusively owned by the kernel
- **Deterministic, race-free exploitation** via splice-able file primitives vs. time-sensitive race windows
- **Credential and binary patching** through page cache to escalate privileges without on-disk binary replacement prior to execution
- **Trilogy lineage:** Dirty Pipe → Copy Fail → Dirty Frag; each builds on the previous page-cache abuse surface
- **Container/Kubernetes exposure:** even in containerized contexts, `CAP_NET_ADMIN` can bridge to node compromise

## 2. Grounding Exercise
Run the reference PoC in a lab kernel:
1. Identify kernel version; confirm likely vulnerable subsystem entries
2. Discover `esp4`/`esp6` and `rxrpc` module availability
3. Communicate findings: why does a networking subsystem write path let you overwrite unrelated page-cache content?

Demonstrate kernel backtracing via `tracepoint:sys_enter_splice` and `nf_tables` audit events.

## 3. Technical Walkthrough
High-level:
1. Phase 1: Identify page-cache-backed writable buffer reachable via xfrm-ESP or RxRPC
2. Phase 2: Use `splice()` to inject crafted content into the page cache
3. Phase 3: Trigger readback of that page-cache region to overwrite on-disk sensitive content
4. Phase 4: Execute modified binary/credential file to obtain root privileges

For detailed incident response data, see canonical intel file:
`/home/nova/.hermes/intel/cybersecurity/2026-06-05_dirty-frag-copyfail2-lpe-chain.md`

## 4. Detection & Defensive Exercises
### YARA Detection Exercise
Build a YARA rule for the V4bel shellcode using:
- `mov al, 0x6a; syscall` (`setgid(0)`)
- `mov al, 0x69; syscall` (`setuid(0)`)
- `mov al, 0x74; syscall` (`setgroups(0, NULL)`)
- `push 0x3b; pop rax; syscall` (`execve("/bin/sh")`)
- `/bin/sh` and `TERM=xterm` strings

### eBPF / Auditd Exercise
Trace `splice()` calls and XFRM/RxRPC-related syscalls from user-owned contexts. Baseline normal traffic; alert on unusual sequences from non-root users.

### EDR / FIM Exercise
Harden `/etc/passwd`, `/bin/*`, and credential binaries with integrity monitoring. Alert on kernel-capability grants (`CAP_NET_ADMIN`) to untrusted users.

## 5. CTF / Lab Problem Design
Build a contained challenge:
- Provide a VM with an older kernel, V4bel PoC, and an auditing script
- Students must identify the primitive, run the PoC, and write a detection signature
- Advanced extension: artificially inject `CAP_NET_ADMIN` via ambient capability and break out of a restricted container

## 6. Mitigation & Incident Response
Temporary mitigation:
```bash
sh -c "printf 'install esp4 /bin/false\ninstall esp6 /bin/false\ninstall rxrpc /bin/false\n' > /etc/modprobe.d/dirtyfrag.conf"
```

Incident response step:
```bash
echo 3 > /proc/sys/vm/drop_caches
```

Vendor patching sequence: kernel updates > container runtime hardening > capability minimization > auditd/eBPF monitoring.

## 7. Reference Readings
- Wiz Research: https://www.wiz.io/blog/dirty-frag-linux-kernel-local-privilege-escalation-via-esp-and-rxrpc
- ReversingLabs analysis and YARA: https://www.reversinglabs.com/blog/dirtyfrag-linux-privilege-escalation-exploit
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/05/01/cve-2026-31431-copy-fail-vulnerability-enables-linux-root-privilege-escalation/
- GitHub V4bel/dirtyfrag: https://github.com/V4bel/dirtyfrag
