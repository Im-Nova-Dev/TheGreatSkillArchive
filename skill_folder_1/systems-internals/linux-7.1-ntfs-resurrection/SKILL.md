---
name: linux-7.1-ntfs-resurrection
description: Mechanistic teaching module on the Linux 7.1 ground-up NTFS rewrite ("NTFS resurrection"). Covers coexistence with ntfs3, iomap + folio page-cache integration, NTFS $LogFile journal replay, mount-time superblock probing, BIO flag behavior, and database/data-recovery implications. Goes below "filesystem TUTORIAL" into how the kernel actually executes an NTFS write.
---

# Linux 7.1 "NTFS Resurrection" – Mechanistic Internals

**Source fetch date:** 2026-06-06
**Intel file:** `/home/nova/.hermes/intel/systems/2026-06-06-ntfs-resurrection-linux-7.1.md`
**Prerequisites:** Linux VFS `mount(2)` plumbing, `iomap`, `folio`, BIO flags

---

## The What

Linux 7.1 merged a fully rewritten optional in-kernel NTFS driver maintained by Namjae Jeon. Linus Torvalds labeled the merge the "NTFS resurrection." The driver:
- modernizes legacy `fs/ntfs/` with `iomap` and `folio`
- adds full write support the legacy driver lacked
- coexists with `ntfs3` without deprecating it

---

## Why a third driver

Path | Location | Read-write | Architecture | Notes
---|---|---|---|---
`ntfs-3g` | user-space FUSE | RW | classic FUSE request/reply | mature, conservative default
`ntfs3` | `fs/ntfs3/` | RW | direct `writepage`/`readpage` | Paragon contribution; post-merge maintenance concerns
New `ntfs` | `fs/ntfs/` | RW | iomap + folio | Namjae Jeon modernization | legacy codebase reuse

The "new `ntfs`" is a modernized rewrite from the legacy `fs/ntfs/` skeleton, not a scratch rewrite. It drops old buffer-head helpers in favor of `iomap_file_buffered_write()` and `iomap_file_direct_write()`.

---

## Mechanistic detail: mount and VFS binding

The driver registers with VFS using a normal `file_system_type`:

```c
static struct file_system_type ntfs_fs_type = {
    .owner   = THIS_MODULE,
    .name    = "ntfs",
    .mount   = ntfs_mount,
    .kill_sb = kill_block_super,
};
```

User space selects driver by `-t ntfs` vs `-t ntfs3`. On successful probe against `NTFS_SB_MAGIC`, `fill_super()` reads `$Boot`, builds the cluster-to-device-sector map, and constructs `inode->i_mapping->a_ops` backed by iomap folio ops. This matches the ext4/xfs model and means write clustering, flush/fua barriers, and readahead all follow the same kernel primitives other major filesystems use.

---

## iomap + folio integration

Buffered write path:
1. `iomap_file_buffered_write()` copies user data into newly dirtied folios tagged against `mapping`.
2. `iomap_write_begin()`/`iomap_write_end()` ensure cluster-aligned operations.
3. `writepages` writeback uses the standard `writeback_control` → BIO submission path. BIOs for metadata/journal use `REQ_SYNC`. Data hashes follow the same BIO chains.

Direct I/O path (`O_DIRECT`):
- Uses `iomap_dio_rw()` and issues BIOs directly, flips `REQ_FUA` for write-barrier preservation.

Large folio interaction:
- NTFS cluster size is locked at format time (commonly 4 KB).
- mTHP can hand a 64 KB folio to the driver even if only a 4 KB cluster belongs to the fs. The iomap folio-boundary logic handles sub-folio writes correctly but increases folio-dirty scan cost on writeback.

---

## NTFS journal ($LogFile) replay model

NTFS uses an internal journal called `$LogFile`. The new driver replays at mount by:

1. Reading `$Boot`, verifying `BPB.BytesPerSector`, `BPB.SectorsPerCluster`, `BPB.ReservedSectors`.
2. Mapping `$LogFile` runlist. The RSTR page declares dirty VCN ranges.
3. Walking the RCV pages and applying fixups to the MFT mirror.
4. Clearing the volume dirty bit on success.

This is structurally similar to XFS `xlog_do_recover()`, but unlike ext4 there is no separate `-o journal_path` abstraction. The journal is internal to the volume and invisible to user space.

Database implication: Flush ordering databases rely on is enforced by BIO flag choices in the driver. With the new driver, FUA writes appear on metadata paths, making crash recovery safer than `ntfs-3g` and more predictable than early `ntfs3` builds.

---

## Fourth subtlety: BIO flag semantics

The iomap+folio path tags data writes as `REQ_WRITE | REQ_SYNC` unless `O_DIRECT` was passed, in which case `REQ_FUA` may be added for durability.

`ntfs3`, by contrast, sets `REQ_META` on metadata BIOs more aggressively because its `writepage` implementation treats the MFT specially. This leads to:

- `iostat` and `blktrace` readings differ.
- pdflush/dirty-page ratios differ under the same workload.
- Database doublewrite / torn-page exposure differs if an application assumes metadata-ordered writes like XFS/ext4.

---

## Observability for verification

```c
// bpftrace: watch extent write size
tracepoint:iomap:iowrite
/args->rwbs == "W"/
{
    @bytes[args->dev] = sum(args->bytes);
    @count[args->dev] = count();
}
```

```bash
# lsblk / block device scheduler / queue flags
lsblk -t
cat /sys/block/nvme0n1/queue/rotational
cat /sys/block/nvme0n1/queue/nr_requests
```

Compare BIO merge counts between `-t ntfs` and `-t ntfs3` using blktrace to spot fragmentation differences on the same underlying storage controller.

---

## Security / containment

- Old pre-7.1 `fs/ntfs/` was practically dormant; the rewrite tidied up a long-decaying codebase and narrowed boundary exposure.
- `_NTFS_FS_` defaults to `m` (module), so attack surface is opt-in.
- Both `ntfs` and `ntfs3` drivers may co-reside. Kernel USB-storage + automount stacks should prefer `ntfs3` until the new driver has broader real-world exposure.

---

## Key Takeaways

1. Modernization, not revolution. Architecture tracks iomap + folio patterns from ext4/xfs.
2. Two in-kernel NTFS drivers is intentional: paragon-style vendor code (`ntfs3`) preserved alongside a cleaned community rewrite (`ntfs`).
3. For storage-engineers, driver selection is now a filesystem-tuning knob, with similar semantics risk as choosing between ext4 and ext4dev.
4. The "NTFS resurrection" is an under-the-radar storage change in 7.1 with more kernel-architecture significance than headline AI stories indicate.

---

## References

- Phoronix: "The NTFS Resurrection Has Occurred For Linux 7.1"
- LKML merge commit `cdd4dc3aebeab43a72ce0bc2b5bab6f0a80b97a5`
- Knightli: "Linux 7.0 and 7.1 NTFS Driver Changes Explained"
- `fs/ntfs/super.c`, `fs/ntfs/aops.c`, `include/linux/iomap.h`
