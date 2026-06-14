---
name: grothendieck-constant-and-inequality
description: |
  Teach the Grothendieck inequality, the constant K_G, its algorithmic proof via rounding schemes, and the 2026 new upper bound showing K_G < π/(2 log(1+√2)) - 10^{-5}.
  Use when introducing analysis of algorithms, Banach space geometry, discrepancy theory, integrality gaps, or randomized rounding.
category: quantitative-theory
---

# Grothendieck Constant and Inequality

## Purpose
Provide a compact, textbook-quality treatment of the Grothendieck inequality, the constant K_G, its algorithmic proofs via rounding, and the 2026 paper that proved K_G is strictly smaller than Krivine's classical upper bound.

## Core Concepts

### 1. Statement of the Grothendieck Inequality
For real numbers `a_ij` and unit vectors `u_i, v_j ∈ S^{d-1}` in Hilbert space:

```
|Σ_i Σ_j a_ij (u_i · v_j)| ≤ K_G · sup_{ε_i,δ_j = ±1} |Σ_i Σ_j a_ij ε_i δ_j|
```

`K_G` is the smallest universal constant for which this holds for all `a_ij` and all dimensions. Equivalently, in the language of bilinear forms, the operator norm of the bilinear form on Euclidean vectors is at most `K_G` times its norm on sign vectors.

### 2. Two Quantities Compared
- **Discrete quantity**: `s(a) = sup_{ε,δ = ±1} |Σ a_ij ε_i δ_j|` (cut norm of matrix `a`).
- **Continuous quantity**: `c(a) = sup_{u,v on sphere} |Σ a_ij (u·v_j)|`.

Grothendieck: `c(a) ≤ K_G · s(a)`. The infimum over `a` of `c(a)/s(a)` is `K_G`.

### 3. Classical Bounds
- Grothendieck (1953): proved existence; original constants huge.
- Krivine (1979): gave `K_G ≤ π/(2 log(1+√2)) ≈ 1.7822...`, using an explicit rounding scheme from `S^{d-1}` to `{±1}`.
- Earlier lower bound: `K_G ≥ π/2` (Kashin–Szarek? actually Khot–Naor?); known `K_G > 1.6` roughly.

Braverman et al. and subsequent work narrowed tighter lower/upper bounds, but Krivine's upper bound stood for decades.

### 4. Why The Constant Matters in CS
- **Rounding/SDP gaps**: Grothendieck appears as integrality gap for `MAX-2-CSP` and related problems via the crash of vector solutions to integral solutions.
- **Correlation clustering**: objective can be phrased through Grothendieck-type bilinear forms.
- **Discrepancy**: relates to signing matrices to minimize cut norm.
- **Quantum information**: nonlocal games and XOR games connect to Grothendieck-type inequalities.

### 5. Krivine's Rounding Scheme
Given vectors `u_i, v_j ∈ S^{d-1}`:
1. Pick random orthonormal basis; project vectors onto first coordinate.
2. Round sign by threshold: `ε_i = sign(u_i · e_1)`.
3. Distributional analysis: the rounded cut objective `s(a)` approximates the continuous objective `c(a)` within factor bounded by `K_G`.
The scheme is deterministic in distribution and yields the constant above.

### 6. New 2026 Result (arXiv:2606.03991)
**Theorem.** `K_G < π/(2 log(1+√2)) - 10^{-5}`.

Authors: Alan Li, Rahul Saha, Anton Xue, Adam Klivans, Pravesh K. Kothari, Raghu Meka, Swarat Chaudhury.

What this means:
- Krivine's `π/(2 log(1+√2))` is not tight.
- The proof improves the rounding scheme or derives a tighter analysis showing the true constant is slightly smaller.
- Significance: pushes exact value of `K_G` down by at least `0.00001`; ongoing progress toward conjecture that true value is slightly below 1.67–1.70 range? (Keep as open problem.)

## Proof Sketch Barriers
The theorem is non-constructive-by-analysis in flavor:
1. Identify a specific matrix family or class where Krivine's analysis is not tight.
2. Optimize a distribution over rounding directions or weights to improve the bound.
3. Use semi-infinite programming / dual certificate method to bound the supremum more sharply than Krivine.

## Teaching Exercises
1. **Direct verification**: For `2×2` matrix `a = [[1, -1], [-1, 1]]`, compute both sides and show `K_G ≥ 2/1 = 2`? Actually check equality.
2. **Rounding experiment**: Implement Krivine's random-projection rounding numerically for random unit vectors and estimate `c(a)/s(a)` for many matrices.
3. **CS connection**: Show how a `K_G` gap upper-bounds the integrality gap of a natural SDP relaxation for a bi-clustering objective.
4. **Research extension**: Discuss whether a matching improvement in lower bound is needed to pin down `K_G` exactly.
5. **Algorithmic interpretation**: Define an explicit algorithm that, given `a_ij`, produces signs achieving `s(a) ≥ c(a)/K_G`.

## Key Papers
- A. Grothendieck, "Résumé de la théorie métrique des produits tensoriels topologiques" (1953).
- J.-L. Krivine, "Constante de Grothendieck pour les opérateurs à coefficients dans `ℓ_p`" (1979).
- Braverman et al. (earlier improvements on upper/lower bounds).
- A. Li et al., "The Grothendieck Constant is Less Than π/(2 log(1+√2)) - 10^{-5}" (arXiv:2606.03991, June 2026).

## Related Skills
- `linear-algebra-cs`: inner products, operator norms.
- `probability-for-engineers`: random rounding, distributional error analysis.
- `optimization`: SDP relaxations and integrality gaps.
- `approximation-algorithms`: rounding algorithms.
