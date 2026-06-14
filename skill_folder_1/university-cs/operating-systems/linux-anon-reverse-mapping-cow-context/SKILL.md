---
title: "Linux Anonymous Reverse Mapping: COW Context Redesign"
category: "university-cs/operating-systems"
tags: ["linux-kernel", "memory-management", "reverse-mapping", "cow", "mm_struct", "lsfmm-bpf-2026"]
difficulty: "advanced"
prerequisites: ["linux-memory-management-fundamentals", "page-tables-and-pte", "fork-copy-on-write", "vma-anon-vma-basics"]
---

# Linux Anonymous Reverse Mapping: COW Context Redesign

## Learning Objectives

After completing this skill, you will be able to:

1. **Explain the purpose of reverse mapping** in Linux memory management and why it's needed for anonymous pages
2. **Describe the current anon_vma design** including its data structures (anon_vma, anon_vma_chain), lookup algorithms, and lifetime management
3. **Identify the scalability and complexity problems** with the current VMA-granularity approach after 20+ years of accreted evolution
4. **Understand the COW Context proposal** from LSFMM+BPF 2026 (Lorenzo Stoakes) as a process-granularity redesign
5. **Analyze the tradeoffs** between VMA-level and process-level tracking: object count, lock contention, RCU friendliness, MAP_PRIVATE handling
6. **Trace the reverse-mapping lookup path** in both designs: page→anon_vma→VMA chain vs page→cow_context→process hierarchy
7. **Evaluate the current state** of the prototype (git branch `project/cow-context`, first draft, incomplete)

## Prerequisites

- Linux virtual memory fundamentals: page tables, PTEs, folios, page cache
- Process address space: mm_struct, VMA (vm_area_struct), fork() semantics
- Copy-on-write mechanics: page fault on write, PTE duplication, reference counting
- Kernel synchronization: spinlocks, RCU, lock contention patterns
- Basic understanding of memory reclaim and page migration requiring reverse maps

---

# Module 1: Why Reverse Mapping Exists

## The Forward vs Reverse Mapping Problem

**Forward mapping** (hardware-assisted): Virtual Address → Physical Page (via page tables)
- Hardware walks page tables on every memory access
- TLB caches recent translations

**Reverse mapping** (software-only): Physical Page (folio) → All PTEs mapping it
- **No hardware support** - kernel must maintain this itself
- Required for any operation that needs to find all mappings of a physical page

## Operations Requiring Reverse Mapping

| Operation | Why Reverse Map Needed |
|-----------|------------------------|
| **Page reclaim** | Must unmap page from all processes before freeing |
| **Page migration** | Must update all PTEs pointing to page being moved |
| **Swap-out** | Must unmap page from all processes before writing to swap |
| **NUMA balancing** | Must find all mappings to migrate to preferred node |
| **Copy-on-write fork** | Must track shared anonymous pages between parent/child |
| **KSM (Kernel Samepage Merging)** | Must find all processes sharing identical pages |
| **HWPoison / memory failure** | Must unmap corrupted page from all processes |

## Anonymous vs File-Backed Pages

- **File-backed pages**: Reverse map via `address_space` (inode) + `i_mmap` tree - relatively straightforward
- **Anonymous pages**: No inode, no persistent identity - must track via process hierarchy (anon_vma)

---

# Module 2: Current anon_vma Design (Mechanistic Deep Dive)

## Core Data Structures

### struct anon_vma
```c
struct anon_vma {
    struct anon_vma *root;           // Root of anon_vma tree (for locking)
    struct rb_root_cached rb_root;   // RB-tree of anon_vma_chain (VMAs)
    atomic_t refcount;               // Lifetime management
    unsigned int degree;             // Number of child anon_vmas
    struct anon_vma *parent;         // Parent in hierarchy
    // ... lockdep, RCU head, etc.
};
```

### struct anon_vma_chain
```c
struct anon_vma_chain {
    struct vm_area_struct *vma;      // VMA this chain belongs to
    struct anon_vma *anon_vma;       // anon_vma this chain links to
    struct rb_node rb;               // RB-tree node in anon_vma's tree
    struct list_head same_vma;       // Link in VMA's anon_vma_chain list
};
```

### Page → anon_vma Pointer
- Stored in `page->mapping` (reused for anon pages with `PAGE_MAPPING_ANON` flag set)
- Low bit indicates anonymous vs file mapping
- Points to **one** anon_vma (the one where page was first instantiated)

### VMA → anon_vma Chain
- Each VMA has `struct list_head anon_vma_chain` 
- Links to all anon_vmas this VMA participates in
- Created at `mmap()`/`fork()`/`mremap()` time

## Fork Mechanics: Building the anon_vma Hierarchy

```
Parent process (before fork):
  mm_struct
    └── VMA (file or anon)
          └── anon_vma_chain → anon_vma (root)

fork() creates child:
  1. Duplicate parent's mm_struct (copy VMAs)
  2. For each anon VMA in parent:
     a. Create NEW anon_vma for child
     b. Set child_anon_vma->parent = parent_anon_vma
     c. Set child_anon_vma->root = parent_anon_vma->root
     d. Link child VMA to child_anon_vma via anon_vma_chain
     e. existing pages still point to parent_anon_vma (shared)
  3. On COW fault in either process:
     a. Allocate new page
     b. Update faulting process's PTE
     c. New page points to faulting process's anon_vma
```

## Reverse Mapping Lookup Algorithm (Current)

**Given**: folio (anonymous page)  
**Goal**: Find all PTEs in all processes mapping this folio

```c
// Simplified rmap_walk_anon() path
folio → page_mapping() → anon_vma (with PAGE_MAPPING_ANON flag)
    → anon_vma_lock_read(anon_vma->root)  // Lock entire hierarchy
    → rmap_walk_anon_locked(folio, anon_vma, callback)
        → For each anon_vma in hierarchy (DFS):
            → For each anon_vma_chain in anon_vma->rb_root:
                → vma = chain->vma
                → If vma->vm_mm matches target (or all):
                    → pte_offset_map() → callback(pte, ...)
    → anon_vma_unlock_read()
```

**Key properties**:
- Locks **entire anon_vma hierarchy** (root anon_vma) during walk
- Walks RB-tree of VMAs per anon_vma
- Complexity: O(VMAs in hierarchy) - can be large for processes with many VMAs
- `fork()` holds this lock across entire operation → contention hotspot

## Lifetime Management

| Event | anon_vma Behavior |
|-------|-------------------|
| `mmap(MAP_ANONYMOUS)` | Create new anon_vma, link VMA |
| `fork()` | Create child anon_vma, link to parent, increment refcounts |
| COW page fault | New page → faulting process's anon_vma |
| `munmap()` / process exit | Unlink VMA from anon_vma_chain, decrement refcount |
| Last refcount drop | Free anon_vma (after RCU grace period) |
| Page freed | folio's mapping cleared |

**Critical invariant**: anon_vma persists as long as any page points to it OR any VMA links to it

---

# Module 3: Problems with Current Design

## Scalability Issues

### Object Explosion
- **One anon_vma per VMA** (not per process)
- Process with 10,000 VMAs = 10,000 anon_vma objects + 10,000 anon_vma_chain objects
- Chrome, JVM, databases routinely have 10K-100K VMAs
- Each object: ~128-256 bytes → MBs of kernel memory overhead

### Lock Contention on fork()
- `fork()` takes `anon_vma->root` lock (read) for **entire duration**
- With many VMAs, lock held for milliseconds
- Blocks concurrent page faults, reclaim, migration on **all** related processes
- NUMA systems: remote lock access adds latency

### RB-Tree Overhead
- Each anon_vma maintains RB-tree of its VMAs
- Insert/delete on every `mmap`/`munmap`/`mremap`/`fork`
- Cache misses traversing RB-trees during rmap walks

## Code Complexity (20+ Years of Accretion)

| Era | Change | Complexity Added |
|-----|--------|------------------|
| 2002 | Rik van Riel initial rmap | Basic anon_vma |
| 2004 | Andrea Arcangeli rework | anon_vma hierarchy, root locking |
| 2010 | Transparent Huge Pages | PMD-level reverse maps, splitting |
| 2013 | KSM integration | Stable node tracking |
| 2016 | `mremap()` fixes | anon_vma reuse logic |
| 2019 | Folio conversion | folio vs page handling |
| 2020+ | `folio_add_anon_rmap` etc. | New helper proliferation |

Result: **Multiple lock types** (spinlock, RWSEM, RCU), **subtle lifetime rules**, **special cases** for THP, KSM, hugetlb, `mremap()`, `userfaultfd`

## MAP_PRIVATE File Mappings

- File-backed but COW on write → same reverse-map needs as anonymous
- Currently shoehorned into anon_vma machinery
- Creates additional `anon_vma` objects for file VMAs
- "Pain of their own" per Stoakes

## RCU Unfriendliness

- Reader-writer lock on hierarchy root prevents RCU read-side critical sections
- Walk requires lock acquisition → no lockless fast path
- Page-table freeing requires lock → complex RCU grace period coordination

---

# Module 4: COW Context Proposal (LSFMM+BPF 2026)

## Core Idea: Process-Granularity Tracking

**Shift from VMA-level to mm_struct-level**

| Aspect | Current (anon_vma) | Proposed (COW Context) |
|--------|-------------------|------------------------|
| Granularity | Per-VMA | Per-process (mm_struct) |
| Objects/process | O(VMAs) | O(1) |
| Hierarchy | anon_vma tree | Process tree (mm_struct) |
| Page pointer | folio→anon_vma | folio→cow_context |
| Lookup | Walk anon_vma→VMA RB-tree | Walk process hierarchy tree |
| Lock scope | Entire anon_vma hierarchy | Single context + RCU |

## COW Context Data Structure

```c
struct cow_context {
    struct mm_struct *mm;              // Owning process address space
    struct cow_context *parent;        // Parent in fork hierarchy
    struct list_head children;         // Child contexts
    atomic_t refcount;                 // Lifetime (outlives process if children exist)
    spinlock_t lock;                   // Protects context tree modifications
    // Future: per-context page-table tracking, generation counters
};
```

**Key invariant**: One `cow_context` per `mm_struct` (per process)

## Fork Mechanics with COW Context

```
Parent process:
  mm_struct → cow_context (refcount=1)

fork() creates child:
  1. Allocate child mm_struct
  2. Allocate child cow_context
  3. child_cow_context->parent = parent_cow_context
  4. list_add(&child_cow_context->sibling, &parent_cow_context->children)
  5. atomic_inc(&parent_cow_context->refcount)
  6. Existing pages: still point to parent_cow_context (shared)
  7. On COW fault:
     a. New page → faulting process's cow_context
```

## Folio-to-Context Pointer

- Each folio gains `folio->cow_context` pointer (replaces `folio->mapping` for anon)
- Points to **lowest** cow_context in hierarchy where page is mapped
- **Optimization**: When page first mapped in child after fork, points to child's context
- Avoids walking up hierarchy for common case (private pages)

## Reverse Mapping Lookup Algorithm (Proposed)

```c
// Given: folio
// Goal: Find all PTEs mapping this folio

cow_context = folio->cow_context;           // Start at lowest mapping context
cow_context_lock(cow_context);              // Fine-grained lock

// Walk UP hierarchy to root
while (cow_context) {
    if (cow_context->mm) {
        // Scan this process's page tables for folio
        rmap_walk_mm(cow_context->mm, folio, callback);
    }
    cow_context = cow_context->parent;
}

// Walk DOWN sibling subtrees not yet visited
// (Ensure we visit ALL processes sharing this folio)
cow_context_walk_descendants(folio->cow_context, callback);

cow_context_unlock();
```

**Key properties**:
- O(processes sharing page) not O(VMAs)
- No RB-tree traversal
- Lock per-context, not global hierarchy

## Lifetime Management

| Event | COW Context Behavior |
|-------|---------------------|
| Process creation (`fork`/`clone`) | Allocate cow_context, link to parent |
| COW page fault | New page → faulting context |
| `munmap()` / page unmapped | No context change (other mappings may exist) |
| Process exit (no children) | Free context immediately |
| Process exit (has children) | Context persists, refcount decremented when last child exits |
| Last child exits | Free context after RCU grace period |

**Critical difference from anon_vma**: Context lifetime tied to **process hierarchy**, not page/VMA references. Context exists as long as any descendant process exists.

---

# Module 5: Technical Challenges & Open Questions

## Address Remapping

**Problem**: Same folio mapped at different virtual addresses in different processes
- Current: VMA stores address range → easy to compute PTE location
- Proposed: cow_context only knows mm_struct → must scan entire page table?

**Potential solutions**:
- Per-context page-table index (radix tree of VFNs?)
- Accept full page-table scan (O(PTEs) not O(VMAs) - still better for sparse mappings)
- Track VMA list within context for address-range queries

## MAP_PRIVATE File Mappings

- File-backed but COW on write
- Need reverse mapping for both file identity AND COW tracking
- Current: Uses anon_vma for COW part
- Proposed: How to integrate?
  - Option A: Separate file rmap + cow_context for COW
  - Option B: Extend cow_context with file mapping info
  - Option C: "Pain of their own" - solve separately

## RCU vs Locking Tradeoff

| Approach | Pros | Cons |
|----------|------|------|
| **Fine-grained spinlock per context** | Simple, deterministic | Lock contention on hot contexts |
| **RCU read-side for walks** | Lockless readers | Writers need grace periods; complex |
| **Hybrid**: RCU for tree structure, spinlock for page-table scans | Best of both | Most complex |

Stoakes noted: "RCU is faster but lacks synchronization points; needs some sort of lock with mapping granularity"

## Race Tolerance Alternative

**"Crazier" option** (Stoakes):
- Tolerate races in reverse-map walk
- Delay page-table freeing until after RCU grace period
- Accept that concurrent COW fault might miss a mapping temporarily
- **Risk**: Could leave stale mappings → security/stability issues

## THP (Transparent Huge Pages) and Folio Support

- Current anon_vma handles PMD-level mappings
- COW context must handle folio (multi-page) mappings
- Page-table walk must handle PMD → PTE splitting correctly
- Per-folio cow_context pointer vs per-page?

## KSM (Kernel Samepage Merging) Integration

- KSM merges identical anonymous pages across processes
- Creates shared pages not from fork
- Current: Stable nodes in anon_vma tree
- Proposed: How to track cross-hierarchy sharing?
  - cow_context tree only covers fork hierarchy
  - KSM pages need separate cross-process tracking

## Migration and NUMA Balancing

- Page migration needs to update all PTEs
- Current: rmap_walk finds all PTEs efficiently
- Proposed: cow_context walk must be equally fast
- NUMA faults: need to find all mappings quickly

## Memory Overhead Comparison

| Metric | anon_vma (current) | cow_context (proposed) |
|--------|-------------------|------------------------|
| Per-process base | 1 root anon_vma | 1 cow_context |
| Per-VMA | 1 anon_vma + 1 chain | 0 |
| Per-shared-page | 1 folio→anon_vma ptr | 1 folio→cow_context ptr |
| Lock objects | 1 RWSEM per hierarchy root | 1 spinlock per context |
| Typical Chrome tab | ~500 objects | ~1 object |

---

# Module 6: Current State & Implementation Status

## Prototype Repository

- **Git**: `git.kernel.org/pub/scm/linux/kernel/git/ljs/linux.git`
- **Branch**: `project/cow-context`
- **Author**: Lorenzo Stoakes
- **Status**: First draft, incomplete, rough edges

## What Exists (Per Summit Presentation)

- Basic cow_context allocation/free
- Fork hierarchy linking (parent/children lists)
- Folio→cow_context pointer integration
- Initial page-table walk using cow_context tree
- Refcount-based lifetime management

## What's Missing / Incomplete

| Component | Status |
|-----------|--------|
| Address remapping (different VAs per process) | Not implemented |
| MAP_PRIVATE file mapping integration | Not addressed |
| RCU vs locking decision | Undecided |
| THP/folio splitting support | Not implemented |
| KSM cross-hierarchy tracking | Not designed |
| NUMA/migration page-table updates | Not tested |
| Lock validation (lockdep, lockstat) | Pending |
| Performance benchmarks vs anon_vma | None |
| xfstests / mmtests integration | None |
| Documentation (kernel-doc) | None |

## Community Reception (LSFMM+BPF 2026)

- **No discussion** - session ran out of time
- Stoakes acknowledged: "research project that might not work out"
- **Key question from audience**: None recorded (time overrun)

## Path to Mainline (If Pursued)

1. Complete address remapping solution
2. Resolve MAP_PRIVATE integration strategy
3. Decide and implement RCU/locking model
4. Add THP/folio support
5. Implement KSM cross-hierarchy tracking
6. Comprehensive mmtests/xfstests validation
7. Performance benchmarking vs current anon_vma
8. Incremental merge: start with opt-in for specific architectures/workloads
9. Long-term: replace anon_vma entirely (flag day or gradual migration)

---

# Module 7: Hands-On Exercises

## Exercise 1: Trace Current anon_vma Code Path

**Goal**: Understand the existing reverse-map walk

```bash
# In kernel source tree
grep -r "rmap_walk_anon" mm/
grep -r "anon_vma_lock" mm/
less mm/rmap.c  # Core reverse mapping logic
```

**Questions**:
1. Where is the hierarchy root lock acquired?
2. How does the walk traverse from anon_vma to VMA?
3. What callback signature is used?
4. How are THP (PMD) mappings handled differently?

## Exercise 2: Compare Object Counts

**Goal**: Quantify the object explosion problem

```c
// Kernel module or bpftrace script
// Count anon_vma + anon_vma_chain per process
```

```bash
# bpftrace one-liner (requires root)
bpftrace -e 'kprobe:anon_vma_alloc { @[comm] = count(); } kprobe:anon_vma_free { @[comm]--; } interval:s:10 { print(@); clear(@); }'
```

**Analyze**: How many objects for Chrome vs simple process?

## Exercise 3: Explore Cow Context Prototype

```bash
git clone git://git.kernel.org/pub/scm/linux/kernel/git/ljs/linux.git
cd linux
git checkout project/cow-context
grep -r "cow_context" mm/
```

**Questions**:
1. Where is `struct cow_context` defined?
2. How is the folio→cow_context pointer stored?
3. What locking primitive is used?
4. How does fork create the child context?

## Exercise 4: Design Review - Address Remapping

**Task**: Write a design proposal for handling address remapping in cow_context

**Requirements**:
- Same folio mapped at VA 0x1000 in parent, VA 0x5000 in child
- Reverse-map walk must find both PTEs efficiently
- Must not require full page-table scan on every walk

**Deliverable**: 1-page design doc with:
- Data structure additions
- Lookup algorithm pseudocode
- Memory overhead analysis
- Locking requirements

## Exercise 5: RCU vs Locking Tradeoff Analysis

**Task**: Model the contention scenarios

| Scenario | anon_vma (current) | cow_context (spinlock) | cow_context (RCU) |
|----------|-------------------|------------------------|-------------------|
| fork() | | | |
| COW fault (shared page) | | | |
| Reclaim (walk all mappings) | | | |
| Migration (update all PTEs) | | | |
| Process exit (cleanup) | | | |

**Research**: What are typical contention windows? Use `perf lock` or lockstat.

---

# Module 8: References & Further Reading

## Primary Sources

- **LWN.net Article 1072378**: "Keeping COWs in context (a.k.a. anonymous reverse mapping)" — Jonathan Corbet, May 14, 2026
- **LSFMM+BPF 2026 Summit**: Session by Lorenzo Stoakes
- **Git Repository**: `git.kernel.org/pub/scm/linux/kernel/git/ljs/linux.git` branch `project/cow-context`

## Historical Context

- **LWN.net**: "The Anonymous Reverse Mapping – An Introduction" (Oracle Linux Blog)
- **Rik van Riel (2002)**: Original reverse mapping patch
- **Andrea Arcangeli (2004)**: Major anon_vma rework
- **Mel Gorman**: "Linux Page Reclaim and Reverse Mapping" (various talks)

## Current Kernel Implementation

- `mm/rmap.c` — Core reverse mapping logic
- `mm/anon_vma.c` — anon_vma allocation, linking, lifetime
- `include/linux/anon_vma.h` — Data structure definitions
- `mm/memory.c` — COW fault handling (`do_wp_page()`, `wp_page_copy()`)
- `mm/migrate.c` — Page migration reverse mapping

## Related Kernel Subsystems

- **KSM**: `mm/ksm.c` — Kernel Samepage Merging
- **THP**: `mm/huge_memory.c` — Transparent Huge Pages reverse mapping
- **NUMA Balancing**: `mm/migrate.c`, `kernel/sched/numa_balancing.c`
- **Userfaultfd**: `mm/userfaultfd.c` — User-space page fault handling

## Academic / Theoretical

- "Scalable anon_vma in Linux kernel 2.6.34" — Karthick AR
- "Operating Systems: Three Easy Pieces" — Ch. on Virtual Memory, Fork/COW
- "Linux Kernel Development" — Robert Love, Ch. on Memory Management

---

## Assessment Checklist

After completing this skill, verify you can:

- [ ] Draw the anon_vma hierarchy for a 3-generation fork tree
- [ ] Trace rmap_walk_anon() from folio to PTE callback
- [ ] Explain why `fork()` holds the anon_vma root lock
- [ ] Describe the cow_context data structure and its invariants
- [ ] Compare object counts: 100-VMA process in both designs
- [ ] List the 5 major unsolved challenges in cow_context
- [ ] Argue for/against RCU vs spinlock for cow_context walks
- [ ] Explain how KSM sharing breaks the fork-hierarchy model

---

*Skill created from LSFMM+BPF 2026 Summit coverage (LWN.net 1072378). This is a teaching skill for mechanistic OS internals — not a how-to-use guide. The cow_context proposal is a research prototype; production deployment is speculative.*