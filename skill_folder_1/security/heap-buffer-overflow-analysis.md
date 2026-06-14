# Heap Buffer Overflow Analysis for Server-Side Applications (CWE-122)

A practical offensive-security skill covering identification, analysis, and exploitation of heap buffer overflows in server-side C/C++ applications, with case studies from NGINX, Apache, and similar high-performance software.

---

## When to Use This Skill

Use this skill when:
- Analyzing CVE reports mentioning heap buffer overflow (CWE-122) in server software
- Auditing NGINX/Apache/mod_* modules for memory corruption
- Building detection rules for overflow-producing request patterns
- Differentiating heap overflow from stack overflow and use-after-free
- Planning exploitation paths: DoS vs. RCE tradeoffs given ASLR/CFI/PIE

---

## Core Concepts

### 1. Heap vs. Stack vs. Global Overflow
- **Heap:** Dynamic allocation (`malloc`, `calloc`, `ngx_palloc`, `slab` allocator). Corrupts adjacent heap chunks, metadata, or linked-lists.
- **Stack:** Automatic local variables. Corrupts saved frame pointer / return address → RCE.
- **Global/BSS:** Static buffers. Less common in modern server software.

**Server-side twist:** High-performance servers use custom allocators (NGINX pool allocator, jemalloc, tcmalloc). Standard glibc heap techniques may not apply directly.

### 2. Common Trigger Patterns in Server Software

| Pattern | Example Context | Root Cause |
|---------|----------------|------------|
| **Unbounded regex capture → small buffer** | PCRE captures too many chars for expected replacement buffer (NGINX CVE-2026-42945) | Computes dest size from template, not src |
| **Header/cookie concatenation** | `sprintf(buf, "%s%s", user_header, fixed_suffix)` | Trusts attacker-controlled input length |
| **Path traversal / URI normalization** | `realpath()` output exceeds expected PATH_MAX | Assumes canonical path fits static buffer |
| **Chunked transfer miscalculation** | Content-length mismatch in chunked encoding | Parses chunk size but allocates wrong size |
| **Module-to-core callback overflow** | Module writes to core-provided buffer without size check | Missing bounds verification at API boundary |

### 3. NGINX-Specific Memory Model

NGINX uses `ngx_pool_t` (similar to Apache `apr_pool_t`):
- Sub-pools per request (`ngx_http_request_t`)
- Large allocations go directly to `malloc`
- Small allocations come from contiguous "arena" style blocks
- **Key insight:** Exploiting NGINX often means corrupting *another request's pool block* or a shared slab if you can influence allocation ordering.

**Analysis Loci:**
- `ngx_http_rewrite_module`: PCRE regex handling → string substitution → buffer alloc
- `ngx_http_proxy_module`: Header parsing and forwarding
- `ngx_http_core_module`: URI and location matching

---

## Analysis Methodology

### Step 1: Identify the Vulnerable Code Path

For any reported CVE:
1. Check which module/directive triggers it
2. Read the source for that directive's handler
3. Identify where user input enters a `*alloc` call
4. Check if the allocation size accounts for full user-controlled length

**NGINX Example (CVE-2026-42945):**
```c
// Pseudocode from rewrite module
size = ngx_strlen(replacement_template); // calculates from template
buf = ngx_palloc(pool, size);
ngx_memcpy(buf, actual_user_input, actual_user_input_len); // overflow!
```

### Step 2: Determine Impact Boundaries

- **Does the overwritten region contain function pointers?**
- **Is this a persistent overflow** (many sequential requests can groom the heap)?
- **What allocator controls the region?**
- **Can the attacker influence adjacent allocations** (e.g., by triggering other allocations in the same worker)?

### Step 3: Assess Exploitation Feasibility

| Factor | Favorable Conditions | Unfavorable Conditions |
|--------|----------------------|------------------------|
| ASLR enabled | Info leak + heap groom | No info leak → RCE unlikely |
| PIE / RELRO | Stack pivot harder | ROP-only chains |
| Custom allocator | May lack safe-unlink | Fixed slab layouts predictable |
| Root cause | Overflow into controlled data | Into random metadata → crash |
| Crash tolerance | Persistent connection (HTTP/2, proxy) | Worker dies, new process → ASLR reset |

### Step 4: Detection Design

1. **Network-layer anomalies:**
   - Request bodies or headers with high entropy + high repetition
   - POST/GET parameters exceeding typical length thresholds for the target endpoint

2. **Host-layer telemetry:**
   - NGINX worker crashes (`core_pattern` / `coredump`)
   - `dmesg` OOM or segfault from `nginx: worker process`
   - Abnormal allocation sizes via eBPF (if available)

3. **WAF rules:**
   - Regex to detect path traversal combined with rewrite-like URL structures
   - Rate-limit requests with params exceeding N× typical length

---

## Exploitation Considerations: DoS vs. RCE

### Reliable DoS Path
- Craft input that deterministically overflows accessible heap region
- Target critical metadata: `ngx_pool_t` linked list, slab bitmap
- Trigger on next allocation → crash
- **Counter:** Auto-restart, multiple workers, upstream load balancer

### RCE Path
- Requires:
  1. **Heap Feng Shui** — shape the heap so the overflow hits a controllable object
  2. **Information Leak** — bypass ASLR by leaking libc/NGINX base address
  3. **Code Execution Primitive** — overwrite function pointer, free→use-after-free, or ROP chain

**Technique mapping:**
- **Fastbin poisoning** → if glibc malloc used for large object
- **Tcache poisoning** → if small allocations in same thread
- **House of Force** → top chunk overflow on old glibc
- **JIT / script engine spray** → if module embeds Lua, njs, or Perl

---

## Practical Case Study Template

Use this template when documenting a new CVE:

```markdown
## CVE-YYYY-NNNNN — Module/Fix
- **Affected Component:** [Module name]
- **CWE:** CWE-122 (Heap-based Buffer Overflow)
- **Trigger:** [HTTP request pattern, config condition]
- **Allocator:** [malloc, ngx_palloc, jemalloc, custom slab]
- **Overflow Target:** [Adjacent chunk, function pointer, metadata]
- **DoS Reliability:** [High/Medium/Low]
- **RCE Feasibility:** [None / Low / Medium / High]
- **ASLR Bypass:** [Yes — info leak needed / No — not required]
- **Detection:** [Network + Host indicators]
```

---

## Key References

- how2heap (glibc techniques adapted to server allocators)
- NGINX source: `src/http/modules/ngx_http_rewrite_module.c`
- Corelan/Heap overflow exploitation primers
- CVE-2026-42945 writeup (Akamai, itm4n methodology)

---

## Anti-Patterns to Avoid

- **Assuming** glibc heap primitives apply to jemalloc/slab (modern NGINX, Apache2)
- **Ignoring** custom pool allocators: they often lack safe-unlink and have deterministic layouts
- **Forgetting** worker restart: ASLR rerolls on fork/exec — useful for info-gathering, bad for reliable RCE
- **Underestimating** WAF/IPS: many already rewrite URL decoding; test with normalized vs. raw payloads
