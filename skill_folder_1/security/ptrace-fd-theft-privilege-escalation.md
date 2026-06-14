# Linux ptrace Exit-Race & FD Theft Privilege Escalation

Methodical teaching/red-team reference for CVE-2026-46333-class flaws: privileged file descriptor theft via a `do_exit()` race in the kernel ptrace path.

## When to Use This Skill
- Interpreting ptrace exit-race intelligence, including CVE-2026-46333 and similar kernel advisory reports.
- Encoding exploit steps, detection hooks, mitigation guidance, or hardening advice for this primitive.
- Building lab exercises around kernel fd theft.
- Mapping the technique to MITRE ATT&CK and documenting adversaries’ exploitation patterns.

## Exploit Development Workflow
1. Identify SUID/setgid helpers that open secrets before dropping privileges (e.g. `ssh-keysign`, `chage`).
2. Understand `pidfd_getfd(2)` and `pidfd_open(2)` per Linux man pages; confirm kernel v4.10+ target.
3. Instrument high-frequency helper launches from the attacker unprivileged namespace; measure race-window likelihood.
4. Prepare the exploit strategy:
   - Race-based: iterate over many spawns until the attacker-side `pidfd_getfd()` wins inside the window between `exit_mm()` and `exit_files()`.
   - Race-free alternative: target helpers with long slow shutdown paths where `mm` becomes NULL early.
5. Read duplicated fd via `read()`/`pread()`; confirm returned content matches secret material.
6. Prefer `setns()`/`unshare()` to avoid noisy TTY artifacts and make audit filtering harder.

## Detection Guidance
- Monitor `pidfd_getfd()` syscall calls paired with SUID helper exits via eBPF tracepoints (`sys_enter_pidfd_getfd`, `sys_exit_do_exit`).
- Observe transitions where `task->mm` becomes NULL while `files->fdt` retains root-owned entries.
- Yama `ptrace_scope` audit logging and `auditd` rules around `/usr/sbin/chage`, `/usr/lib/openssh/ssh-keysign`.
- Detect unknown local processes requesting `CAP_SYS_PTRACE` or spawning excessive short-lived privileged helpers.

## Hardening Recommendations
1. Apply kernel updates containing upstream `ptrace` dumpability logic fix.
2. Set `kernel.yama.ptrace_scope = 2` on multi-tenant hosts; monitor for unauthorized ptrace activity.
3. Remove unnecessary SUID/SGID bits from userland helpers when operationally feasible.
4. Disable unneeded `AF_ALG` crypto sockets inside containers via AppArmor/seccomp.
5. Rotate credentials stored in SUID helper memory after exposure windows; treat page-cache-only patched hosts as suspect.

## Threat Modeling Vocabulary
- **Tactic**: Privilege escalation, credential theft, host escape (container contexts).
- **Affected target class**: Linux kernels v4.10–patched versions; multi-user/CI/XCP-ng/XOA hosts.
- **Detection difficulty**: High; bypasses FIM by never touching on-disk secret files.
- **Reliability**: Medium-high; public exploits require many helper spawns but no custom shellcode.
- **MITRE ATT&CK**:
  - T1068: Exploitation for Privilege Escalation
  - T1555.003: Credentials from Password Stores
  - T1145: Private Keys
  - T1611: Escape to Host

## Worked Examples / Notes
- CVE-2026-46333 public PoCs: `ssh-keysign-pwn`, `ptrace_may_dream`.
- Combined with CVE-2026-31431 (Copy Fail page cache tampering), adversaries can chain privilege escalation with credential theft and memory-only patching for defense evasion.

## References
- Qualys TRU advisory for CVE-2026-46333.
- kernel.org commits `01363cb3fbd0`, `31e62c2ebbfd`.
- PenLigent/HackingLabs `ssh-keysign-pwn` technical narrative.
