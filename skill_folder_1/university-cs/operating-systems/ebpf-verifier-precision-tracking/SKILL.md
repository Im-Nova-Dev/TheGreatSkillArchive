---
title: eBPF Verifier Precision Tracking
description: >
  Mechanistic internals of the Linux eBPF verifier — precision tracking, register states,
  backtracking, and what causes verifier rejections beyond simple safety checks.
triggers:
  - ebpf verifier precision
  - ebpf register tracking
  - ebpf rejection causes
  - bpf verifier mechanics
  - bpf precision
dependencies: []
---

# eBPF Verifier Precision Tracking

## Sources of truth
- `net/core/filter.c` and related `kernel/bpf/` verifier code
- `tools/testing/selftests/bpf/` (`progs/` and `vmtest.c`)
- Linux kernel documentation: `Documentation/networking/filter.rst`

## What the verifier decides
The verifier checks every reachable instruction state tuple `(insn_idx, register state snapshot)`.
If a snapshot repeats, that path is pruned. If no valid path reaches `BPF_EXIT`, the program is rejected.

## Register state components
- `type` — NOT_INIT, SCALAR_VALUE, PTR_TO_CTX, PTR_TO_MAP, etc.
- `id` — pointer provenance chain identifier
- `off` — fixed byte offset from base pointer
- `imm` — immediate value (may be cleared to zero to reduce precision)
- `min_value`, `max_value` — scalar bounds
- `min_value_defined`, `max_value_defined` — whether bounds are known
- `prec` — precision marker; used for backtracking and for preventing constant-propagation kills

## Precision backtracking
When a helper or instruction may consume pointer metadata, the verifier marks that
register as needing precision. If a register loses precision, the verifier
revisits earlier instruction states (backtracking) and marks the register as
unknown again.

Relevant helpers that often trigger precision requirements:
- bpf_probe_read, bpf_probe_read_user
- bpf_skb_load_bytes
- bpf_map_lookup_elem
- bpf_trace_printk
- bpf_get_current_task

Common pattern: speculative bounds computations on pointer-derived values can widen
the register type or clear `id`, forcing `mark_reg_unknown()` and reducing
verifier confidence on dependent branches.

## Bounded loops impact
Verifier 5.x loop support adds a convergence check: loop metadata must stabilize
across iterations. If a loop depends on imprecise scalar bounds, the verifier may
reject it with "not in old_insn[] after loop" or similar convergence failure.

## Teaching tools
1. Write small single-loop eBPF programs, then inspect `insn` state log with
   `bpfc -d` or kernel printk-style debug prints via `bpf_printk`.
2. Run `vmtest.sh` from `tools/testing/selftests/bpf/` to compile and verify.
3. Show how `imm` clearing reduces precision; demonstrate spurious rejections and
   then how padding struct fields with `__attribute__((aligned(8)))` removes them.

## Further reading
- `Documentation/admin-guide/bpf/` verifier design notes
- `tools/testing/selftests/bpf/progs/verifier_*` test files
