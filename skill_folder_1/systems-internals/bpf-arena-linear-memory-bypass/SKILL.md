# BPF Arena Linear Memory Bypass — `BPF_MAP_TYPE_ARENA`
Mechanistic teaching module on Linux `bpf_arena` (BPF_MAP_TYPE_ARENA): sparse on-demand shared memory, address-space casting, `bpf_arena_alloc_pages()`, lazy page-fault allocation, `BPF_F_MMAPABLE`, the BPF vs user virtual address mapping invariant, the `vmap_pages_range()` controversy, security/atomicity tradeoffs, and how this bypasses traditional BPF map overhead with real kernel-pinning semantics.

Target audience: OS students, eBPF developers, and kernel/database engineers who want to reason below "how to use" into why arena works, what it changes about BPF safety model, and where it silently breaks.

## 1. The Core Problem with Traditional Maps

Traditional BPF maps force one of three bad choices:
- Ringbufs: one-way (kernel→user), no random access, no pointer following.
- Hash/Array maps: every userspace access requires a `bpf()` system call.
- Array maps mapped via `mmap()`: reserve full `max_entries × value_size` upfront in non-pageable kernel memory; unused pages waste locked kernel RAM.

Worse, the BPF verifier forbids storing kernel pointers across map entries, so linked lists, trees, and graphs must encode adjacency as integer indices:
```c
struct node { int next_idx; int data; };
```
Every traversal step: `bpf_map_lookup_elem(&nodes_map, &idx)` — separate syscall-equivalent, verifier check, and cache miss.

`bpf_arena` eliminates this by providing:
1. A sparse virtual memory region shared between BPF and userspace.
2. Real C pointer dereference inside BPF programs (`__arena` pointers).
3. On-demand page allocation: pages appear only when touched.
4. Zero-copy userspace access via `mmap()` — no `bpf()` per element.

## 2. Address-Space Mapping Invariant

Arena works because of a deliberate kernel invariant:

> Lower 32 bits of userspace `mmap()` address == BPF program 32-bit pointer value.

Kernel maps the arena at two virtual addresses:
- BPF world: 32-bit address space (separate from normal kernel linear map).
- User world: high canonical address (e.g., `0x0000_ffff_ffff_0000` + page-aligned offset on x86-64, or `0xffff_0000_0000_0000` on arm64).

Because the low 32 bits match, a cast is trivial: just reinterpret the pointer in the other address space. No full 64-to-32 truncation pass is required.

`map_extra` carries the user-space mapping base hint:
```c
__ulong(map_extra, 0x1ull << 44);  // x86-64 typical base
__ulong(map_extra, 0x1ull << 32);  // arm64 typical base
```

## 3. Pointer Provenance in the Verifier

Traditional BPF pointers come from `map_lookup_elem()`, `probe_read()`, etc. and are tagged as `PTR_TO_MAP_VALUE`/`PTR_TO_MEM`. The verifier prevents:
- Storing them in maps.
- Pointer arithmetic beyond one element.
- Arithmetic mixing with scalar integers.

Arena pointers carry the `__arena` annotation. The verifier:
- Treats `__arena` pointers as a separate register type.
- Allows arithmetic (`ptr + offset`) within the same arena region.
- Allows dereference with normal load/store instructions.
- Allows storing `__arena` pointers into arena memory itself, enabling linked structures.

The verifier still disallows mixing `__arena` pointers with standard BPF pointers in the same expression. This prevents aliasing bugs but requires explicit casts at boundary functions:
```c
long ret = bpf_arena_alloc_pages(&arena, order);
struct node __arena *n = (void __arena *)ret;
```

## 4. Page Allocation Paths

### 4.1 Explicit Allocation

`bpf_arena_alloc_pages(struct bpf_map *map, u32 order)` allocates `2^order` physically contiguous pages and maps them into the arena's virtual region. Order-0 = one page. Failures return 0 (NULL), which the verifier tracks precisely.

### 4.2 Lazy Allocation (Page Fault)

Userspace accesses an unmapped page inside the `mmap()` region → do_page_fault() → kernel handles inside `bpf_arena` fault handler → allocates a zeroed page → maps it → resumes userspace.

This means userspace can do:
```c
size_t *counter = mmap_base + ARENA_OFFSET;
(*counter)++;  // First touch allocates page implicitly
```
No `bpf()` syscall, no explicit kernel interaction.

## 5. The `vmap_pages_range()` Controversy

Arena pages must be mapped into the kernel's direct map or a dedicated kernel vmalloc region so BPF JIT code can access them with normal load instructions. The implementation uses `vmap_pages_range()` — an internal VM function lacking the safety checks of public `vmap()`.

Arguments in the review thread:
- Christoph Hellwig (VM maintainer): exposes internal VM abstractions; breaks encapsulation after years of cleanup.
- Johannes Weiner: `vmap()` was made internal because only BPF still needed it; public/private distinction is historical accident.
- Lorenzo Stoakes: security concern — internal API lacks bounds checks.
- Linus Torvalds: "The onus of coming up with an acceptable solution is on the person who needs something new." Rejected demand for perfection without providing alternative.

Current practical status: arena uses internal VM path. If you backport arena to an older tree, you must export or inline `vmap_pages_range()`.

## 6. Security Model and Invariants

Arena intentionally relaxes BPF's usual safety boundary. New attack surfaces:

1. **Kernel pointer disclosure via race:** If userspace writes crafted pointer values into shared memory while BPF reads them, and `BPF_F_NO_USER_CONV` is not set, BPF could cast an attacker-controlled user-pointer-like value back to a kernel address. The `__arena` provenance tracking and address-space mapping make this hard but not impossible.
2. **Use-after-free within arena:** Arena allocator does not track referenced regions. A BPF linked list can hold a dangling node if the page was freed externally (only possible currently if the map is destroyed; no `bpf_arena_free_pages()` helper). Design invariant: arena data structures must outlive any holder, or use epoch/reclamation discipline.
3. **Fork races:** Arena is inherited across `fork()`. Both processes share the same kernel backing. Concurrent modifications must be synchronized by the application.
4. **Size accounting:** 4GB virtual size does not mean 4GB physical allocation. But if a malicious BPF program allocates every page, it can consume up to 4GB of non-pageable kernel memory. The verifier caps instruction count, but not allocation volume — a misbehaving or compromised BPF program is a memory pressure vector.
5. **Atomicity of stores:** Single 8-byte store is atomic on supported architectures. But multi-word structures (e.g., 16-byte node header) require explicit synchronization if readers can race with writers.

## 7. Performance Properties

### Eliminated per-element costs

| Operation | Hash map | Arena |
|-----------|----------|-------|
| Insert | `bpf_map_update_elem()` = syscall + verifier pass + hash bucket lock | store into mmap'd page |
| Lookup | `bpf_map_lookup_elem()` = syscall + verifier pass + hash scan | load from mmap'd page via pointer |
| Traverse linked list | syscall per node | pointer chase with cache loads only |

### Allocation behavior

- Initial pages: 0 cost. Touch a page → one `alloc_page(GFP_KERNEL)` + vmap.
- No pre-allocation; partially used structures only consume touched pages.
- Sequential allocation → adjacent virtual pages (good for prefetch/TLB).
- Random allocation → scattered pages (TLB pressure).

### syscall overhead eliminated entirely for:
- Shared counters updated by BPF and read by userspace.
- Event notification pointers written by BPF, consumed by polling userspace.
- Large work-queue arrays where index is a scalar but storage is contiguous.

## 8. Code Paths and Key Symbols

### Userspace mmap
```
sys_mmap()
  → bpf_map_mmap()           // checks BPF_F_MMAPABLE
    → vm_map_pages()         // most architectures
      → vm_ops->fault()      // lazy allocation on miss
```

### BPF program access
```
bpf_prog_run()
  → JIT code executes:
      r1 = *(u32 *)(rX + OFFSET)   // direct VMA read
  → if page not mapped:
      page fault → bpf_arena_fault() → alloc_page → map into kernel VMA
```

### Key symbols
| Symbol | File (6.15+) | Role |
|--------|--------------|------|
| `BPF_MAP_TYPE_ARENA` | `include/linux/bpf.h` | Map type |
| `bpf_arena_alloc_pages()` | `kernel/bpf/arena.c` | Explicit alloc helper |
| `BPF_F_MMAPABLE` | `include/uapi/linux/bpf.h` | Enables userspace mmap |
| `BPF_F_NO_USER_CONV` | `include/uapi/linux/bpf.h` | Disable automatic cast |
| `bpf_map_mmap()` | `kernel/bpf/syscall.c` | mmap handler |
| `bpf_arena_fault()` | `kernel/bpf/arena.c` | Page-fault handler |

## 9. Demonstrating the Bypass

Compare a BPF linked list in a traditional array map vs arena:

### Traditional (syscall-per-node)
```c
struct node { int next_idx; int data; };
struct bpf_map *nodes = ...;
n = bpf_map_lookup_elem(&nodes, &idx);     // bpf() trap
process(n->data);
idx = n->next_idx;
```

### Arena (syscall-zero traversal)
```c
struct node __arena { struct node __arena *next; int data; };
struct node __arena *head = ...;
for (struct node __arena *n = head; n; n = n->next)
    process(n->data);
```

Same logical operation; arena version runs entirely inside BPF VM without kernel boundary crossing.

## 10. Debugging and Validation

Key traces:
- `bpf:bpf_map_alloc` for arena page allocations.
- `bpf:bpf_map_free` when arena is torn down.
- Userspace: `perf trace -e syscall:mmap` + inspect `/proc/<pid>/maps`.

Common failure modes:
- SIGBUS on userspace touch → page fault inside arena map handler failed (memory pressure). Check `dmesg` for OOM context.
- Verifier rejects `__arena` pointer arithmetic → forgot `__arena` annotation on intermediate variables.
- JIT segfault → arena unloaded while BPF program still running; map reference must be held by pinned file or FD.

## 11. Relationships and Dependencies

- **eBPF verifier:** arena pointer type is a new dimension in register state; affects precision-tracking logic.
- **io_uring BPF filter:** registered-buffer kfunc gap (Ming Lei series) is a parallel discussion about allowing BPF to pin/use user memory without copies — conceptually related to arena's mmap approach but implemented via different mechanism (registered file descriptors vs mmap'd map).
- **XDP/AF_XDP UMEM:** UMEM uses `mmap()` from userspace into kernel BPF pages for zero-copy RX. Arena generalizes this pattern from packet buffers to arbitrary data.
- **bpf_jit:** 32-bit vs 64-bit pointer truncation in JIT-compiled BPF must handle `__arena` pointers correctly; check if your kernel's JIT was built with `CONFIG_BPF_JIT_DEFAULT_ON`.

## 12. Watch Items (2026–2027)

- `bpf_arena_free_pages()` explicit deallocation helper (proposed; would give BPF programs reclamation control).
- Per-cgroup arena accounting (currently arena pages count toward cgroup MEMCG charge but no dedicated throttle).
- Multi-arena spanning with automatic migration/pinning for NUMA-aware BPF programs.
- Integration with `bpf_timer` for deferred page release in BPF-implemented slab allocators.

## 13. Practical Recommendations

1. Use arenas for linked structures, adjacency lists, or large shared buffers you need to access from both sides.
2. Use `BPF_F_NO_USER_CONV` if userspace must not follow internal pointers — reduces kernel surface for pointer-confusion bugs.
3. Always align 4GB arenas to 4GB boundaries; align smaller arenas to 2MB hugepage boundaries for TLB efficiency.
4. Do not rely on arena for security boundaries; treat arena-backed regions as fully trusted between BPF and its loader.
5. Combine with `bpf_timer` or `bpf_send_signal()` inside BPF for lifecycle notification if userspace needs to know when allocation runs full.

## 14. References

- LWN: "A proposal for shared memory in BPF programs" — https://lwn.net/Articles/961941/
- Eunomia tutorial: https://eunomia.dev/tutorials/features/bpf_arena/
- Alexei Starovoitov patch series (Feb 2024): kernel mailing list
- LLVM BPF backend patches for address-space casts
- Related CVE/surface: io_uring ZCRX freelist race (CVE-2026-43121) — same on-demand page-mapping pattern from networking angle
