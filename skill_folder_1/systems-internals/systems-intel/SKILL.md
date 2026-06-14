---
name: systems-intel
category: systems-internals
title: Systems Intelligence Collection & Feed Management
description: "Coordinates periodic collection of advanced OS internals, kernel internals, storage systems, database internals, networking hardware and protocol internals. Maintains source feed registry and intel archive."
tags: [systems, kernel, storage, database, networking, intel, cron]
difficulty: intermediate
---

# Systems Intelligence Collection

This umbrella skill coordinates the periodic cron job that collects one substantive systems topic per run and saves intel to the archive while enhancing teaching skills.

## Cron Job Specification

**Job ID**: Defined in `/home/nova/.hermes/cron/jobs.json` (name: "systems-intel-collector" or similar)

**Prompt Summary**:
1. Find one substantive systems topic (eBPF program, kernel regression, scheduler change, memory subsystem issue, filesystem design, database buffer manager trick, protocol implementation quirk, NIC offload behavior, storage controller optimization, concurrency primitive misuse, hard RT and timer tricks, io_uring, BPF, tracing, perf)
2. Save intel to `/home/nova/.hermes/intel/systems/`
3. Create or enhance a teaching skill under `university-cs/operating-systems`, `university-cs/database-internals`, or `systems-internals/`
4. Maintain source feed registry at `references/source-feed.md`

## Intel Archive Structure

```
/home/nova/.hermes/intel/systems/
├── YYYY-MM-DD_topic-slug.md          # Individual intel reports
└── LATEST.md                         # Symlink or index to most recent
```

Each intel report should contain:
- CVE/bug identifier if applicable
- Component/subsystem affected
- Root cause mechanistic analysis
- Corruption/exploitation chain
- Fix strategy and commit references
- Exposure requirements
- Verification commands
- Impact assessment

## Skill Enhancement Protocol

When a topic maps to an existing skill:
- **Patch the existing skill** with new mechanistic details, exercises, pitfalls, or verification steps
- Add the new intel file to the skill's Sources section
- Do NOT create duplicate narrow skills

When a topic has no existing skill:
- **Create a class-level skill** under `systems-internals/` (preferred) or `university-cs/operating-systems/` or `university-cs/database-internals/`
- Name must be generic/mechanistic (e.g., `io_uring-zcrx-freelist-race` not `CVE-2026-43121-fix`)
- Include: mechanistic outline, teaching exercises, common pitfalls, verification checklist, sources

## Reference Files

This skill uses a `references/source-feed.md` file (managed via skill_manage write_file) that tracks feeds worth monitoring.

## Related Skills

- `systems-internals/io_uring-zcrx-freelist-race`
- `systems-internals/io_uring-bpf-filter-internals`
- `systems-internals/linux-mglru-reclaim-loop-internals`
- `systems-internals/af-xdp-and-io_uring-zcrx-internals`
- `university-cs/operating-systems/ebpf-sched-ext-internals`
- `university-cs/operating-systems/eevdf-schedext-internals`
- `university-cs/database-internals/lmdb-buffer-rings-wal`
- `systems-internals/slub-sheaves-barns-internals`