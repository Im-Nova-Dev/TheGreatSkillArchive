---
name: ptrace-credential-disclosure-and-privilege-reuse
title: ptrace Credential Disclosure and Privilege Reuse Exploitation
description: Teach ptrace-based credential disclosure and privilege reuse including CVE-2026-46333, credential-dropping race conditions, pidfd_getfd capture primitives, and host-based detection/blue team defenses. Covers attack surface, exploitation workflow, detection evasion, and red team usage patterns.
triggers:
  - ptrace credential disclosure
  - pidfd_getfd capture
  - credential dropping race
  - __ptrace_may_access race
  - ptrace LPE Linux kernel
  - local root via ptrace
  - setuid process fd capture
---

# ptrace Credential Disclosure & Privilege Reuse Exploitation

## When to use this skill

Use when teaching, practicing, or defending against attacks that exploit ptrace subsystem race conditions to capture privileged file descriptors, credentials, or IPC channels from set-uid/set-gid/root processes during exit or credential-dropping transitions. Includes:

- CVE-2026-46333 class: `__ptrace_may_access()` race + `pidfd_getfd(2)`
- setuid binary exploitation (pkexec, chage, ssh-keysign, accounts-daemon)
- Local shell → root privilege escalation with high reliability
- Host-based detection and Blue team hardning

---

## Core Concept

Modern Linux privilege separation relies on `dumpable` flags to gate `ptrace()` to privileged processes. CVE-2026-46333 reveals that `__ptrace_may_access()` is not atomic with respect to the credential drop in `do_exit()`: a privileged process may remain ptrace-attachable briefly after its UID has changed and its dumpable flag has been cleared.

Attackers use this transient window to:
1. Attach to a privileged process
2. Reopen sensitive file descriptors into their own namespace via `pidfd_getfd(2)`
3. Reuse captured FDs with the original privilege context

This bypasses both discretionary access control and traditional audit boundaries, because the captured FDs retain the security context of the donor process.

---

## Prerequisites for Students

| Knowledge | Why |
|-----------|-----|
| Linux process credentials | UID/GID, filesystem UID, `dumpable`, ptrace scopes |
| ptrace subsystem internals | `PTRACE_ATTACH`, `PTRACE_GETFPREGS`, `__ptrace_may_access()` |
| `pidfd_getfd(2)` semantics | Cross-process FD capture via pidfd |
| setuid/setgid/capabilities | When to expect elevated privileges in child processes |
| Host-based monitoring | auditd rules, eBPF tracing, Falco / Tetragon |

---

## Exploitation Workflow

### Step 1: Target Enumeration

Identify set-uid/set-gid/root daemons:

```bash
# Classic
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null

# Live processes
ps -eo pid,user,group,comm --no-headers | awk '$2=="0" || $3=="shadow" {print}'
```

### Step 2: Timing Control

Race against `do_exit()` credential drop. Two strategies:

**Strategy A - Trigger-and-Race**: Force the privileged binary into a credential-dropping exit path, then compete to attach before dumpable is cleared.

**Strategy B - Direct Daemon Attack**: Target long-running root daemons that interact with unprivileged clients via authenticated channels (D-Bus, polkit). Wait for a transient state during normal operation.

### Step 3: ptrace Attachment

```c
// Minimal representation
pid_t target = fork(); // child = privileged process
if (target == 0) execl("/usr/bin/pkexec", ...);
// parent races __ptrace_may_access
ptrace(PTRACE_ATTACH, target, NULL, NULL);
waitpid(target, NULL, 0);
```

### Step 4: pidfd_getfd Capture

```c
int pidfd = syscall(SYS_pidfd_open, target, 0);
int fd = syscall(SYS_pidfd_getfd, pidfd, idx, 0);
// 'fd' is now readable in attacker namespace with privileged context
read(fd, buffer, sizeof(buffer));
```

### Step 5: Privilege Reuse

- Capture from `chage` → SSSD cache or `/etc/shadow`
- Capture from `ssh-keysign` → `/etc/ssh/ssh_host_ecdsa_key`
- Capture from `accounts-daemon` via D-Bus → systemd D-Bus activation → root shell
- Capture from `pkexec` → root polkit channel → root execution

---

## Detection Framework

### High-Value Detection Rules

| Signal | Source | Difficulty |
|--------|--------|------------|
| `ptrace(PTRACE_ATTACH)` to set-uid process from non-ancestor | auditd + eBPF | Medium — avoid false positives from legitimate debuggers |
| `pidfd_getfd(2)` from unprivileged process to privileged process | auditd raw_syscall | High — low baseline noise, clear IoC |
| `open()` on sensitive paths during target race | eBPF file mod check | Medium |
| rapid setuid binary exec → `_exit` → unexpected state changes | process lifecycle monitoring | Medium-High |
| D-Bus method call bypassing intended client on livable path | D-Bus monitor + audit | Low if full D-Bus logging enabled |

### Yama ptrace_scope=2 Mitigation

Setting `kernel.yama.ptrace_scope = 2` requires `CAP_SYS_PTRACE` for any cross-process attach, eliminating public exploit chains. For containers, enforce via seccomp-bpf or pod security standards.

### Auditd Rule Examples

```
auditctl -a always,exit -F arch=b64 -S ptrace -F a0=PTRACE_ATTACH -k ptrace_attach
auditctl -a always,exit -F arch=b64 -S pidfd_getfd -F a1!=0 -k pidfd_capture
```

---

## Exploitation Case Studies

### Case A: `/usr/bin/chage` + `/etc/shadow`

1. Trigger `chage -l <user>` in background
2. Race during credential drop to `ptrace`-attach to dying `chage` process
3. `pidfd_getfd` returns FD to `/etc/shadow` allocated earlier
4. Read shadow hashes offline

**Impact**: High-availability credential exposure for offline cracking

### Case B: `/usr/bin/pkexec` → Root Execution

1. Execute `pkexec` inside constrained environment (e.g., SSH `allow_active`)
2. Wait for credential-drop transition
3. Capture `pkexec`'s polkit-agent or D-Bus descriptor
4. Replay privileged polkit action grant to spawn root shell

**Impact**: Remote lateral movement escalation via SSH access

### Case C: `/usr/libexec/accounts-daemon` D-Bus Hijack

1. Wait for accounts-daemon healthy IPC session
2. Attach to daemon during maintenance window
3. Capture authenticated D-Bus FDs
4. Issue Account/UserAdmin calls as root

**Impact**: Persistent access through system daemon

---

## Edges and Pitfalls

- **Race Reliability**: The window is narrow. Exploit reliability depends on kernel scheduling quality. Real-time kernels may expand or shrink the window.
- **Kernel Version Restriction**: Requires `pidfd_getfd(2)` (v5.6+). Pure ptrace path without pidfd is much harder.
- **Container Context**: Containers typically run with `SYS_PTRACE` capability dropped. Root inside container `nsenter` may still reach host ptrace during shared process namespaces.
- **User Namespace Implications**: Inside a user namespace, unprivileged users may have effective ptrace permission that crosses namespace boundaries via threads/tasks.

---

## CTF Exercises

1. **Easy**: On a vulnerable kernel, attach `pidfd_getfd` capture to a `su` process, read its `/etc/shadow` FD, and decode the hash.
2. **Medium**: Write a reliable exploit for `pkexec` with minimal crash noise; include a retry loop to win the race on the first 5 attempts.
3. **Hard**: Detect and patch the race in a minimal kernel tree without breaking normal ptrace debugging workflows.
4. **Expert**: Chain CVE-2026-46333 with an initial web RCE foothold to perform full LPE in a simulated container breakout scenario.

---

## Defensive Architectures

### Immediate
- Apply kernel updates from vendor
- Set `kernel.yama.ptrace_scope = 2`
- Deploy auditd + eBPF rules as shown above

### Structural
- Avoid user namespaces in untrusted containers
- Isolate workloads with dedicated kernels (gVisor, Firecracker, Kata)
- Deny `SYS_PTRACE` capability in container runtimes
- Reduce surface: strip set-uid bits where not strictly required

---

## Red Team Operational Playbook

### SSH-Constrained Lateral Movement
Many environments allow SSH with `allow_active` console sessions for passwordless auth agents, but prevent interactive root. In this state:
1. Log in with low-priv user.
2. Spawn `pkexec` via `ssh -t host pkexec /bin/bash` or directly if agent is active.
3. Race `__ptrace_may_access()` during the `polkit-agent` attach phase.
4. Capture D-Bus polkit auth FD; replay action to spawn root shell.
5. Use `setpriv --reuid=0 --inh-caps=-all` to drop capability footprint while keeping UID 0.

### Container Escape Route
From inside a container with `SYS_PTRACE` or inherited host PID namespace:
1. Host PID namespace exposed via volume mount or host PID sharing.
2. Target a host SUID process spawned from inside container namespace.
3. `pidfd_getfd()` operates on host PID space if container sees host namespace.
4. Capture host `/etc/shadow` FD → crack → pivot to host root account.
5. Alternative: capture host ssh-agent socket → sign host SSH sessions from inside container.

---

## Evasion & Detection Bypass

### Circumventing `ptrace_scope=2` in User Namespaces
- User namespaces create independent YAMA LSM contexts.
- Inside unprivileged user namespace mapping, `ptrace_scope` defaults to the container's override.
- If shared with host PID namespace, ptrace permissions from inside can cross namespace boundaries via threads/tasks.

### Crash Noise Reduction
- Use a retry loop with pause on `SIGSTOP` / `SIGCONT` to settle target before attach.
- Avoid `PTRACE_O_TRACESYSGOOD` unless debug-style logging is acceptable.
- Post-capture, restore target's `dumpable` flag via `/proc/<pid>/attr/current` if writeable to delay OOM/audit noise.

### Anti-Forensics
- Clear `auditd` logs from container context via `audit -D` if runtime permits.
- Remove eBPF trace artifacts from `/sys/fs/bpf/` maps if owning namespace.

---

## CTF / CICD Exercises

1. **Easy**: Change target logic from `chage` to `useradd`; derive exploit path from SUID argument parsing.
2. **Medium**: Chain CVE-2026-46333 with CVE-2026-31431 (CopyFail) for multi-stage root-from-web scenario with container escape.
3. **Hard**: Write a kernel module to detect the `do_exit()` window with sub-millisecond precision using tracepoints.
4. **Expert**: Audit a real-world SUID binary; find the indicator that would reveal it’s in the Qualys target list without reading the advisory.

---

## References

- Qualys TRU: CVE-2026-46333 full advisory (May 20, 2026)
- `__ptrace_may_access()` and `do_exit()` interaction analysis
- `pidfd_getfd(2)` man7.org semantics
- Yama LSM documentation
- Falco ptrace rule reference
- Intel item: `/home/nova/.hermes/intel/cybersecurity/2026-06-05-cve-2026-46333-ptrace-pidfd-getfd-lpe.md`
