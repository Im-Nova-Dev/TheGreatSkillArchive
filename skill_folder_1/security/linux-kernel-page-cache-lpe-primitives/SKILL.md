---
name: linux-kernel-page-cache-lpe-primitives
description: Teach Linux kernel local privilege escalation via page-cache corruption. Covers CopyFail, Dirty Frag, Fragnesia, AF_ALG + splice, skbuff shared-fragment handling, ESP-in-TCP/RxRPC attack paths, and mitigation + detection strategies.
---

# Linux Kernel Page-Cache LPE Primitives

Use this skill when teaching, writing, defending against, or reproducing Linux kernel local privilege escalations that corrupt page-cached files via in-kernel crypto write-what-where primitives.

## Scope & Trigger Conditions
Apply when:
- Researching or demonstrating `skbuff`, `AF_ALG`, `AIO`, `splice()`, or `NETLINK_XFRM` LPE chains.
- Analyzing DMA or in-place crypto backends that touch page-cache pages without proper COW.
- Defending against kernel exploits that bypass disk-based FIM by altering only memory.

Key CVE examples to reference:
- CVE-2026-31431 (CopyFail)
- CVE-2026-43284 / CVE-2026-43500 (Dirty Frag)
- CVE-2026-46300 (Fragnesia)

## Teaching Checkpoints

### 1. Page Cache Basics
- Linux page cache stores file-backed pages; modifications update memory but not on-disk data until writeback.
- Setuid binaries (`/usr/bin/su`, `sudo`, `ssh-keysign`) are prime targets because executing after cache corruption yields code execution as root.
- `read()` vs `mmap()` vs `splice()` behaviors regarding page flags.

### 2. Copy-on-Write (COW) Invariants
- `SKBFL_SHARED_FRAG` tells ESP whether page-cache-backed pages still need COW before decryption.
- If the flag is wrong, kernel performs in-place decryption on a shared page.
- Critical window: after sharing drops to zero, but the flag says shared.

### 3. Attack Surface: User Namespaces + Network Namespaces
- `unshare(CLONE_NEWUSER | CLONE_NET)` + `CAP_NET_ADMIN` grants attacker control over XFRM/AF_ALG without being root.
- Modern distros increasingly restrict unprivileged user namespaces (sysctl `kernel.unprivileged_userns_clone`, AppArmor, SELinux policy).

### 4. ESP-in-TCP / RxRPC Primitives
- Installs via `NETLINK_XFRM` with known keys (AES-128-GCM typical).
- RxRPC variant: no ESP needed; uses `rxrpc` module directly.
- TCP socket switching to `espintcp` ULP after queuing pages avoids early COW.

### 5. Keystream / Nonce Selection
- AF_ALG API exposes `recv()` that returns keystream chunks keyed by nonce bytes.
- Build 256-entry lookup table mapping every possible byte value to a nonce.
- Chosen byte XORs into target page; repeat per byte produces arbitrary writes.

### 6. Determining Target Pages
- `fincore()` or `mincore()` to confirm a file’s pages are in cache.
- `madvise(MADV_DONTNEED)` flushes pages; avoid before exploit.
- `posix_fadvise(POSIX_FADV_DONTNEED)` and `madvise()` after corruption can extend the window or reload.

### 7. Detection Theory
- FIM misses this entirely (disk unchanged).
- Memory forensics: compare critical setuid binary page-cache hashes against on-disk in `/proc/PID/pagemap`.
- EDR: unusual AF_ALG/XFRM activity from non-root users in containers or sandboxes.

### 8. Mitigation Checklist
- Disable `esp4`, `esp6`, `rxrpc` if not required (RHSB-2026-003 style).
- Restrict unprivileged user namespace creation (`kernel.unprivileged_userns_clone=0`).
- Apply live-patched kernels containing upstream `skbuff` coalescing fix (Fixes: `f4c50a4034e6`, `cef401de7be8`).
- Enable kernel memory write-protection / CFI where available.

## Lab / Example Exploit Flow
```
unshare(CLONE_NEWUSER | CLONE_NET)
create NETLINK_XFRM SA (AES-128-GCM)
build AF_ALG keystream table (256 nonces)
splice setuid-binary fd into TCP socket
set socket ULP to "espintcp"
send crafted packets targeting chosen page-cache pages
obs