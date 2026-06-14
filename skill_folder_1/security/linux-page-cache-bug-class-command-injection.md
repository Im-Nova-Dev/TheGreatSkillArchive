---
name: linux-page-cache-bug-class-command-injection
description: "Teach the shared Linux page-cache exploitation bug class across Dirty Pipe, Copy Fail, and Dirty Frag — including how in-place kernel writes, splice(), sk_buff frags, and CoW bypass enable unprivileged code execution and privilege escalation. Use when asked to explain past-CVE bug families, teach Linux LPE internals, or prepare red-team labs on page-cache primitives."
---
# Linux Page-Cache Bug Class: Dirty Pipe, Copy Fail & Dirty Frag

## Why this family matters
Three 2022–2026 kernel flaws share a single idea:
> The kernel reuses a read-only page-cache page inside a kernel data structure as a raw pointer, then performs an in-place write on it, assuming private ownership.

| CVE | Year | Sink | Primitive | Bypass target |
|---|---|---|---|---|
| Dirty Pipe `CVE-2022-0847` | 2022 | `pipe_buffer` | Page-cache overwrite via stale `PIPE_BUF_FLAG_CAN_MERGE` | CoW / pipe splice merge logic |
| Copy Fail `CVE-2026-31431` | Apr 2026 | `algif_aead` TX SGL | 4-byte STORE during `crypto_authenc_esn_decrypt()` byte rearrangement | Copy-on-Write guard missing for AEAD SGL |
| Dirty Frag `CVE-2026-43284` | May 2026 | `sk_buff` frag | 4-byte STORE (ESP) and 8-byte STORE (RxRPC) into non-linear skb frag | `skb_cow_data()` skipped when no `frag_list` |
| Fragnesia `CVE-2026-46300` | May 2026 | ESP `sk_buff` frag | Same page-cache overwrite via ESP | Single-variant ESP path |

## Core Linux primitives involved
1. **Page cache** — RAM cache of file data. Modifying it changes what *every process* reads from a file, even a read-only on-disk file.
2. **CoW (Copy-on-Write)** — normally private-copies shared pages before modification. The bug family exploits CoW bypass.
3. **splice() / MSG_SPLICE_PAGES** — moves data between file descriptors without user-space copy. Can pin a page-cache page reference directly inside an `sk_buff` or pipe buffer.
4. **sk_buff frags** — `struct sk_buff` stores packet data that may be split across non-contiguous fragments (`frags[]`) in addition to linear data.
5. **In-place cryptography** — code that writes decrypted output into the same buffer it read encrypted input from.

## Exploit schematic

```
Attacker                          Kernel
   |                                |
   | splice(fd_pagecache)           |
   |  -> skb.frags[0] = page_ref   |
   |                                |
   |        network Rx path         |
   |        crypto_authenc_esn_     |
   |        decrypt(skb.frags[0])   |
   |                                |
   +--- WRITE 4 bytes into page ----+
         (still read-only page)
         of /usr/bin/su or /etc/passwd
```

## Dirty Pipe quick recipe (pedagogical)
1. Open read-only file via memfd_create / splice page cache ref
2. Leak/write path via write() to pipe while another thread sees stale `PIPE_BUF_FLAG_CAN_MERGE`
3. Overwrites arbitrary readonly files (e.g. `/etc/passwd`)

## Copy Fail quick recipe
1. `splice()` target read-only file page into `algif_aead` SGL
2. Trigger AEAD decrypt that moves ESN high bytes — 4-byte arbitrary write at read-only page addr
3. Choose target: `/etc/passwd` line to null password or `/usr/bin/passwd` to shell

## Dirty Frag quick recipe (ESP variant)
1. `unshare(CLONE_NEWUSER|CLONE_NEWNET)` to gain net-ns + CAP_NET_ADMIN
2. `add_key("esp", ...)` + `socket(AF_ALG)` + `splice()` to plant page-cache ref into skb frag
3. IPsec ESP decrypt writes 4 bytes at a time into read-only `/usr/bin/su` page cache
4. 4×48 = 192 bytes overwritten — inject ELF trampoline; `su` becomes root shell binary

## Dirty Frag quick recipe (RxRPC variant)
1. `add_key("rxrpc", ...)` + `socket(AF_RXRPC)`
2. `splice()` page-cache ref of `/etc/passwd` into rxrpc sbuffer
3. 3×8-byte in-place decrypt writes clear password hash for root line to empty/blank
4. `su -` provides root without authentication

## Detection strategies
- Linux: `cat /proc/net/esp` + audit `add_key` calls by non-root users
- ETW/bpf: trace `splice()` from process groups not typically spawning crypto / rxrpc ops
- FIM: memhash-only misses page-cache overwrites; require live page-cache diff
- Host: alert on `su` executed by non-TTY / container host process flips to root uid
- Container: dropped privilege namespace creates noisy XFRM state

## Teaching progression
1. Start with page cache and file I/O basics (tmpfs vs ext4)
2. Add splice() and zero-copy mechanics
3. Introduce CoW semantics and why "read-only" is a property of inode flags, not page content
4. Walk through the three CVEs side-by-side highlighting sink differences
5. Build tiny kernel module or eBPF probe to observe `splice()` + skb frag state
6. Hands-on exploit reproduction in qemu/virtualized kernel at known-vulnerable rev

## Common pitfalls
- Updating `/usr/bin/su` on disk does nothing — exploit exists in page cache. Reboot or `drop_caches` first when investigating.
- Namespace requirements differ by distro: Ubuntu AppArmor blocks unprivileged user namespaces, requiring RxRPC path.
- RxRPC module not loaded by default in RHEL — exploit requires additional module load.
- No filesystem forensic evidence. Everything happens in RAM page cache.

## Keywords
linux-kernel-exploitation, page-cache, dirty-pipe, copy-fail, dirty-frag, privilege-escalation, CoW-bypass, splice(), sk_buff, eBPF, MITRE-ATT&CK-T1068
