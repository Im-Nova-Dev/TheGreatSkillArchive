# Linux Kernel LPE Families: Page Cache, Pipe, and Pointer Revalidation Attacks

**Category:** security / red-teaming  
**Skill type:** Teaching deep-dive for kernel exploitation students and red-team operators.  

---

## When to use this skill
Use this skill when teaching local kernel privilege escalation fundamentals, comparing exploitation families, or when a student asks why "Dirty Pipe" and "Copy Fail" are different from race-condition bugs like Dirty COW.

It covers:
- Dirty Pipe (CVE-2022-0847)
- Copy Fail (CVE-2026-31431)
- Dirty Frag (CVE-2026-43284 / CVE-2026-43500)
- Double-fetch (class of bug; multiple CVEs)
- GUP races (Dirty COW, CVE-2016-5195)

This skill deliberately skips broad Windows user-mode topics and focuses on *local* Linux kernel attack primitives involving file-backed memory and syscall path revalidation.

---

## Teaching progression

### 1. Core abstraction: page cache
- Linux buffers file pages in the **page cache** as 4K pages shared VM-wide.
- Page-cache pages can be simultaneously mapped into multiple processes via the page fault handler.
- Backing file does not have to be memory-mapped: ordinary `read()`/`write()` paths use page cache too.

### 2. Kinds of "write-through"
| Family | Mechanism | Canonical example |
|--------|-----------|--------------------|
| Pipe overflow | `splice()` moves pipe buffer into page-cache page; writeback bypasses mmap checks | Dirty Pipe |
| Crypto write-through | `algif_aead` / xfrm-ESP / RxRPC expose kernel-crypto write pointers to page-cache pages | Copy Fail, Dirty Frag |
| mmap/GUP race | `get_user_pages()` races with madvise or fork into MAP_PRIVATE; writes land in COW page, readable elsewhere | Dirty COW |
| TLB shootdown race | i915 gem objects mapped simultaneously into user and kernel, splices cause machine-check | newer GPU hacks |
| Double-fetch | kernel dereferences user pointer twice without revalidating CONTENT between fetches | assorted ioctl bug classes |

### 3. Copy Fail / Dirty Frag deep dive
- Summarize `algif_aead`, `xfrm`, `splice()`.
- Emphasize determinism: exploit is *not* a race.
- Emphasize cross-namespace impact: page cache is host-global.
- Compare to Dirty Pipe: same primitive class, different privileged interface.

### 4. Detection and mitigation
- `auditd` rules on `splice` + AF_ALG (`auditctl -a always,exit -F arch=b64 -S splice -F a0=...`) — precise but noisy.
- eBPF / Falco `splice` from AF_ALG to pipe.
- fs-verity / IMA signatures on setuid binaries.
- Runtime hardening: unload `esp4`, `esp6`, `rxrpc` (breaks IPsec/AFS); gVisor / Firecracker for tenants.

### 5. Lab exercises
1. Confirm Write-Through: `copy-fail-poc.py --read SUID_BINARY ADDR` in env with vulnerable kernel. Show page-cache corruption.
2. Inspect AF_ALG: `strace -e trace=splice,openat ./poc` to capture syscall patterns.
3. Detection: add Falco rule to alert on `splice` from `algif_aead` fd and inspect logs.
4. Mitigation test: confirm unprivileged users cannot exploit after blocking `esp4`, `rxrpc`.
5. Compare Families: ask students to plot Dirty COW / Dirty Pipe / Copy Fail on "race?" vs "deterministic" vs "requires capability" axes.

### 6. Thinking in attack families
Ask the student to generalize: "which kernel subsystems expose user-reachable write pointers into page-cache-backed memory, but skip `mmap`/`can_do_fork()` revalidation?" This is the abstraction frontier of Copy Fail-class bugs.

---

## Common misconceptions to address
- "Race conditions are necessary for Linux LPE" — no; Copy Fail-style bugs are deterministic.
- "Containers are safe from kernel bugs" — no; shared page cache breaks namespace isolation for local write-through primitives.
- "I can patch this with seccomp/AppArmor" — partially; seccomp may *block* `splice`/`AF_ALG` but not corrupt pages after an already-established bug class.
- "Exploiting needs source code" — not when PoC is 732-byte universal Python.

## Pitfalls and edge cases
- Some cloud kernels backport patches without changing version numbers; always verify against vendor advisory.
- `CAP_NET_ADMIN` required for Dirty Frag reduces exploitation via default pod seccomp; Copy Fail has no such requirement.
- `fs-verity` on `/usr/bin/sudo` neutralizes *this* attack vector only; attackers pivot to other setuid binaries if not covered.
- Page-cache poisoning via setuid `mv`/`cp`-style interactions can be reset by `echo 3 > /proc/sys/vm/drop_caches` but not on live-mounted bind mounts.

---

## Reference list
- Bugcrowd: Copy Fail / CVE-2026-31431 — https://www.bugcrowd.com/blog/what-we-know-about-copy-fail-cve-2026-31431/
- Wiz: Dirty Frag / CVE-2026-43284 + CVE-2026-43500 — https://www.wiz.io/blog/dirty-frag-linux-kernel-local-privilege-escalation-via-esp-and-rxrpc
- Wiz PoC repo — https://github.com/0xdeadbeefnetwork/Copy_Fail2-Electric_Boogaloo
- Dirty Pipe reference — https://dirtypipe.cm4all.com/
- AlmaLinux advisory — https://almalinux.org/blog/2026-05-07-dirty-frag/
