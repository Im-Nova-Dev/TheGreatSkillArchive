---
name: linux-kernel-page-cache-credential-disclosure-and-lpe
description: >
  Teach Linux kernel local privilege escalation primitives using page-cache manipulation,
  ptrace/dumpable races, and credential disclosure via pidfd_getfd(2). Use when analyzing,
  detecting or hardening Linux hosts against kernel credential-drop races, setuid/root daemon
  hijacking, AF_ALG page-cache writes (CopyFail class), and post-compromise escalation.
  Includes theoretical foundation, exploit mechanics, detection, defense, and CTF-style exercises.
triggers:
  - CopyFail
  - CVE-2026-31431
  - CVE-2026-46333
  - CVE-2026-43284
  - CVE-2026-43500
  - Dirty Frag
  - Fragnesia
  - ptrace credential disclosure
  - pidfd_getfd
  - page cache write
  - AF_ALG
  - setuid root privilege escalation
  - Linux privilege escalation
  - dumpable race
  - kernel ptrace path
  - credential disclosure
  - page cache manipulation
---

# Linux Kernel Page-Cache Credential Disclosure & LPE — Teaching Pack

## 0) Why This Module

Two tight exploitation classes hit the Linux mainline in 2026:
- CopyFail / Dirty Frag class: write through the page-cache / AF_ALG socket interface to corrupt
  SUID memory / shared files (CVE-2026-31431, CVE-2026-43284, CVE-2026-43500, CVE-2026-46300).
- ptrace credential-drop race: steal file descriptors or secrets from a SUID/root process as it
  drops privileges via `pidfd_getfd(2)` (CVE-2026-46333).

Both collapse the "local-only" barrier: an unprivileged shell becomes root or credential theft.

## 1) Core Concepts (Theory)

### 1.1 Page Cache & splice() Writes
- Linux caches file pages in memory; `splice()` / `sendpage()` can move data between a file and a
  socket without userspace copies.
- `AF_ALG` exposes the kernel crypto API to userspace. When an AEAD cipher is used in-place,
  overlapping source/destination pages can cause kernel to write plaintext into the *page cache*
  of the destination inode rather than scratch space.
- CopyFail uses this to flip pages owned by SUID binaries (e.g., `su`) still sitting in page cache,
  from 0→1 or NOP→`\x0f\x05` (`syscall`) to gain execution with elevated credentials.

### 1.2 Dumpable, ptrace, and pidfd_getfd()
- `dumpable` (in `task_struct`) controls whether ptrace, core dumps, and `/proc/<pid>/mem` access
  are permitted. A SUID process sets `DMP_FSUID` on exec; on exit it may reset.
- Race window: after privilege drop but before full `exit()`/`mmput()`, `__ptrace_may_access()` can
  still allow attach because `dumpable` is stale in another thread.
- Combine with `pidfd_getfd(pid, fd, flags)` (added v5.6-rc1) to copy an open fd from the dying
  privileged process into the attacker's fd table — e.g., `/etc/shadow`, SSH host private key,
  dbus-to-systemd fd.

### 1.3 Memory Fragmentation (Dirty Frag)
- ESP/esp4/esp6 (IPsec) and rxrpc manipulate sk_buff fragments. Under memory pressure and
  specific splittable-frag conditions, crafted UDP/IPsec packets can manipulate kernel heap
  metadata to leak or overwrite adjacent objects — including process credentials.
- Reliable: the race is in kernel networking and does not depend on userland process timing windows.

## 2) Exploit Mechanics (Practical)

### 2.1 CopyFail (CVE-2026-31431) — Stealthy / No Race

Key steps:
1. Open `AF_ALG` socket, bind `aead` alg with small key/iv.
2. `sendfile()` or `splice()` attacker-controlled buffer into socket.
3. Allocate/cache same page-backed inode as target SUID binary (e.g., by mmap-reading `su`).
4. Trigger crypto op so kernel writes into target's page-cache page in-place.
5. Flip one word in `su` body to change its logic or inject `int 0x80 / syscall` gadget.
6. Re-execute cached binary interpretation; payload runs with effective UID 0.

Detectability: low. Crypto op looks like ordinary kernel activity, no ptrace attach.

### 2.2 ptrace + pidfd_getfd Race (CVE-2026-46333)

Conceptual primitive — hardened environments may block actual root escalation, but fd theft
still works.

Steps:
1. Spawn or wait for privileged helper (e.g., `pkexec`, `ssh-keysign`, `chage`, `accounts-daemon`).
2. On a helper that will drop credentials short after exec, try attach via `ptrace(PTRACE_ATTACH)`,
  reading `dumpable` in a loop alongside `waitid()/waitpid()` harmonics.
3. Once attached, use `pidfd_getfd(target_pid, victim_fd, 0)` to clone fd into attacker.
4. Read secret file / dbus / credentials.
5. For `pkexec`: same path can re-exec request with hijacked bus fd to run arbitrary cmd as root.

Detection: medium-high. `ptrace` attach is logged (`audit`/`kernel.yama.ptrace_scope=1`).

## 3) MITRE ATT&CK Mapping

Tactic            | Technique                 | Note
------------------|---------------------------|-------------------------------------------
Privilege Escalation | T1053 (Scheduled Task/Job)  | Long-term persistence via SUID implant.
Privilege Escalation | T1059 (Command and Scripting Interpreter) | Execute as root via execveat/cached payload.
Credential Access   | T1555.003 (Credentials from Password Stores: /etc/shadow, keyrings)
Credential Access   | T1078 (Valid Accounts via SSH host key reuse)
Defense Evasion     | T1218 (System Binary Proxy Execution: su/pkexec hijacked)
Collection          | T1005 (Data from Local System: shadow, dbus state)
Persistence         | T1547.006 (Boot or Logon Autostart: cron/systemd timer planting)

## 4) Detection & Telemetry

| Layer | Signal |
|-------|--------|
| Audit / syscall | `ptrace`, `pidfd_getfd`, `process_vm_readv` near setuid-root exec |
| EDR / Kprobe | `aead`/`salg` AF_ALG opens + splice + same mmap region read for SUID binary |
| Integrity | Page-cache hash mismatch of SUID binaries; `verity` / `ima` catches if enabled |
| Network | `rxrpc`/`xfrm` unusual skb fragment operations in Dirty Frag variants |
| Behavioral | SUID binary closing after unusual open-fd set; abrupt uid change logs |

## 5) CTF-Style Exercises

1. Instrument a VM with `dmesg -w` + auditd; reproduce `pidfd_getfd` pid race against a custom
   setuid helper. Identify the 10-30ms window in `strace`.
2. Given a static `su` binary loaded into page cache, craft an `AF_ALG` test harness that flips a
   NOP sled over a target word. Measure PAGE_SIZE alignment requirements.
3. For Dirty Frag: build a netkit lab with `xfrm` state; simulate `esp4` packet injection and
   observe slab cache state in `/proc/slabinfo`.
4. Harden a container image for this class: list all capabilities, `NO_NEW_PRIVS`, `yama.ptrace_scope`
   settings, and predict which primitive survives.

## 6) Quick Reference

- Primary references: Qualys TRU advisory CVE-2026-46333; Greenbone CopyFail & Dirty Frag; xint.io CopyFail page-cache walkthrough; Microsoft Dirty Frag + Fragnesia.
- Kernel versions: vulnerable range spans Linux 4.10-rc1 through 6.x unpatched.
- One-line rule: any local shell on an unpatched default-install Linux now has a practical path to
  root or credential theft; treat "local access" as full compromise.
