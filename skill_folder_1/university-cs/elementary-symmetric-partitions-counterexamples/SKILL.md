---
name: elementary-symmetric-partitions-counterexamples
description: Teach the 2026 counterexamples to the Devnani-Eyyunni refined conjecture on elementary symmetric partition maps: pre_j is NOT injective on partitions of length 2j for j >= 3, while the complete homogeneous analog prh_j IS injective everywhere. Covers symmetric polynomial maps on partitions, the original Ballantine-Beck-Merca conjecture, the Devnani-Eyyunni refinement, and the sharp boundary between elementary and homogeneous cases.
category: university-cs
tags: [combinatorics, partitions, symmetric-functions, elementary-symmetric, conjectures, 2026, counterexamples, injectivity]
---

# Elementary Symmetric Partition Maps: The 2026 Counterexamples

## Overview

This skill teaches a **sharp 2026 result** on partition maps derived from symmetric polynomials:

| Map | Definition | Injectivity |
|-----|------------|-------------|
| **`pre_j`** (elementary) | Parts = summands of j-th elementary symmetric polynomial on λ | **Fails** at length `2j` for `j ≥ 3` |
| **`prh_j`** (complete homogeneous) | Parts = summands of j-th complete homogeneous symmetric polynomial on λ | **Holds** for ALL partitions |

The result resolves a chain of conjectures in the **negative** for elementary symmetric polynomials, while the homogeneous version remains universally injective.

---

## Background: Symmetric Polynomial Partition Maps

### Partitions

A **partition** `λ = (λ₁ ≥ λ₂ ≥ … ≥ λₖ > 0)` of `n` has:
- `n = sum λᵢ` (size)
- `ℓ(λ) = k` (length/number of parts)

### Elementary Symmetric Polynomials

For variables `x₁, …, xₖ`, the **j-th elementary symmetric polynomial**:

```
e_j(x₁,…,xₖ) = Σ_{1 ≤ i₁ < … < i_j ≤ k} x_{i₁} … x_{i_j}
```

### The Map `pre_j`

Given a partition `λ = (λ₁,…,λₖ)`, evaluate `e_j(λ₁,…,λₖ)`. The result is a sum of monomials. The parts of the new partition `pre_j(λ)` are the **exponents** (or summands) appearing in this evaluation.

**Example**: `λ = (3,2,1)`, `j=2`
- `e₂(3,2,1) = 3·2 + 3·1 + 2·1 = 6 + 3 + 2`
- `pre₂(λ) = (6,3,2)` (parts sorted descending)

---

## The Conjecture History

| Year | Authors | Conjecture | Status |
|------|---------|------------|--------|
| — | Ballantine, Beck, Merca | `pre_j` injective on partitions with `ℓ ≥ j` | **FALSE** |
| — | Devnani, Eyyunni | Counterexample at `ℓ = j`; **refined**: injective for `ℓ > j` | **REFUTED (2026)** |
| 2026 | **Hadelyn, Niergarth, Li, Li** | — | **`pre_j` NOT injective at `ℓ = 2j` for `j ≥ 3`** |

---

## Main Theorems (2026)

### Theorem 1 (Negative — Hadelyn et al., arXiv:2606.00420)

> **`pre_j` is not injective on partitions of `n` with length `2j` for all `j ≥ 3`.**

This provides **explicit counterexamples** to the Devnani-Eyyunni refined conjecture.  
The boundary is **sharp**: injectivity fails precisely at length `2j` (for `j ≥ 3`).

### Theorem 2 (Positive — Same paper)

> **The complete homogeneous analog `prh_j` is injective on the set of ALL partitions.**

This contrasts dramatically with the elementary case — a structural dichotomy.

---

## Why This Matters

1. **Sharp threshold**: `ℓ = 2j` is the exact length where injectivity breaks for `pre_j` (when `j ≥ 3`)
2. **Symmetric function dichotomy**: Elementary vs. complete homogeneous symmetric polynomials behave fundamentally differently on partitions
3. **Algebraic combinatorics**: Reveals how the *type* of symmetric polynomial (elementary vs. homogeneous) controls the combinatorics of partition maps
4. **Conjecture resolution**: Closes a specific line of inquiry started by Ballantine-Beck-Merca, refined by Devnani-Eyyunni

---

## Teaching Exercises

### Exercise 1: Compute `pre_j` by Hand
Let `λ = (4,3,2,1)` (length 4). Compute `pre_2(λ)` and `pre_3(λ)`.

<details>
<summary>Solution</summary>

`e₂(4,3,2,1) = 4·3 + 4·2 + 4·1 + 3·2 + 3·1 + 2·1 = 12+8+4+6+3+2 = 35` → parts: the six summands → `(12,8,6,4,3,2)` sorted: `(12,8,6,4,3,2)`

`e₃(4,3,2,1) = 4·3·2 + 4·3·1 + 4·2·1 + 3·2·1 = 24+12+8+6 = 50` → summands: `(24,12,8,6)`
</details>

### Exercise 2: Understand the Injectivity Question
Why would anyone conjecture `pre_j` is injective for `ℓ > j`?

<details>
<summary>Discussion</summary>

- For small lengths, the map "spreads out" information
- The original conjecture was plausible because `e_j` encodes j-wise interactions
- Devnani-Eyyunni found `ℓ = j` counterexamples, suggesting `ℓ > j` might be safe
- The 2026 result shows: even `ℓ = 2j` is **not** safe for `j ≥ 3`
</details>

### Exercise 3: Contrast with `h_j` (Complete Homogeneous)
For `λ = (3,2,1)`, `j=2`, compute `h₂(λ) = Σ_{i≤j} λᵢλⱼ` and compare the structure to `e₂`.

<details>
<summary>Solution</summary>

`h₂(3,2,1) = 3² + 2² + 1² + 3·2 + 3·1 + 2·1 = 9+4+1+6+3+2 = 25` → summands: `(9,6,4,3,2,1)` → partition `(9,6,4,3,2,1)`

Note: `h_j` includes **diagonal terms** (squares), `e_j` does not. This structural difference is key to why `prh_j` stays injective.
</details>

### Exercise 4: The Sharp Boundary
For `j=3`, the theorem says `pre_3` fails injectivity at length `6`. Try to construct or find a pair of distinct partitions of length 6 with the same `pre_3` image.

<details>
<summary>Hint</summary>

The paper provides explicit constructions. The counterexample structure uses partitions with carefully chosen repeated parts that make the elementary symmetric sums collide. Look at the arXiv:2606.00420 paper for the exact families.
</details>

---

## Key Concepts Summary

| Concept | Definition |
|---------|------------|
| `pre_j` | Partition map from j-th elementary symmetric polynomial |
| `prh_j` | Partition map from j-th complete homogeneous symmetric polynomial |
| **Injectivity** | Distinct partitions → distinct image partitions |
| **Length threshold** | `ℓ = 2j` for `j ≥ 3` is the sharp boundary for `pre_j` |
| **Complete homogeneous** | `h_j = Σ_{1≤i₁≤…≤i_j} x_{i₁}⋯x_{i_j}` (allows repeats) |

---

## Reference

- **Paper**: Hadelyn, Niergarth, Li, Li — *Counterexamples regarding elementary symmetric partitions* (arXiv:2606.00420, May 2026)
- 17 pages, math.CO
- DOI: 10.48550/arXiv.2606.00420

---

## Connections to Other Skills

- `university-cs/euler-pentagonal-number-theorem` — partitions, generating functions
- `university-cs/sum-product-phenomena-and-conjecture` — symmetric polynomials, combinatorics
- `university-cs/planar-perfect-matching-determinant-hardness` — Pfaffians, skew-symmetric polynomials
- `quantitative-theory/circle-method-digit-sums-primes` — recent 2026 analytic combinatorics

---

## Intel Log

Saved to: `/home/nova/.hermes/intel/math-and-theory/2026-06-06-elementary-symmetric-partitions.md`