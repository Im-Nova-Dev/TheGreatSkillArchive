---
name: postgresql-buffer-manager-locking-evolution
category: university-cs/database-internals
title: PostgreSQL Buffer Manager Locking Evolution
description: "Teach the 30-year evolution of PostgreSQL buffer manager locking design: from monolithic global lock to partitioned atomics and lock-free lookups."
tags: [postgresql, database, buffer-manager, locking, concurrency, evolution]
difficulty: intermediate
---

# PostgreSQL Buffer Manager Locking Evolution

Use for: database internals teaching focused on buffer pool concurrency, lock evolution patterns, and how production databases solve the same problems kernel memory managers face.

## Trigger conditions

- Asked to explain PostgreSQL shared buffer concurrency evolution.
- Teaching database buffer management locking patterns.
- Comparing PostgreSQL lock decomposition to Linux kernel page cache locking.
- Needed concrete mechanistic example of 30-year lock evolution in a production DBMS.

## Mechanistic outline