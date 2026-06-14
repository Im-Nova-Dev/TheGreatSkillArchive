---
name: linux-af-packet-race-escape
description: Linux Kernel AF_PACKET UAF Race and Container Escape. Covers AF_PACKET internals, use-after-free primitives, use of PACKET_RX_RING and fanout to exploit kernel races, detection difficulty, and practical lab setup for privilege escalation via network namespace escape.
version: 1.0.0
category: red-teaming
---

# Linux AF_PACKET UAF Race and Container Escape

Technical foundation for offensive exploitation of classes like **CVE-2025-38617**: 20-year-old use-after-free races in `net/packet` yielding container escape and local privilege escalation on Linux.

## 4. Container Escape Application

---

## Prerequisites

- Linux kernel internals: memory allocator (SLAB/SLUB), socket buffers (`sk_buff`), namespaces.
- Userspace C/Python; comfortable with raw sockets, `sendmsg`/`recvmsg`, `mmap`, `setsockopt`.
- Container runtime knowledge (Docker, Kubernetes pods, capabilities).
- Optional: Kernel debugging with QEMU + `gdb`, `ftrace`, `kprobes`, `syzkaller`.

---

## 1. AF_PACKET Surface Area

`AF_PACKET` provides Layer-2 raw access and is frequently granted to containers for monitoring/forwarding.

Key paths and syscalls:
- `socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))`
- `setsockopt(..., PACKET_RX_RING / PACKET_TX_RING, ...)`
- `mmap(...)` for packet ring buffers
- `setsockopt(..., PACKET_FANOUT, ...)`
- `bind()` / `sendto()` / `recvfrom()`

Ring buffer modes:
- TPACKET_V1/V2/V3 (`tpacket` family) — used historically in exploits.
- `PACKET_RX_RING` with `tpacket3_hdr` supports multi-block rings; concurrent setup/teardown is where races occur.

---

## 2. Root Cause Classified: Use-After-Free in `packet_set_ring`

The bug class centers on:

1. Thread A calls `packet_set_ring()` to allocate a ring and attaches `mmap`ed pages.
2. Thread B triggers deallocation (`packet_release()` path).
3. Competing sibling or cross-thread `fanout` operations hold stale references to freed `block_desc` / page structures.
4. Reallocation of those same pages introduces attacker-controlled content (or at least attacker-controlled metadata through controlled mappings) at the freed object's virtual address.
5. Dereference yields kernel memory corruption / info leak / ROP entry.

Concurrency amplifiers:
- Shared fanout groups and rollover between `TPACKET_V1/V2`.
- Colliding `req` parameters (block size, frame size, nr_blocks) on multiple CPUs.
- Abrupt `close()` of sockets during another's `recvmsg()`.

---

## 3. Exploitation Primitive

### Phase A — Probe for UAF Window

Goal: Teardown ring while another thread still has it mapped.

```c
for (cpu = 0; cpu < ncpu; cpu++) {
    pthread_create(&tid[cpu], NULL, worker, arg);
}

void *worker(void *arg) {
    while (1) {
        int s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
        struct tpacket_req req = { .tp_block_size = 1<<18, .tp_block_nr = 64,
                                   .tp_frame_size = 2048, .tp_frame_nr = 0 };
        setsockopt(s, SOL_PACKET, PACKET_RX_RING, &req, sizeof(req));
        mmap_ring(s);
        bind_ether(s, ifindex);
        usleep(rand()%500);
        close(s);
    }
}
```

Spin many threads per CPU; vary `tp_block_nr` to create asymmetric frees.

### Phase B — Stabilize and Detect

- Monitor `/proc/diskstats` / `softlockup` messages (`Panic on softlockup` to triage).
- Use `gdb` attached to a QEMU VM; set a watchpoint on a `skb` or `block_desc`.
- Best detection: certain reproducible kernel `BUG: unable to handle page fault` or `KASAN: use-after-free`.

### Phase C — Abuse Freed Object

If freed page is reused by attacker-controlled `mmap` (possible in some kernel configs where user page is re-inserted into ring), attacker can:
- Place a ROP chain or function-pointer payload.
- Trigger a dereference via crafted `recvmsg()` result path or fanout update ioctl.

For **info leak** (more common pre-code-exec):
- Map known patterns across candidate reused pages.
- Read back via `recvfrom()` data or via side channel (`CacheBleed`-style indirect) to recover kernel base.

---

## 4. Container Escape Application

Kubernetes / Docker defaults often expose `CAP_NET_RAW` in pods:
- Default Docker bridge network keeps `CAP_NET_RAW`.
- Exception: `--cap-drop=ALL` or seccomp profiles that block `socket(AF_PACKET)`.

Exploit chain inside a container:
1. Build and run the race workload inside the container.
2. Achieve kernel UAF -> root on container namespace.
3. Use host `netns` reference via `/proc/<pid>/ns/net` after scanning or wait for host procfs access.
4. Escalate to host root if host kernel is also unpatched.

---

## 5. Detection Difficulty

**High** on modern systems absent in-kernel UAD/UBSan or explicit syscall auditing.

Indicators:
- Massive `socket(AF_PACKET)` / `setsockopt` churn from one process.
- Repeated `mmap`/`munmap` of `PACKET_RX_RING` mappings from unprivileged processes.
- Seccomp audit denials for `socket(AF_PACKET, SOCK_RAW, ...)` are golden signals.
- Kernel Oops messages mentioning `packet_set_ring`, `fanout`, or `tpacket_rcv`.

Blue team mitigations:
- Drop `CAP_NET_RAW` from containers unless strictly required.
- Apply seccomp profile blocking: `socket(AF_PACKET)`, `setsockopt(PACKET_RX_RING)`, `setsockopt(PACKET_FANOUT)`, `setsockopt(PACKET_TX_RING)`.
- Monitor container runtime for unexpected capability additions.
- Enable kernel lockdep / KASAN in testing to surface the race.

---

## 6. MITRE ATT&CK Mapping

- **T1068** – Exploitation for Privilege Escalation
- **T1611** – Escape to Host
- **T1203** – Exploitation for Client Execution
- **T1082** – System Information Discovery
- **T1059.003** – Command and Scripting Interpreter: Unix Shell (post-exploitation)

---

## 7. Hands-On Lab

Environment: Ubuntu 22.04 VM + QEMU, kernel 5.15.x without CVE-2025-38617 backport (confirm via `uname -r` and distro patch notes).

1. Confirm feature availability:
   ```sh
   zgrep -i CONFIG_PACKET /boot/config-$(uname -r)
   zgrep -i CONFIG_PACKET_FANOUT /boot/config-$(uname -r)
   ```
2. Build and run a multi-threaded ring allocator stressor (above pseudocode, expand to ~80 threads).
3. Reproduce with `stress-ng --af-packet N` if available, or custom binary.
4. Capture kernel log: `dmesg -w`.
5. Harden: observe behavior change after adding seccomp block or dropping caps.

---

## 8. Related Techniques

- Linux kernel slab manipulation via `SLUB` freelist feng shui with `userfaultfd`.
- `io_uring` ZCRX races (`io_uring-zcrx-internals` skill).
- `AF_XDP/XSK` zero-copy packet receive races.
- Windows `ALPC` / `FltMgr` object manipulation for LPE.

---

## References

- https://blog.calif.io/p/a-race-within-a-race-exploiting-cve
- https://nvd.nist.gov/vuln/detail/CVE-2025-38617
- https://security-tracker.debian.org/tracker/CVE-2025-38617
- Linux kernel `net/packet/af_packet.c` history in `packet_set_ring` / `tpacket_rcv`
