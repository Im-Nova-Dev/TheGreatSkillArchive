{
  "name": "linux-page-cache-abuse-primitives",
  "description": "Teach Linux page-cache abuse primitives for red team, CTF, and incident response: Copy Fail, Dirty Frag, detection, eBPF tracing, and memory-corruption-only privilege escalation techniques.",
  "category": "security"
}

# Linux Page-Cache Abuse Primitives

Focus: analyze/use kernel page-cache write primitives from an unprivileged local context, with emphasis on Copy Fail (CVE-2026-31431) and Dirty Frag (CVE-2026-43284). Includes detection, IR triage, and safe lab verification.

## Core Concepts
- Page-cache-backed files are writable through kernel-internal scatterlist paths after `splice()` + `recvmsg()` on crypto/AF_ALG or net subsystem sockets.
- The corruption is memory-only: on-disk file data stays intact, so file integrity monitoring misses it.
- Successful exploitation relies on corrupting code loaded later via `execve()`, `read()`, or `mmap()`.
- Page cache is shared between containers and host, expanding impact from container breakout to node takeover.

## Procedure
1. Verify target kernel and loaded modules.
2. Identify exposure: `AF_ALG`, `algif_aead`, `esp4/esp6`, `rxrpc` module status.
3. Choose analysis path: red team = exploitation primitive; IR/blue team = detection, hunting, containment.
4. Correlate artifacts: auditd/eBPF trace of suspicious syscalls; unusual UID 0 transitions; `drop_caches` cleanup attempts.
5. Remediate with module/blacklist restrictions, seccomp/AppArmor/SELinux blocking, and kernel upgrades.

## Commands and Checks
- List loaded modules: `lsmod | grep -E 'algif|aead|esp4|esp6|rxrpc'`
- Block vulnerable modules:
  ```sh
  printf 'install algif_aead /bin/false\ninstall esp4 /bin/false\ninstall esp6 /bin/false\ninstall rxrpc /bin/false\n' > /etc/modprobe.d/pagecache-abuse.conf
  ```
- Auditd telemetry:
  ```sh
  auditctl -a always,exit -F arch=b64 -S splice -S recvmsg -S socket -F auid>=1000 -k pagecache_abuse
  ```
- eBPF quick-check path: `bpftrace -e 'tracepoint:syscalls:sys_enter_splice /uid != 0/ { @[comm] = count(); }'`
- Clear cached evidence after suspected compromise: `echo 3 > /proc/sys/vm/drop_caches` (note: also a post-compromise indicator)

## Detection Strategy
- Hunt for unprivileged users creating `AF_ALG` sockets and invoking `splice()` then `recvmsg()` chains on the same fd pair.
- Correlate with `setuid(0)` or `execve()` of binaries that were recently read from an unprivileged context.
- Look for `echo 3 > /proc/sys/vm/drop_caches` before/after privilege escalation events.
- In containers, alert on host-level page-cache mutations from containers requesting unusual `AF_ALG` operations.

## IR Triage
1. Preserve runtime memory and page-cache state before flushing.
2. Timeline suspicious `splice()`/`recvmsg()` with auditd/eBPF data.
3. Check for `drop_caches` execution before integrity scans.
4. Compare on-disk hashes to execve-loaded images via audit `SYSCALL` + `EXECVE` records to detect mismatch.

## Common Pitfalls
- Do not rely solely on file-integrity monitoring: page-cache primitives leave no on-disk change.
- Do not dismiss container-to-host impact: shared page cache means container escape can host-encompass the whole node.
- Restricting network access does not stop local exploitation; the primitives use local IPC and syscalls.

## References
- Microsoft Security Blog: CVE-2026-31431 Copy Fail
- Wiz Blog: Dirty Frag (CVE-2026-43284 / CVE-2026-43500)
- HackTricks: Copy Fail AF_ALG + Splice page-cache overwrite writeup
- oss-sec disclosure threads for CVE-2026-31431, CVE-2026-43284, CVE-2026-43500
