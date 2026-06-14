---
name: ebpf-verifier-precision-tracking
description: >
  Teach Linux eBPF verifier internals at the mechanistic level: precision tracking,
  branch pruning algorithm, tnum-based scalar bounds, register state merging,
  historical unsoundness causes, FOSDEM 2025 verifier evaluation across kernels
  5.0–6.8, and the compiler-verifier gap exemplified by production Cilium workarounds.
  Aims below "how to use" to explain why the verifier accepts or rejects code and how
  unsoundness arises.
trigger: >
  eBPF verifier internals, branch pruning, precision tracking, tnum, verifier soundness,
  CVE/syzbot BPF issues, compiler-verifier gap, verifier performance, static analysis
  of safety properties, unsafe accepted program, eBPF static analysis failure.
---

# eBPF Verifier Precision Tracking & Branch Pruning Internals

## Scope
Mechanistic how-it-works of the Linux kernel eBPF verifier's precision tracking
and branch pruning. Focus on the "language-verifier gap": how high-level C code
compiled by LLVM to eBPF bytecode is independently checked by `verifier.c`, why
that check is unsound in practice, and how the symbolic execution engine can
mark unsafe paths as safe.

## Prerequisites
- eBPF program loading model, `struct bpf_insn`, `struct bpf_prog_info`.
- Basic static analysis: symbolic execution, control flow graph, merge/join semantics.
- Linux kernel `tnum` representation and pointer register types.
- Familiarity with LLVM eBPF backend assumptions.

---

## Lesson 1: What the verifier actually computes

The verifier symbolically executes each instruction over all possible execution
states. A state is a tuple per-register and per-stack-slot:

```
struct bpf_reg_state {
    enum bpf_reg_type type;
    struct tnum        var_off;
    u64                smin_value, smax_value;
    u64                umin_value, umax_value;
    u64                off;
    int                ref_obj_id;
}
```

`struct tnum` encodes known/unknown bits:
- `value`: bits known to be 1.
- `mask`: 1 = unknown bit (kernel docs use "top 56 bits known 0, low 8 unknown"
  as canonical example of `(0x0; 0xff)` for a loaded byte).

Precision is captured in `mask`: a perfectly precise register has `mask == 0`.
A fully unknown register has `mask == ~0ULL`.

### Bounds inference from tnum
- `umin_value / umax_value`: unsigned min/max derivable from `tnum` plus extra
  constraints from comparisons.
- `smin_value / smax_value`: same, signed.
- `off`: fixed offset added to pointer bases; updated by immediate-adds.

---

## Lesson 2: Branch pruning and the join problem

### Branch pruning
Before 5.3, every conditional branch spawned a fresh state; exponential explosion.
Since 5.3, bounded loops introduced a fixpoint iteration where the verifier
deduplicates equivalent states via a hash.

### Precision loss at joins
When two states from the true/false branches merge, regstate merges are
conservative in some dimensions and aggressive in others:
- `type` must be identical across both states or merge rejects the instruction
  transition.
- `tnum` merges with bitwise-OR: `merged.value = a.value | b.value`,
  `merged.mask = a.mask | b.mask | (a.value ^ b.value)`. This is the fundamental
  widening operation. If left branch knows a register is `0xf0` and right branch
  knows `0x0f`, joined-register becomes `(0xff;0xff)` — completely unknown.
- `umin/umax` and `smin/smax` take the intersection of valid ranges across both
  states, but intersection with wide tnum can degenerate to `[0, U64_MAX]`.

### Why tracking over-approximates unsoundly
The verifier assumes "if all paths to an access are checked here, then the access
is safe." But if precision is lost before the check (e.g. a join from two states
with disjoint but individually safe ranges produces an all-unknown range), the
verifier may:
- **Accept** programs where the unsafe path was pruned away from the joined view
  (i.e., the verifier thinks a path is unreachable after pruning).
- **Reject** safe programs (false positive), which is the dominant developer pain.

This is the root cause documented as SA-2025-092 branch pruning issue.

---

## Lesson 3: Real-world unsoundness examples (2023–2025)

### 2023: Signed/unsigned comparison precision loss
Google syzbot reported `bpf_tree` class bugs where signed compare followed by
unsigned bounds check still accepted unsafe loads. The tenor was: after
`BPF_JSGT` path, verifier preserved wrong signedness domain and later allowed
out-of-bounds access that should have been rejected.

### 2024: Pointer-spill-to-stack aliasing
Researchers (USENIX Security 24, Jin et al.; OSDI 24, Sun et al.) showed that
when a pointer register `R6` is spilled to the stack and reloaded as a scalar
`R4`, type aliasing in the later merge incorrectly preserved packet pointer
semantics, allowing packet off-by-one loads.

### 2025: FOSDEM verifier evaluation (Julia Lawall / Maxime Derri)
Evaluation of kernels 5.0 → 6.8 found:
- Conditional-jump verification time decreased after 5.3 bounded loops (due to
  pruning+fixpoint).
- However, consumed memory was stable and there existed programs where
  verification time regressed due to excessive pruning artifacts.
- Comparative study with PREVAIL (sound user-space verifier) showed eBPF's
  pruning causes it to create more paths before pruning; PREVAIL's join+fixpoint
  handled path explosions differently.

### SA-2025-092
Advisory summary: "incorrect verifier pruning in BPF in some versions of Linux
Kernel may lead to unsafe code paths being incorrectly marked as safe."

---

## Lesson 4: The language-verifier gap in the wild

### Compiler divergence
The arXiv "Rax" paper (2025) tabulated 72 production commits in Cilium, Aya,
Katran that were clearly working around verifier limitations:

| Workaround | Count |
|---|---|
| Split big programs into many small ones (to dodge complexity limits) | 27 |
| LLVM hinting to produce verifier-friendly bytecode | 22 |
| Refactoring data flow to avoid precision loss | 15 |
| Working around verifier bugs across kernels | 9 |
| Reimplementing library functions (`memset`/`memcpy`) for verification | 1 |

### Cilium example: 32-bit move misclassifies pointer
```c
// Original
1; return (void*)(unsigned long)ctx->data;
22: r9 = *(u32 *)(r7 + 76)   // LLVM compressed 64-bit -> 32-bit move
...
87: r2 = *(u8*)(r6+22)       // rejected: r6 is inv/scalar, not packet
```

Workaround: inline assembly to prevent LLVM from truncating the pointer:
```c
static __always_inline void* ctx_data(const struct __sk_buff *ctx){
    void *ptr;
    asm volatile("%0 = *(u32 *)(%1 + %2)"
                 : "=r"(ptr) : "r"(ctx),
                   "i"(offsetof(struct __sk_buff, data)));
    return ptr;
}
```

### Cilium example: goto-style control flow confuses precision
A `goto` combining policy-check paths caused the verifier to misclassify a
pointer as scalar due to join-induced precision loss. Refactored to inlined
function call without `goto`.

### Takeaway
Developers write C with a "verifier contract" that is an informal, undocumented
subset of C, targeting the verifier's current puns and precision limits. When
LLVM changes generation behavior, safe code can become rejected or incorrectly
accepted.

---

## Lesson 5: Mechanistic flow of a pruning-related reject/accept

### Rejection via precision loss at branch join
```
state_A: r4 = pkt(id=0,off=0,r=64)    [readable, bounded 0..64]
state_B: r4 = pkt(id=0,off=32,r=64)   [readable, bounded 32..96]
join(r4) = pkt(id=0,off=0,r=96) if umax preserves original L3 linear offset
         => reject next access at offset 96 because it assumed max 96 but
            no guarantee that actual runtime offset is <=96 in all states?
```
More typical: after two paths the type is preserved but `off` is widened; the
verifier's `reg_bounds_sync` is called with contradictory info and rejects.

### Acceptance via pruning error
If branch pruning considers one of the two preceding states unreachable due to
a precision bug in `is_state_visited()` comparison (an older bug class), a path
that would fail a bounds check is dropped from further exploration, and an
access outside valid bounds is accepted because only the "safe" branch remains
live.

---

## Lesson 6: Key functions and data structures upstream

- `kernel/bpf/verifier.c`:
  - `__check_mem_access()`: bounds-checking entrypoint.
  - `maybe_widen_reg()`: where scalar bounds can be widened after symbolic ops.
  - `reg_bounds_sync()`: reconcile signed/unsigned bounds from `tnum`.
  - `do_check()`: main symbolic execution loop.
  - `is_state_visited()`: pruning / loop detection.

- `include/linux/bpf_verifier.h`:
  - `struct bpf_reg_state`.
  - `struct tnum`.
  - `enum bpf_reg_type` (1-to-1 mapping with allowed types).
  - `MAX_BPF_STACK`, `BPF_MAX_VAR_SIZ` (limits that drove the workarounds).

- `kernel/bpf/btf.c`: BTF-based type propagation that reduces type loss.

---

## Lesson 7: Formal verification context

- PREVAIL (PLDI 2019): SQL-style verification conditions, sound, user-space.
  - Slower than in-kernel eBPF verifier but does not have the language-verifier
    gap because it operates on the same IR.
- Agni (Rutgers): automatic verification of the verifier's analysis algorithms.
- Rax: removes eBPF verifier entirely, replacing with Rust borrow checker +
  lightweight taint analysis. Demonstrates the gap cannot be patched from within
  the existing verifier architecture.

---

## Exercises / thought problems

1. Given two byte loads: `r4 = *(u8 *)(r6 + 0)` and `r4 = *(u8 *)(r6 + 64)` in
   separate branches that share `r6 = pkt(id=0,off=0,r=128)`, trace the joined
   state for `r4`. Compute `tnum`, `umin`, `umax`, `smin`, `smax` after the
   merge. Why might the verifier reject a following `*(u8 *)(r4 + x)` load?

2. Inspect `kernel/bpf/verifier.c` in Linux 5.15 and 6.8. Find where
   `reg_bounds_sync()` changed and hypothesize why that touched precision on
   `BPF_JSGT` / `BPF_JSGE` comparisons.

3. Reproduce the Cilium 32-bit move issue manually: write a small eBPF C
   program that copies `ctx->data` into a `u32` local first, then does a packet
   access. Compile with Clang-8 vs Clang-14 and observe the verifier log (use
   `bpftool prog dump xlated`). What changes in the bytecode cause the verifier
   to see or lose the pointer type?

4. Simulate the pruning error described in SA-2025-092. Suppose `is_state_visited()`
   compares states using an `<` operator that loses `tnum.mask` information.
   Give a concrete two-branch example where the unsafe state is spuriously
   considered "already visited" and pruned.

5. Why does PREVAIL avoid the path-explosion problem that motivates eBPF's
   pruning? If eBPF switched to a PREVAIL-style join + fixpoint model, what
   would break in the production verifier's performance model?

6. Explain how `BPF_ALU64 | BPF_MOV` with a 32-bit sub-register destination
   (`w6 = w9`) interacts with `maybe_widen_reg`. Under what conditions does the
   verifier zero-extend to 64-bit and when does it not?

7. Design a minimal regression test for `reg_bounds_sync` that would catch a
   signed/unsigned precision loss bug. Which BPF instruction sequence and which
   post-merge bounds check should fail if precision is lost?
