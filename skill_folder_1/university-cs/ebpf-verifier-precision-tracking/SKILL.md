# eBPF Verifier Precision Tracking

Use this skill when explaining how the Linux eBPF verifier tracks register and stack state, why precise tracking fails, and what kernel invariants force verification rejection. Target audience: systems programmers and advanced OS students.

## Trigger Conditions

- A question asks why an eBPF program is rejected despite “obviously safe” control flow.
- Need to explain bounded-range tracking, precision bits, and branch-merge behavior.
- Debugging verifier output (`bpf_verify_program`, `print_verifier_state`, verbose logs).
- Designing eBPF helpers or kfuncs with new types that require special verifier handling.

## 1. Core Concept: What the verifier tracks

For each instruction and call instruction:
- `reg_type` (PTR_TO_MAP, SCALAR_VALUE, PTR_TO_STACK, CONST_PTR_TO_MAP, etc.)
- `umin_value`/`umax_value` for unsigned bounds
- `smin_value`/`smax_value` for signed bounds
- `precision` bit indicating whether the register has a **precise value** (exact set) or only **range info**
- `frameno`, `slot`, and spill-fill bindings (for PTR_TO_STACK)

This is maintained in `struct bpf_reg_state` with parent pointers and per-state metadata like `parent`, `loop_nesting`, and `active`.

## 2. Precision vs Boundedness

Key distinction students miss:
- **Bounded** — verifier knows a scalar lies within an interval.
- **Precise** — verifier knows the exact value set at this program point.

A scalar after `r2 &= 0xFF` has bounded range [0, 255]; it is only precise if the original range was also [0, 255] (e.g., a known immediate). Arithmetic can downgrade precise to bounded.

## 3. Pointer Arithmetic and Type Promotion

`PTR_TO_STACK` and `PTR_TO_MAP` carry `off` (byte offset) and may carry `var_off` for run-time offset ranges.

`adjust_ptr_min_max_vals`:
- Adjusts offset by a known constant or range.
- Can introduce alignment requirements (e.g., `BPF_ALU64 | BPF_ADD` with a map pointer preserved alignment).
- If alignment can no longer be guaranteed, pointer type may be dropped in favor of SCALAR, destroying precision.

## 4. Branch Merging Lattice

When two paths reach the same instruction, verifier does an **intersection**:
- If both states agree exactly → merged state is identical.
- If one state is bounded [0, 100] and the other [200, 300], intersection is empty → path discarded as unreachable.
- If one state is precise and the other bounded, merged state is bounded.
- If types differ (PTR_TO_MAP vs SCALAR_VALUE for the same register), merged register falls back to SCALAR with bounds from the union.

This means a later branch becomes more likely to fail verification at the join because precision was already lost upstream.

## 5. Loop Back-Edge Behavior

- Back-edge triggers state checkpoint and iterative widening until fixed point.
- Loop unrolling bounds are inferred where possible from `decrement-to-zero` patterns.
- Historic classic failure: pointer increment by `sizeof` inside a loop over a map. If the verifier cannot prove that `off + sz*i <= map_max_entries * value_size`, it rejects with “value access beyond allowed range.”

## 6. Spin-Lock and Reference-Tracking Invariants

- Maps marked with `BPF_MAP_TYPE_RINGBUF`, `BPF_MAP_TYPE_ARRAY`, etc. have distinct ownership rules.
- Helper functions that consume references (e.g., `bpf_ringbuf_reserve_dynptr`) require verifier to carry reference-tracking metadata separately from the value-bound tracking.
- Failure to release a reference before program exit is a verifier rejection.

## 7. Teaching Exercises

1. Trace `print_verifier_state` output for a function that adds a pointer to a bounded offset derived from a map lookup. Identify where precision is lost and recover the exact reason by grepping for “precision lost.”

2. Write the simplest program that illustrates how branch A produces PTR_TO_MAP + bounded offset and branch B produces PTR_TO_STACK. Explain why the verifier merges to SCALAR_VALUE.

3. Prove that a loop bounded by a decrement-from-constant counter is accepted, but the same loop rewritten as `for (i = 0; i < n; ++i)` with `n` being the bound is not. Identify the verifier code path that falls back to symbolic iteration.

4. Design a small bug in a verifier helper handler that incorrectly drops alignment info on `PTR_TO_MAP` when `var_off` is present. Describe the rejection signature.

## 8. Related Intel

- `/home/nova/.hermes/intel/systems/2026-06-05_ebpf-verifier-precision-tracking.md`
- `/home/nova/.hermes/intel/systems/2026-06-05-cve-2026-23383-bpf-jit-alignment-tearing.md`
- `/home/nova/.hermes/skills/systems-intel/source-feed.md`

## 9. Kernel Source Pointers

- `kernel/bpf/verifier.c` — main verifier state machine
- `kernel/bpf/verifier.c:adjust_ptr_min_max_vals()`
- `kernel/bpf/verifier.c:find_equal_scalars()`
- `kernel/bpf/verifier.c:process_loops()`
- `include/linux/filter.h` / `include/linux/bpf.h` — type constants and verifier structures
- `tools/bpf/bpf_dbg.c` — inspection utilities

## Sources

- `Documentation/bpf/verifier.rst` in kernel source
- `Documentation/bpf/verifier/` subdirectory (if present)
