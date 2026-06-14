---
name: toeplitz-summability-and-cesaro-means
title: Toeplitz Summability Theorem and Cesàro Means
description: Teach the Toeplitz/Silverman–Toeplitz summability theorem, including necessary and sufficient conditions for a matrix method to preserve convergent sequences, Cesàro means as a canonical example, monotonicity conditions, scope and limitations in sequence spaces, and instructional exercises in summability theory.
---

# Toeplitz Summability Theorem and Cesàro Means

## 1. Background intuition

A sequence (s_n) often fails to converge, but its averages may still approach a limit. The classical Cesàro mean is the oldest example:

C^1: σ_n = (s_0 + s_1 + · · · + s_n) / (n + 1)

If s_n → L, then σ_n → L. Conversely, σ_n → L does not guarantee s_n → L. This shows that Cesàro means are a “weaker” but still structured notion of convergence.

## 2. Matrix regularization viewpoint

Generalize by writing the transformed sequence σ as a matrix A = (a_{ij}):
σ_i = Σ_{j≥0} a_{ij} s_j

The method A is called **regular** if it preserves limits of convergent sequences. The Silverman–Toeplitz theorem gives the necessary and sufficient conditions.


## 3. Silverman–Toeplitz theorem

Let A = (a_{ij}) be an infinite real matrix. The following are equivalent:

1. **Regularity:** For every convergent real sequence s with limit L, the sequence σ given by σ_i = Σ_j a_{ij} s_j also converges to L.
2. **Toeplitz conditions:**
   - **Bounded row norm:** Σ_{j≥0} |a_{ij}| ≤ M for all i.
   - **Column convergence:** For every fixed j, lim_{i→∞} a_{ij} = 0.
   - **Row sum → 1:** lim_{i→∞} Σ_{j≥0} a_{ij} = 1.

**Proof idea for (ii) ⇒ (i):**
Let s_n → L. Write σ_i − L = Σ_j a_{ij} (s_j − L). Given ε > 0, split the sum into small j and large j. Boundedness controls the tail; column convergence kills off-diagonal terms for fixed j.

## 4. Cesàro means satisfy Toeplitz

For the Cesàro matrix C = (c_{ij}) defined by c_{ij} = 1/(i + 1) for j ≤ i and 0 otherwise:
- Row sum = 1.
- Each entry ≤ 1/(i + 1) → 0.
- The matrix is regular.

## 5. Monotone coefficient rigidity

For triangular Toeplitz-type methods with **monotone coefficients** a_{ij} ≥ a_{ij+1} for each i and j, and a_{ij} → 0, the condition Σ_j a_{ij} = 1 yields stronger control on mass distribution.

Informal statement: monotonicity limits how “leaky” the averaging can be. Without monotonicity, Toeplitz regularity permits “wild” rows that spread mass over high indices while still satisfying the three conditions.

## 6. Corollaries and extensions

- Cesàro summability (C,1) is regular, hence preserves limits.
- The iterated method (C,α) remains regular.
- A regular matrix need not be conservative on all bounded sequences; there exist bounded sequences not summable (C,1) but transformable by another regular method.
- For matrix methods preserving all bounded sequences rather than just convergent ones, stricter conditions are needed beyond standard Toeplitz.

## 7. Operational constraints

- Toeplitz conditions are necessary and sufficient for regular methods on convergent sequences.
- In algorithmic contexts, Toeplitz matrices are often banded or triangular; diagonal structure matters.
- Cesàro sums are useful where “convergence after smoothing” appears: discrete PDEs, numerical sequences, randomized rounding with finite-time averages.

## 8. Teaching exercises

1. Verify Toeplitz conditions for the r-means (Riemann) method R where r_{ij} = 1/2 for 0 ≤ j ≤ i, else 0.
2. Show that the moving average σ_i = (s_i + s_{i+1})/2 is regular.
3. Find a regular matrix that is not row-finite and explain why the proof still works.
4. Give an explicit divergent sequence whose Cesàro means converge to 1.
5. Prove that a regular matrix maps bounded sequences to bounded sequences.

## 9. Further reading

- Hardy, G. H. *Divergent Series*. Oxford, 1949.
- Zygmund, A. *Trigonometric Series*. Cambridge, 2002.
- Persson, L.-E. “The Toeplitz theorem on summability methods.”
- Wikipedia: Silverman–Toeplitz theorem, Cesàro summation.