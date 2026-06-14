---
name: xfs-self-healing-fserror-design
description: Teach Linux XFS autonomous self-healing filesystem design and fserror internals at the mechanistic level. Covers anonfd event notification, kernel/userspace health hook paths, priority inversion fixes across v4–v6, systemd + fanotify auto-start, and interactions with iomap media verification.
---

# XFS Autonomous Self-Healing and fserror Design

## Core Teaching Goal
Explain how XFS turns metadata corruption and I/O errors into actionable userspace events without blocking unmounts or introducing priority inversions. Go below "how to use" into the actual code paths, data structures, and cross-layer interactions.

## Background and Problem Space
Filesystems already detect I/O errors and metadata inconsistencies during runtime, but the information often stays in kernel logs or requires an administrator to run `xfs_repair` manually under unmounted conditions. Autonomous self-healing aims to:
1. Observe failures as close to the origin as possible.
2. Queue structured events for userspace.
3. Trigger repair automatically while preserving forward progress.

## High-Level Architecture

```
iomap / XFS writeback + IO completion
        |
        v
  xfs_health hook (tracepoints + anonfd queue)
        |
        v
  anonymous inode (anonfd) read() by xfs_healer daemon
        |
        v
  xfs_online_repair  -- fixes while fs is mounted
```

- The anonymous inode is created per mounted XFS instance.
- `CAP_SYS_ADMIN` is required to open the anonfd; otherwise the event stream is inaccessible.
- A `max event lag` bounds the ring to prevent unbounded memory growth during corruption storms.

## Patchset Version Progression (mechanistic lessons)
Each version fixed a concrete systems issue:

- v4: Multi-client support used indirect calls through function pointers. Drops this to use direct calls, eliminating extra cache misses and pointer-chasing in the hot report path.
- v5: Adds `verify-media` ioctl and collapses helper functions because the healthmon code had grown fragmented.
- v6: Fixes priority-inversion breaking bugs. Earlier versions could block higher-priority kernel paths waiting for userspace daemon I/O. v6 decouples the report from the wait by making the queue non-blocking and honoring a maximum lag.

## Cross-Subsystem Interactions

### iomap
XFS hooks into iomap completion to inspect `bio->bi_status`:
- `BLK_STS_MEDIUM`, `BLK_STS_IOERR`, and `BLK_STS_TARGET` map to different event classes.
- bio status flags are filtered carefully in v6 to avoid swallowing transient errors.
- This connection makes XFS one of the first filesystems to route iomap-generated failures into a structured recovery channel.

### fanotify + systemd
A starter service watches via fanotify and auto-starts `xfs_healer` when the XFS filesystem is mounted. This is important because:
- Repair must run with knowledge of the mounted filesystem state.
- systemd manages lifetime so the daemon does not prevent unmount when no repair is in flight.

### fserror infrastructure
Christian Brauner’s `fserror` provides generic filesystem error reporting primitives consumed by XFS. For teaching, this is a case study in:
- Layered error reporting: raw media error -> block layer -> iomap bio -> filesystem health event.
- Why generic hooks matter: they allow multiple filesystems to share notification plumbing without duplicating code.

## Data Structures and Code Paths

### xfs_health and xfs_healthmon
- `struct xfs_health` lives on the mount structure; one per mounted filesystem.
- `struct xfs_healthmon` owns the anonfd, event ring, and daemon interactions.
- Event records are C structs queued onto a ring buffer. Each record contains:
  - event class (metadata, io error, state change)
  - inode / ag number / extent range when applicable
  - timestamp

### xfs_notify_failure
- Hooks the `notify_failure()` callback chain used for fsdax and media errors.
- Translates block-layer failure codes into XFS health events.

### xfs_ioctl verify-media
- New ioctl allows userspace to ask the kernel to verify a region or device and report results via the health channel.
- This closes the loop: healer daemon can request proactive verification and observe results.

## Concurrent and Priority Considerations
- Event queuing must be safe under memory pressure; if the ring is full, events are dropped but metrics/counters continue to increment.
- Priority inversion fix in v6: earlier code could hold kernel locks while writing to userspace through the anonfd, which is unacceptable in filesystem paths that need to remain preemptible.
- Pattern to study: defer all blocking I/O to the reader side of the anonfd; kernel side merely copies event records into a pre-allocated ring.

## Hardening / Exploit Considerations
- Malformed event records in the anonfd can cause `xfs_healer` to misinterpret ranges or corrupt metadata via `xfs_online_repair`.
- The verify-media ioctl must validate extent alignment and bounds before issuing read requests to avoid kernel oops from crafted input.
- `CAP_SYS_ADMIN` gating on the anonfd is a hardened check, but any local privilege escalation to `CAP_SYS_ADMIN` would grant access to raw health events that could leak filesystem structure information.

## Teaching Exercises and Study Order

1. Trace the code path from `bio_endio()` through `xfs_io_end()` to `xfs_health_record_event()` in `xfs_health.c`. Identify where the lock discipline changes between v4 and v6.
2. Read `fs/xfs/xfs_healthmon.c` and map the anonfd ring buffer state machine: producer (kernel health hook), consumer (xfs_healer), overflow policy.
3. Examine `xfs_ioctl.c` verify-media ioctl: what flags can userspace pass, and how does the kernel translate them into media verification requests?
4. Compare the XFS self-healing event model with `ext4` error injection and `btrfs` device stats. How does the generic `fserror` layer unify or diverge?
5. Identify why priority inversion arose in v4 and reproduce the fix conceptually: how does a ring buffer with a consumer in userspace avoid blocking kernel writers?

## Related Skills and Intel
- `filesystem-buffer-manager-btrfs-ext4-folio` (xarray/extent-buffer concurrency).
- `linux-mglru-reclaim-loop-internals` (dirty folio writeback and reclaim interactions).
- `vfs-memory-reclaim-deadlock` (VFS-to-MM reclaim and GFP flag interactions).
- intel/systems/2026-06-05-xfs-autonomous-self-healing-v6.md
