---
name: bpf-jit-alignment-and-atomic-tearing
description: >
  Systems-internals teaching module on arm64 eBPF JIT buffer alignment and
  atomic tearing (CVE-2026-23383). Covers `bpf_jit_binary_pack_alloc()`,
  `struct bpf_plt`, `bpf_arch_text_poke()`, `WRITE_ONCE` vs LDR atomicity
  guarantees on arm64, how 4-byte-aligned JIT blobs cause misaligned u64
  fields, the tearing race, UBSAN interaction, and the 8-byte alignment fix.
  Mechanistic how-it-works, not how-to-use.
trigger: >
  eBPF JIT internals, arm64 JIT buffer alignment, atomic tearing, bpf_plt,
  CVE-2026-23383, WRITE_ONCE misaligned u64, JIT text poking, LDR atomicity
  guarantees, kernel allocator alignment mismatch, BPF PLT internals.
---

# Arm64 eBPF JIT Buffer Alignment & Atomic Tearing (CVE-2026-23383)

Mechanistic internals of how a 4-byte alignment mismatch in the arm64 eBPF JIT
text allocator allowed a torn-read race against `WRITE_ONCE()` updates of the
PLT `target` field, and how the fix repairs the alignment contract.

---

## Lesson 1: The arm64 eBPF JIT and `bpf_plt`

The eBPF JIT turns eBPF bytecode into native instructions. On arm64 it emits
a variable-length instruction stream into a contiguous `bpf_jit_binary`.

`struct bpf_plt` is embedded inside that stream:

```c
struct bpf_plt {
    /* real jump target, updated by bpf_arch_text_poke() at runtime */
    u64 target;
    /* trampoline: ADRP + LDR literal-style stub */
    /* ... */
};
```

`build_plt()` in `arch/arm64/net/bpf_jit_comp.c` writes this struct inline.
The emitted machine code uses `ldr xN, [pc, #offset]` to load `target` and
branch through it.

---

## Lesson 2: Allocation alignment vs struct member alignment

### `bpf_jit_binary_pack_alloc()` contract

```c
static struct bpf_jit_binary *
bpf_jit_binary_pack_alloc(unsigned int size)
{
    /* pre-fix: */
    buf = kvzalloc(size + 4, GFP_KERNEL);
    buf = PTR_ALIGN(buf, 4);
    /* ... */
}
```

The `+4` and `PTR_ALIGN(..., 4)` guarantee the *head* of the buffer ends in
a 4-byte-aligned address. This was enough for the allocator's typical use
case, but `bpf_plt.target` needs 8-byte alignment.

### Why the `build_plt()` padding wasn't enough

`build_plt()` started with an 8-byte-aligned offset relative to the struct
start, then computed an absolute address using `ALIGN(start + pad, 4)`. When
the buffer *base address* ended in 0x4 or 0xc, the absolute address of
`target` ended in 0x4 or 0xc — 8-byte-unaligned from the page's perspective.

```c
/* conceptual sketch */
u64 target_addr = (u64)buf + plt_start_off + plt_pad;
/* if buf is 0x...4, target_addr ends in 0x...c on arm64 */
```

This is an **allocator/type contract violation**: the allocator's alignment
promise does not reach the field's alignment requirement.

---

## Lesson 3: The tearing race

### Participants

| Actor | Action |
|---|---|
| `bpf_arch_text_poke()` | `WRITE_ONCE(plt->target, new_dest)` — 8-byte store |
| JIT-compiled BPF code running on another CPU (or same CPU across a context switch) | `ldr x0, [x0, #offset]` — 64-bit load |

On arm64, the architecture manual states that 64-bit LDR/STR is only
guaranteed to be **single-copy atomic** when the address is 8-byte aligned.
Misaligned 64-bit LDR/STR can be implemented as two 32-bit accesses.

### Failure timeline

1. CPU-A executes `bpf_arch_text_poke()` and issues an 8-byte store to
   `plt->target`. Memory system stages the write.
2. CPU-B fetches `ldr x1, [x28, #off]` from the JIT text (the target load).
3. Because the address is misaligned, the bus splits the transaction.
   CPU-B's load returns the upper 32 bits from the *new* write and the lower
   32 bits from the *old* value — or vice versa — a **torn read**.
4. Result: the BPF program jumps to `0xAAAA5555AAAA` or similar garbage.
   Outcomes: silent misbehavior, kernel oops, privilege escalation if attacker
   controls the write side.

The same scenario with `bpf_arch_text_poke()` running under stop_machine()
would serialize against execution, but `bpf_arch_text_poke()` is specifically
allowed to operate *without* the machine-wide stop if cross-modifying code is
safe — which requires the read side to be atomic.

---

## Lesson 4: UBSAN interaction

UBSAN reports misaligned-access warnings on kernel pointers dereferenced as
`u64 *` when the address is not 8-byte aligned. These warnings do not
immediately crash; they mark the program path UB. In production kernels
built without `CONFIG_UBSAN`, this goes silent.

Critically, UBSAN did not catch this originally because the JIT text pointer
itself was not a `u64 *` in the source; it was computed from byte offsets
inside an inline assembly block. UBSAN cannot track alignment through
assembly-emitted metadata.

---

## Lesson 5: The fix

`bpf_jit_binary_pack_alloc()` was changed to request 8-byte alignment:

```c
static struct bpf_jit_binary *
bpf_jit_binary_pack_alloc(unsigned int size)
{
    unsigned int size1 = size + 8;          /* extra 8 for room to align */
    u8 *buf, *aligned;

    buf = kvzalloc(size1, GFP_KERNEL);
    aligned = PTR_ALIGN(buf, 8);            /* force 8-byte boundary */
    /* ... store header ... */
}
```

- The extra 8-byte headroom means `PTR_ALIGN(buf, 8)` never writes past the
  allocation's end.
- `build_plt()`'s padding math then produces an 8-byte-aligned `target`
  regardless of `buf`'s original position.
- After the fix, `WRITE_ONCE(plt->target, new_dest)` is single-copy atomic
  on arm64 because the address is 8-byte aligned.

---

## Lesson 6: Generalized pattern recognition

This bug is one instance of a class that recurs across the kernel:

**Class: JIT/text-allocator alignment mismatch with embedded atomic fields.**

Other occurrences to watch:

| Subsystem | Field | Fix pattern |
|---|---|---|
| BPF JIT PLT (this CVE) | `u64 target` in inline JIT text | 8-byte align buffer base |
| `module_alloc()` / insn patching | `u32` patched instruction | THUNK_SIZE fence (already used) |
| `text_poke()` caching | `struct text_poke_loc` qspinlock | `__cacheline_aligned` |
| `alternatives` patching | `s32` displacement | alignment not needed (no u64 atomics) |

Rule of thumb: any time a JIT, patch, or text buffer embeds a field updated
with `WRITE_ONCE` / `cmpxchg` and read by executing code, verify `alignof`
of that field against the allocator's `align` argument.

---

## Lesson 7: Mapping to the broader atomicity framework

On arm64 and RISC-V, the architecture manual defines which N-byte aligned
regions support N-byte atomics. The Linux kernel uses `arch_atomic_*` ops
that map onto these regions, but the guarantee only holds when the compiler
and allocator cooperate to emit 8-byte-aligned addresses for 8-byte-width
operations.

```c
/* order2 is required for the WRITE_ONCE to be visible in program order,
   but atomicity requires the address itself to be aligned. */
WRITE_ONCE(plt->target, new_dest);   /* width = 8, alignment = ? */
```

The verifier / code audit gap:
- `READ_ONCE` / `WRITE_ONCE` only compile to a singlke "access width" load/store.
- The compiler extends with correct alignment based on `alignof`. If the
  field is inside an `__attribute__((packed))` or inline struct with
  unknown alignment, the compiler can issue the same 8-byte LDR/STR to a
  potentially misaligned address, and nothing in `READ_ONCE` validates it.

---

## References

- CVE-2026-23383: https://nvd.nist.gov/vuln/detail/CVE-2026-23383
- Debian security tracker: https://security-tracker.debian.org/tracker/CVE-2026-23383
- Red Hat CVE advisory: https://access.redhat.com/security/cve/cve-2026-23383
- Endor Labs analysis: https://www.endorlabs.com/vulnerability/debian-cve-2026-23383
- GitHub GHSA advisory: https://github.com/advisories/GHSA-887m-4qrh-hjq5
- Upstream fix: `arch/arm64/net/bpf_jit_comp.c` — `bpf_jit_binary_pack_alloc()`
  alignment change (6.12.85 / 6.19.8 stable)
