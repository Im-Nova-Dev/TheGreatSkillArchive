---
name: systems-intel-ebpf-verifier-precision
description: "Teach eBPF verifier range tracking precision improvements for BPF_ADD/BPF_SUB (June 2025)"
category: systems-internals
tags: [eBPF, verifier, range-tracking, precision, BPF_ADD, BPF_SUB, formal-verification]
version: 1.0
---

# Teaching: eBPF Verifier Precision — BPF_ADD/BPF_SUB Range Tracking (June 2025)

## Learning Objectives
- Explain how eBPF verifier tracks register value ranges (min/max, signed/unsigned, tnum)
- Analyze why ADD/SUB precision matters for program acceptance and JIT optimization
- Describe the precision improvement for correlated operands and mixed signed/unsigned
- Understand formal verification context (Agni project)

## Prerequisites
- eBPF instruction set (ALU ops, register model)
- Verifier architecture: `kernel/bpf/verifier.c`, `struct bpf_reg_state`
- Range tracking: `smin/max`, `umin/max`, `var_off` (tnum)
- BPF semiotics: 64-bit modulo arithmetic, pointer arithmetic rules

## Core Concepts

### Verifier Range Tracking
Each register has `struct bpf_reg_state`:
```c
struct bpf_reg_state {
    enum bpf_reg_type type;      // SCALAR_VALUE, PTR_TO_MAP_VALUE, etc.
    s64 smin_value, smax_value;  // Signed range
    u64 umin_value, umax_value;  // Unsigned range
    struct tnum var_off;         // Bitwise precision (known/unknown bits)
};
```

### ADD/SUB Precision Challenge
```c
// dst = src + imm   or   dst = src1 + src2
// Must compute new min/max for dst from src operands
```

**Naive approach** (conservative):
```
dst.smin = src1.smin + src2.smin
dst.smax = src1.smax + src2.smax
```

**Problems with naive:**
- Doesn't track correlation (e.g., `r1 = r2 - r2` should yield exactly 0)
- Mixed signed/unsigned edge cases over-approximate
- Wrapping modulo 2^64 semantics not modeled precisely
- `var_off` (tnum) precision ignored for ALU ops

### June 2025 Improvement (Harishankar Vishwanathan)
**Files changed:**
- `kernel/bpf/verifier.c`: +76/-20 — core ADD/SUB precision logic
- `selftests/bpf/progs/verifier_bounds.c`: +85 — new testcases

**Key improvements:**
1. **Correlated operand handling**: `r1 = r2 - r2` → precise 0, not range
2. **Mixed signed/unsigned**: proper bounds when signedness differs
3. **Tnum integration**: leverage `var_off` known bits for tighter bounds
4. **Wrapping semantics**: correct modulo 2^64 range computation

**Selftests added**: Exercise precision for:
- ADD/SUB with constants
- ADD/SUB register-register
- Correlated operands
- Edge cases near signed/unsigned boundaries

### Why Precision Matters
| Impact | Before | After |
|--------|--------|-------|
| **False rejects** | Valid programs rejected | More programs accepted |
| **JIT optimization** | Conservative bounds | Tighter bounds → better codegen |
| **Formal verification** | Agni proof burden higher | Easier proofs (smaller state space) |
| **Developer friction** | Trial-and-error rewrites | Fewer iterations |

## Teaching Flow (75 min)

### 1. Verifier Range Tracking Refresher (15 min)
- `bpf_reg_state` fields: type, smin/max, umin/max, var_off
- How ranges propagate through ALU ops, loads, stores
- Why `var_off` (tnum) is more precise than min/max alone

### 2. ADD/SUB Naive vs Improved (20 min)
- Walk through examples: `r1 = r2 + 5`, `r1 = r2 + r2`, `r1 = r2 - r2`
- Show where naive over-approximates
- Demonstrate improved logic with tnum integration

### 3. Selftests Deep Dive (15 min)
- Read `verifier_bounds.c` new testcases
- Run `bpf verify` on test programs
- Observe acceptance vs rejection

### 4. Formal Verification Context (15 min)
- Agni project (Rutgers): formal verification of verifier
- Precision improvements → smaller abstract state → easier proofs
- Gap: verifier precision ≠ complete — each ALU op needs attention

### 5. Future Directions (10 min)
- Other ALU ops: MUL, DIV, shifts, bitwise
- Pointer arithmetic precision
- Helper call return value tracking

## References
- LKML: [PATCH v2 0/2] bpf, verifier: Improve precision of BPF_ADD/BPF_SUB (Jun 2025)
- v1: https://lore.kernel.org/bpf/20250610221356.2663491-1-harishankar.vishwanathan@xxxxxxxxx/
- Agni: https://people.cs.rutgers.edu/~sn349/agni/
- ACM: "Comparing Precision of Abstract Operators in the eBPF Verifier"

## Exercises
1. **Trace**: `bpftool prog dump xlated` on test program, observe register states
2. **Verify**: Run `bpftool bpf verifier` with `log_level=1` on edge cases
3. **Implement**: Write verifier range tracker for ADD in Python (simplified)
4. **Test**: Add new selftest case for `r1 = r2 * 0` (should yield exactly 0)
5. **Research**: Read Agni paper, identify next precision target