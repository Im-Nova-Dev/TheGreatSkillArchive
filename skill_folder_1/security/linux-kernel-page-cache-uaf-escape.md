---
name: linux-kernel-page-cache-uaf-escape
description: "Practical teaching skill covering Linux kernel page-cache use-after-free exploitation for privilege escalation, container escape, and post-compromise root access, with emphasis on Dirty Frag / CopyFail2-family flaws and detection bypass considerations."
tags: [security, exploit-development, kernel, privilege-escalation, page-cache, container-escape, linux]
---

# Linux Kernel Page-Cache Use-After-Free Privilege Escalation

## Purpose
This skill teaches modern Linux kernel privilege escalation via **page-cache UAF and logic bugs** in memory-handling paths. Unlike traditional heap UAF, page-cache flips usable primitives into file-backed page reclaim and interaction with virtual filesystem/network stacks.

## When to Load This Skill
Use this skill when the task involves:
- Teaching kernel LPE via page-cache or file-backed page UAF.
- Researching Dirty Frag, CopyFail2, Fragnesia, or related 2026 disclosure families.
- Building detection, monitoring, or mitigation strategies for post-intrusion root access.
- Understanding how containerized environments inherit kernel attack surface.

---

## 1. Conceptual Model

```
Userland Process
  -> VFS / syscall boundary
  -> page cache reference (struct page, XArray, address_space)
  -> reclaim / truncate / writeback paths
  -> UAF window during RCU grace period or shrinking interval
  -> kernel ROP / code reuse
```

**Key difference from userspace heap UAF:**  
Kernel memory is mapped physically; controlling page-cache references changes who can free what, when swap/readahead/truncate race occurs.

---

## 2. Key Data Structures
- `struct page` – Refcounted page metadata; UAF happens after `put_page()` races an operation still holding stale pointer.
- `struct address_space` – Hosts radix tree/xarray of `page` pointers; truncate and hole-punch paths manipulate this without exclusive locking.
- `struct inode` – Truncate flows clear page-cache pages; stale references can be rejuvenated.
- RCU grace periods – Freed objects may remain accessible briefly through RCU read-side critical sections.

---

## 3. Dirty Frag / CopyFail2 / Fragnesia Attack Model

### 3.1 Dirty Frag (2026 disclosure)
- **CVEs:** CVE-2026-43284, CVE-2026-43500
- **Subsystems affected:** ESP / RxRPC networking stack + memory-fragment handling
- **Mechanism:** Ask kernel to create or handle fragmented memory; use crafted I/O to free an in-use page and reuse it.
- **Goal:** Achieve an arbitrary kernel read/write primitive. Typical primitives: modify `cred` struct for uid=0 or overwrite kernel code for ROP chain.
- **Container relevance:** Kubernetes pods run on host kernel; unless node-level seccomp/module blacklisting blocks the syscall path, unprivileged pod -> host root is feasible.

### 3.2 CopyFail2 (2026 disclosure)
- **CVE:** CVE-2026-31431
- **Mechanism:** Logic flaw in kernel copy path. Triggers heap fragmentation and controlled deallocation/reallocation of adjacent kernel heap objects, leading to controlled UAF.
- **Primitives produced:** heap feng shui; after winning layout, steal cross-cache references into page-cache-oriented objects.

### 3.3 Fragnesia
- **Mechanism:** Addresses page-cache memory handling where reclaim logic can leave stale entries; creates similar UAF windows after large memory pressure / compaction events.

---

## 4. From UAF to Root: Canonical Steps

1. **Trigger UAF** – Create race window (e.g., multiple threads / processes issuing syscalls where one frees while another dereferences).
2. **Feng Shui** – Spray pages, kmalloc slabs, or filesystem metadata objects to stabilize heap layout around target object.
3. **Realloc / Reclaim** – Reclaim freed object using controlled content (e.g., userfaultfd, remap_file_pages, or direct page insertion via /dev/mem or kernel text gadgets).
4. **Code Reuse** – Once stale pointer points to attacker-controlled memory, build ROP chain. Prefer `commit_creds(prepare_kernel_cred(0))` or built-in `swapgs_restore_regs_and_return_to_usermode` style trampolines.
5. **Stabilize** – Bypass SMEP/SMAP via ret2usr or ROP-only; bypass KASLR by infoleak or deterministic mapping.

---

## 5. Teaching Examples / Practice Targets

| Technique / Family | Primitive | Typical CTF or Lab |
|---|---|---|
| Page-cache truncation UAF | stale `struct page` | Linux kernel CTF challenges, customized VM |
| Dirty Frag ESP/RxRPC chain | arbitrary r/w | Proof-of-concept reconstruction in KVM/QEMU |
| CopyFail2 heap feng shui | cross-cache UAF | Guest kernel with debug symbols; run poc's against `netfilter` or `sock` subsystems |
| userfaultfd-assisted page reclaim | controlled realloc | Modified kernel module or sysctl-enabled environment |

### Minimal Detection Bypass Considerations
- Prefer kernel ROP over userland code injection to stay clear of SMEP.
- Avoid noisy kmalloc caches; reuse slabs that are already in use.
- Avoid persistent kernel modules; rely on transient ROP if possible.
- Hide artifacts: clear `dmesg` ring buffer, remove `/proc/*/maps` evidence, unlink PoC files.

---

## 6. Debugging & Validation Workflow

```bash
# Build target kernel with debugging and disable mitigations for lab use
make menuconfig   # enable CONFIG_DEBUG_KERNEL, disable CONFIG_RANDOMIZE_BASE

# Use QEMU with KVM for interactive exploit development
qemu-system-x86_64 -kernel arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0 root=/dev/ram oops=panic panic_on_warn" \
  -nographic -s -S

# From another terminal, attach gdb
gdb vmlinux
target remote :1234
```

**Monitor while reproducing:**
- `dmesg -w`
- `journalctl -k -f`
- `trace-cmd record -e 'page_cache*' -e '*uaf*' -e 'netfilter*'`
- `kprobe` based tracepoints on suspect functions.

---

## 7. Mitigation & Detection Perspective

### Workload Hardening
- Lockdown `CAP_SYS_ADMIN` to root only.
- Use `seccomp` and `AppArmor`/`SELinux` to deny exotic syscalls (e.g., `userfaultfd`, `memfd_create`, `bpf()`).
- Block or limit raw socket/network stack access for unprivileged users.
- Rotate kernels frequently; apply vendor patches for 2026 LPE families immediately.
- Kubernetes: enforce `allowedUnsafeSysctls: []`, module blacklists, and node-level seccomp.

### Detection Controls
- Alert on UID transitions from unprivileged to root in <1 second.
- Crash-loop CI systems that repeatedly invoke kernel-heavy containers; correlate with `SIGABRT` in compile/build pipelines.
- Monitor /var/log/kern.log, `auditd` rules for suspicious `ptrace`, `bpf`, `userfaultfd`, `keyctl` activity near privilege escalation events.
- Network telemetry for RxRPC/ESP usage from unexpected processes.

---

## 8. Glossary
- **UAF – Use-After-Free:** Memory freed while still reachable by active pointers.
- **Page cache:** Kernel cache for file-backed pages.
- **RCU – Read-Copy-Update:** Concurrency mechanism; object reuse during grace period is common UAF window.
- **Dirty Frag:** 2026 Linux kernel LPE involving ESP/RxRPC/memory fragments.
- **CopyFail2:** Floor/ceiling error in copy path leading to heap corruption.
- **Feng shui:** Heap/page layout manipulation to position objects predictably.

---

## 9. Further Reading
- Microsoft Security Blog – Active Attack: Dirty Frag Linux vulnerability expands post-compromise risk (2026-05-08)
- Huntress – "Panic at the Distro" (2026)
- Upwind – Dirty Frag Linux Privilege Escalation technical analysis
- CSA Research Note – Dirty Frag: Linux Kernel LPE Delivers Enterprise Root Access (2026-05-11)
- Securelist – Q1 2026 vulnerability landscape (2026-04-xx)
- Linux kernel source – `mm/filemap.c`, `fs/truncate.c`, `net/{esp,rxrpc}.c`
