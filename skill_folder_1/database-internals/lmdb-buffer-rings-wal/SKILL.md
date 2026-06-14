---
name: lmdb-buffer-rings-wal
description: >
  Teach LMDB (Lightning Memory-Mapped Database) write-ahead log, MVCC buffer
  state machine, page-level concurrency, and the "read your own writes"
  semantics at a mechanistic level. Covers how MDB_TXN writes accumulate
  in the dirty page ring, how the write lock + page / spill + sync sequence
  advances the WAL tail, and why LMDB's single-writer rule is enforced by
  struct design rather than by advisory mutex. Targets storage systems and
  database internals engineers.
trigger:
  - LMDB WAL mechanics
  - LMDB MVCC
  - MDB_TXN internal representation
  - LMDB read-your-own-writes
  - single-writer design rationale
  - LMDB buffer rings
  - Why LMDB is copy-on-write
  - LMDB crash recovery mechanics
  - MDB_env page flush
---

# LMDB WAL, MVCC and Buffer Rings
## Scope
Mechanistic deep-dive into LMDB's internal page management and MVCC. Not a how-to-use MDB_env — this is a systems-level explanation of dirty page write-paths, memory mapping rules, and the invariants that make LMDB ACID without a traditional write-ahead log in user space.

## Prerequisites
- Virtual memory basics: `mmap`, page faults, MADV_DONTNEED / MADV_FREE.
- MVCC theory: snapshot isolation, read/write set, readers-writer concurrency.
- C struct layout familiarity (field ordering affects atomic reads).

---

## Lesson 1: What LMDB calls WAL vs traditional WAL
LMDB can be configured with MDB_WRITEMAP and MDB_NOSUBDIR. In write-enabled modes LMDB marks the new pages dirty in the memory map, then writes changes live into the map. It does not maintain a separate system of write-ahead-log segments like Postgres WAL or SQLite WAL in the traditional sense.

What LMDB actually does:
1. Reader keeps a stable snapshot of the last committed data pages it accessed.
2. Writer allocates new B+ tree pages from the free DB in the same memory map; reuse while other readers are using them is impossible unless using MDB_NOFREE.
3. Dirty state lives in `mdb_txn->tw` (write list) and `mdb_txn->loose_pages`.

The write recovery path is different from WAL: since pages are already written at the UTC logical point of commit (for the slow path, unless MDB_NOSYNC), the "log" is the sequence of page allocation and reclamation in the free DB itself.

## Lesson 2: The buffer ring — mdb_txn dirty-page state machine
`mdb_txn` maintains several lists for uncommitted changes:

- `mdb_txn->dirty_list` — doubly-linked list of `MDB_page` *pointers* (not copies). Contains root + dirty subtrees.
- `mdb_txn->loose_pages` — singly-linked list of deallocated pages during this txn.
- `mdb_txn->tw` — transaction write-list used during commit travel.

Buffer-level invariant:
For every leaf page A marked dirty in dirty_list, if A is a split result, the parent pages leading to A must also appear in dirty_list. The commit walker enforces this by examining `mdb_page_get_parent()` through the meta page version.

When MDB_NOSYNC is off, the "sync" is `msync(env->me_map, ...)` on the entire database region, which guarantees the dirty pages reach disk at commit time (slow but safe).

## Lesson 3: Write lock and spilling
LMDB requires exclusive write access. The lock is implemented as a bitfield in `mdb_env->me_txck` and interacted with via atomic compare-and-swap on `MDB_TXN_STARTED` flag — not via pthread_mutex.

The write lock semantic key bits:
- `MDB_TXN_WRITEMAP` — whether writes go directly into the mmap.
- `MDB_TXN_FINISHED` — cleared during rollback to indicate the txn is recyclable.

Only MDB_env writers check the `txn->mt_txnid` counter but not a global mutex on the dirty list: the lock is effectively a sequence counter check because child txns inherit a snapshot id when they are created via `mdb_txn_begin()`.

Mechanism: when `mdb_txn_begin()` is called with MDB_RDONLY, it picks the last committed meta page snapshot. When called with write mode, it tries to claim the write slot by swapping the writer flag.

## Lesson 4: B-tree split nuances under writes
A single insert into a full leaf page triggers an 8KB page split. LMDB chooses the smallest page size configured (usually the system page size) — the default database page size equals the OS page size because everything is mmap'd.

During a split:
1. Parent pointer is updated to point to the new page.
2. The new page becomes dirty and is prepended to dirty_list.
3. If the parent was itself full, it recursively splits upward until it reaches the root.

Observation: during this recursive walk, the txn is not holding any kernel lock besides the mmap page table entries. No data is copied — the existing pages are mutated in-place and new pages are taken from the free DB.

Why this is safe to do in-place while readers hold references:
Because the readers are snapshot-isolated using the meta page version number. Any txn that saw the old root pointer does not see the split because it dereferences old page pointers captured at txn start.

## Lesson 5: The free list / page reclamation ring
LMDB pages are reused. The free DB is just another B+ tree in the same memory map. Transactions append to the free DB only at commit time; until then, freed pages live on `mdb_txn->loose_pages`.

At commit, the writer walks dirty_list, heavy-checks parent pointers, then:
1. Fills the new dirty page(s) with pending changes.
2. Appends freed pages to free DB.
3. If MDB_NOSYNC off: `msync()`/`mman` metadata flush.

Why rings matter: LMDB uses a per-env "cache" ring for page reuse — it keeps a small ring of recently-freed page numbers to reduce tree walking for the freelist. This explains why sequential writer, sequential reader performance stays fast: the free list has good locality of reference for reused pages.

## Lesson 6: Recovery and the meta page
LMDB has two meta pages in the file, alternating:

```c
struct MDB_meta {
    uint32_t mm_magic;
    uint32_t mm_version;
    char    mm_psize;      /* page size */
    ...
    uint64_t mm_geo[3];
    uint64_t mm_last_pg;   /* last committed page number */
    ...
    uint64_t mm_magic_and_version ^ 0xDEADBEEF; /* checksum */
};
```

On `mdb_env_open()` with MDB_RDONLY not set:
1. Reads two meta pages, selects the one with higher txn id.
2. Verifies checksum via XOR magic.
3. If checksum mismatches and MDB_RDONLY not set, the env tries to reconstruct from the alternate meta page.

Because writes go live, a crash in the middle of commit may leave dirtied pages but an incomplete root pointer update; recovery reads the last valid meta and discards the odd page allocation by walking dirty_list.

---

## Lesson 7: When single-writer rule breaks
LMDB does not support multiple concurrent writers. The enforcement is *structural*:
- There is one write slot on `mdb_txn_start()`. Multiple write txns created concurrently result in one succeeding and the others receiving MDB_MAP_FULL or MDB_BAD_TXN.
- Two writers do not fight over a mutex; they rely on a bit CAS in `txn->mt_flags` via `atomic_cmpxchg`.

This is why MDB_NOSUBDIR multi-process scenarios need OS-level interlock (fcntl on the lock file) to avoid dead writers. Processes sharing the same env must coordinate lifecycle externally.

---

## Lesson 8: Copy-on-write Snafu
LMDB advertises that the data file grows by one page at a time. When pages are freed by a writer, they go to the free list but the file does *not* shrink. The mmap region also does not shrink until mdb_env_sync() / mdb_env_close() resets the backing file size. 

If you run long-lived writers on a dataset with heavy churn, the file will contain many orphan free pages. Tools: `mdb_dump -f /dev/null` creates a fresh copy; `mdb_env_copy2()` produces a compacted copy.

---

## Lesson 9: The "read your own writes" contract
Inside a single write transaction, LMDB guarantees read-your-own-writes via the dirty_list:
- Any page the txn has dirtied is immediately visible to subsequent reads within the same txn because `mdb_page_search()` first consults dirty_list (`mdb_page_search_mdb()` route).
- Other readers do not see dirty pages because they have pinned older meta page versions.

However this only applies to writes that have not been spilled to disk via the dirty_list flush ordering constraints.

Edge case: If you create a cursor, write, then read the same key in the same transaction, the read succeeds from dirty_list only if the modified leaf page is still dirty and has not been moved to the free list within the same txn.


