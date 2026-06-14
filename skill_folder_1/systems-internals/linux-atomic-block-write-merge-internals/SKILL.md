---
name: linux-atomic-block-write-merge-internals
description: Mechanistic teaching module on Linux atomic (untorn) block writes, BIO_ATOMIC / REQ_ATOMIC flag lifetimes through the block merge path, and how BIO merge logic can silently tear atomic guarantees between 6.13 and 6.15+. Targets OS students and database/kernel developers who need to reason below "how to use statx" into the merge/split code paths.
---

# Linux Atomic Block Write Merge & Flag-Loss Internals

Use this skill when teaching or auditing how database writes transit the Linux block layer with the atomic-write guarantee, and how merge/split code can lose the `BIO_ATOMIC` / `REQ_ATOMIC` flag.

## Prerequisites
- `struct bio`, `struct request`, `struct queue_limits`
- BIO merging states: FUSE/BACK/DOUBLE_ADD
- `bio_attempt_back_merge` state machine
- NVMe / SCSI atomic-write hardware semantics
- `statx(STATX_WRITE_ATOMIC)` userspace contract

---



## Module 1: The atomic-write contract

Database writes use the block layer to guarantee: either the entire N-KB extent is on disk or none of it is.

Hardware exposes:
```
/sys/block/nvme0n1/queue/atomic_write_unit_min
/sys/block/nvme0n1/queue/atomic_write_unit_max
```

Kernel exposes to userspace:
- `statx(STATX_WRITE_ATOMIC)` returns unit sizes for the file's backing store.

Application contract: submit `O_DIRECT` writes aligned to `atomic_write_unit_max`. If the app violates alignment, filesystem should split and preserve atomicity.

---



## Module 2: Flag propagation anatomy

Flags live in parallel state:
- `bio->bi_opf` bits: `REQ_ATOMIC`, `REQ_FUA`, `REQ_PREFLUSH`, `REQ_NOUNMAP`
- `rq->cmd_flags` mirrors them but is the *driver-visible* contract.

Propagation requirements:
1. `blk_mq_submit_bio()` must set `REQ_ATOMIC` on the request when the bio has `BIO_ATOMIC`.
2. `bio_attempt_back_merge()` / `bio_attempt_front_merge()`:
   - If either side has `BIO_ATOMIC`, the result MUST have it.
   - If the resulting sector range exceeds `atomic_write_unit_max`, merge MUST be refused.
3. Chained bios via `bio_chain()` inherit or clear flags; the *tail* bio determines `REQ_PREFLUSH` but not `REQ_ATOMIC` (atomicity is global for the whole group).

---



## Module 3: Known regression vectors

### Vector A: Merge after split loses `REQ_ATOMIC`

```
App submit: 64 KB write  (BIO_ATOMIC)
FS split:    2 x 32 KB    (each with BIO_ATOMIC)
rq1 created: REQ_ATOMIC on rq1
rq2 merge to rq1: bio_attempt_back_merge succeeds
rq final:    cmd_flags missing REQ_ATOMIC
```

Root cause: merge code checked `bio->bi_opf` but the update path in some inline-crypto fallback clears `REQ_FUA` and accidentally does not preserve `REQ_ATOMIC`.

Mitigation: add `REQ_ATOMIC` preservation in the clear mask:
```c
new_opf = (bio->bi_opf & ~(REQ_FUA | REQ_PREFLUSH | REQ_NOUNMAP)) | keep_atomic;
```

### Vector B: Driver grabs `rq->cmd_flags` without ACM

After merge, `rq->cmd_flags` is updated without `smp_wmb()` in the fast path.
- `blk_mq_start_request()` sees stale flag if the reader is on another core than the merger.
- NVMe command generation samples `req->cmd_flags` -> might skip atomic-write variant command.
- Result: device writes full 64 KB but with normal non-atomic variant; torn-write risk.

Mitigation: `blk-mq` pass-through via `WRITE_ONCE` / `READ_ONCE` in merge.

### Vector C: Split-after-merge destroys grouping

If the merged request now spans > `atomic_write_unit_max` but `blk_mq_split_and_merge()` does not see `REQ_ATOMIC`, it will split without preserving `atomic_write_unit_min` alignment and the split halves carry no flag → no torn-write error on partial failure.

---



## Module 4: Filesystem responsibilities

- `ext4_iomap_begin()` / `xfs_iomap_alloc()` must align extents to the device's `atomic_write_unit_min`.
- ext4 currently cannot expose block sizes > page size on x86 → atomic regions <= 4 KB on 4 KB page-size systems, even if NVMe supports 128 KB atomic writes.
- XFS can exceed page size because it tracks its own block size.

Filesystem atomic-write mount-time controls:
```
mount -o atomic_write=strict  # refuse unaligned atomic writes
statx file                   # verify: stx_atomic_write_unit_min == expected
```

---



## Module 5: Database side impact

Databases eliminate double-write:
- BEFORE: log -> undo -> full-write -> complete -> discard old
- AFTER:  log -> direct-atomic-write -> complete

Breaking the kernel assumption:
- Torn extent on power loss reads as two pages of old, two pages of new.
- Journal replay is against corrupted extent; WAL does not detect torn physical writes.
- Corruption may only manifest after recovery replay continues.

Debugging indications:
- `blktrace -d /dev/nvme0n1` shows `A` flag absent on write paths.
- `bpftrace` via `block:block_rq_issue` shows sector spans > max without `A`.

---



## Module 6: Observability and hardening

Kernel-side assertions to add (or check upstream):
```c
WARN_ON_ONCE((bio->bi_opf & REQ_ATOMIC) && !(rq->cmd_flags & REQ_ATOMIC));
```

Userspace checks:
```python
# validate file backing supports atomic writes
import statx
flags = statx.statx(path).write_atomic
if not flags.unit_min or not flags.unit_max:
    sys.exit("atomic write not supported")
```

Runtime bpftrace recipe:
```c
tracepoint:block:block_rq_issue
/args->rwbs !~ "A"/ {
  @missed[args->dev] = count();
}
```
`A` present in `rwbs` means the kernel thinks the request is atomic.

---



## Exercises / Research Prompts

1. Trace `blk_mq_attempt_bio_merge()` for atomic BIO and identify every branch that does or does not propagate `REQ_ATOMIC`.
2. Examine ext4` -> iomap split path: why does 6.15 split a 64 KB atomic write into 2x32 KB on a namespace with `atomic_write_unit_max=128K`?
3. Write a bpftrace program that flags any `block_rq_issue` with `A` missing but sector count > `atomic_write_unit_min`.
4. Compare XFS `dax` + atomic writes vs ext4: what prevents a filesystem from advertizing `atomic_write_unit_max` larger than page size on 4 KB page-size systems?

## Related Intel
Stored in `/home/nova/.hermes/intel/systems/2026-06-05-atomic-blk-merge-flag-loss.md`.
