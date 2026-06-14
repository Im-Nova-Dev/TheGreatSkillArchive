---
name: permanent-range-superpolynomial-bound
description: >
  Teach the 2025 superpolynomial lower bound on the range of the permanent function
  on n×n (±1)-matrices (Ingram–Razborov, arXiv:2507.09433). Covers determinant vs permanent,
  the state of the art before the result, additive-combinatorics core ideas (GAPs,
  bounded monomial maps, Diophantine controls), the theorem statement and proof strategy,
  and why this matters for combinatorics, complexity theory, and quantum computing.
trigger:
  - "permanent range"
  - "superpolynomial lower bound permanent"
  - "Additive combinatorics permanent"
  - "Ingram Razborov permanent"
audience: advanced undergrad/grad students in combinatorics, complexity, or quantum info.
---

# Superpolynomial Range of the Permanent on ±1-Matrices

## 1. The Two Definitions
For M = (a_{i,j}) ∈ ℝ^{n×n}:
- **Determinant:** det(M) = Σ_{σ∈S_n} sign(σ) Π_i a_{i,σ(i)}.
- **Permanent:** per(M) = Σ_{σ∈S_n} Π_i a_{i,σ(i)} (sign dropped).
  
Consequence: det(M) can be computed in poly(n), per(M) is #P-hard. Yet both are “just” sums over permutations.

## 2. Existing Bounds for 0–1 vs ±1
- For 0–1 matrices, permanent is monotone in entries, so local changes produce step-like controls. It is classical that range size = n! (exponential).
- For (±1)-matrices, non-monotonicity destroys simple controls. Until 2025, the best lower bound was **n + 1**.

## 3. Main Result (Theorem 2, Ingram–Razborov 2025)
Authoritative form: let

  r_n = |{per(M) : M ∈ {−1,+1}^{n×n}}|.

Then

  r_n ≥ n^{Ω(log n / log log n)}.

This is the first *superpolynomial* lower bound for (±1)-permanent range.

## 4. Proof Strategy
### 4.1 Fixed Row Count k
Study r_{k,n} = |{per(A) : A ∈ Ω_{k,n}}| for k×n matrices. Because
per(A * J_{(ℓ−k),n}) = per(A) · (n − k)^{ℓ−k}, r_{k,n} monotone in k.

### 4.2 Generalized Arithmetic Progressions (GAPs)
A GAP of dimension d is a set of integer linear combinations of basis vectors

  P ={x_0 + Σ_{i=1}^d ℓ_i x_i : 0 ≤ ℓ_i < L_i}.

A key fact: {per(A * J_{m,n}) : A with a fixed k-row pattern} sits inside a
proper GAP of dimension O(k).

### 4.3 Bounded Monomial Map
Write per(A) = Σ_{σ∈S_{k,n}} sign(σ) Π_i Π_j a_{i,j} with injective columns.
The product is a monomial in entries of A; its coefficients depend only on A.
Using the algebraic structure of elementary symmetric polynomials in rows,
Ingram–Razorov build a **bounded monomial map** whose image lives in a
proper GAP of controlled dimension and size.

### 4.4 Lower Bound on Size
They construct an explicit probability distribution μ on [k] with rational
weights and show that the support of μ yields distinct values of per(A) for
infinitely many n via Diophantine approximation, giving:

  r_{k,n} ≥ ε_k n^{k−2}  (Theorem 1).

Taking k → ∞ slowly in n gives Theorem 2.

## 5. Why This Matters
- **Complexity:** Understanding the valuation/range of the permanent feeds into
  lower-bound questions; richer range resists polynomial approximations.
- **Quantum computing:** BosonSampling outputs statistics based on |per(U)|²,
  so range behavior connects to anticoncentration.
- **Additive combinatorics:** The paper gives a concrete application of GAP
  theory inside an algebraic complexity question.

## 6. Teaching Flow
1. Define determinant/permanent on 2×2, 3×3; discuss computational hardness.
2. Compare range monotonicity for 0–1 vs ±1 via “sign-flip examples.”
3. State Theorem 2; work through the r_{k,n} → r_n idea.
4. Define generalized arithmetic progressions.
5. Use small k to show how a row-pattern table yields polynomial-size range.
6. Explain Diophantine control via rational distributions μ.
7. Discuss implications for quantum anticoncentration.

## 7. Exercises
1. For k = 2, show that r_{2,n} ≥ c n for a concrete constant c > 0.
2. Prove that when ℓ ≥ k, per(A * J_{(ℓ−k),n}) = per(A) · (n − k)^{ℓ−k}.
3. Show why a proper GAP of dimension d and length L_1···L_d has size L_1···L_d.
4. Verify that permuting rows or negating a row flips sign of the permanent,
  but range size is unchanged.
5. Why does adding a row of all +1s produce the scaling in exercise 2?

## 8. References
- D. Ingram, A. Razborov, *On the Range of the Permanent of (±1)-Matrices*,
  arXiv:2507.09433 [math.CO], 2025.
- R. Kenney and C. Zmada, classical n! bound via monotonicity for 0–1.
- S. Krauter, prior best n + 1 bound.
- T. Tao, notes on bosonSampling and anticoncentration for permanent distributions.
