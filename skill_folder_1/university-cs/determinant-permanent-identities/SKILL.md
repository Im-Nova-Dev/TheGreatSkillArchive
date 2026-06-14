---
name: determinant-permanent-identities
title: Determinant and Permanent Identities
description: >
  Teach the determinant and permanent of matrices, algebraic identities,
  combinatorial interpretations, and recent results connecting them to number
  theory and combinatorics, with emphasis on proof techniques and teaching
  exercises.
tags:
  - determinants
  - permanents
  - matrix identities
  - combinatorics
  - algebraic proofs
  - number theory
  - matrix polynomial methods
---

# Determinant and Permanent Identities

Source/signal: recent arXiv listing points to “Some new results on determinants
and permanents”, Bo Jiang, Zhi-Wei Sun, arXiv:2606.03970 (Number Theory /
Combinatorics, 3 Jun 2026).

## 1. Definitions

For an $n \\times n$ matrix $A = (a_{ij})$:

- **Determinant**:
  $$
  \\det(A) = \\sum_{\\sigma \\in S_n} \\operatorname{sgn}(\\sigma)
  \\prod_{i=1}^{n} a_{i,\\sigma(i)}
  $$

- **Permanent**:
  $$
  \\operatorname{per}(A) = \\sum_{\\sigma \\in S_n}
  \\prod_{i=1}^{n} a_{i,\\sigma(i)}
  $$

Same product-sum structure, but permanent drops the sign. That small change has
dramatic algorithmic and combinatorial consequences:

- $\\det(A)$ is in $\\text{NC}^2$; computing $\\operatorname{per}(A)$ mod 2 is
  $\\text{NP}$-hard in general.
- $\\det(A)$ has a geometric meaning (volume scaling).
- $\\operatorname{per}(A)$ enumerates structures: perfect matchings, assignments,
  and many combinatorial objects.

## 2. Basic algebraic identities

These are reusable proof tools. Each proof sharpens “row-column homomorphism”
versus “pairing” thinking.

**Row/column linearity**
- $\\det(\\cdot)$ is multilinear and alternating in rows (and columns).
- $\\operatorname{per}(\\cdot)$ is multilinear but not alternating.

**Transpose invariance**
- $\\det(A) = \\det(A^T)$ and $\\operatorname{per}(A) = \\operatorname{per}(A^T)$.

**Multiplicativity**
- $\\det(AB) = \\det(A)\\det(B)$.
- No exact multiplicative identity for permanent; only bounds and special cases.

**Block matrices and Schur complement (determinant)**
If
$$
A = \\begin{pmatrix} B & C \\\\ D & E \\end{pmatrix}
$$
and $E$ is invertible, then
$$
\\det(A) = \\det(E)\\ \\det(B - C E^{-1} D).
$$

This is a standard determinant proof technique and bridges linear algebra,
matrix factorizations, and algorithmic preconditioning.

**Cauchy–Binet**
For $A$ ($m \\times n$) and $B$ ($n \\times m$) with $m \\le n$:
$$
\\det(AB) = \\sum_{S \\subseteq [n],\\ |S|=m}
\\det(A_{:,S})\\ \\det(B_{S,:}).
$$
Useful for understanding how rank and subdeterminants compose.

**Combinatorial interpretation of permanent**
- For $0$-$1$ matrices, $\\operatorname{per}(A)$ counts permutation matrices
  $\\le A$, i.e., perfect matchings in the bipartite graph defined by $A$.
- Generalizes to weighted counting problems over bijections and factorizations in
  combinatorial species.

## 3. Connections to number theory and combinatorics

Determinants and permanents appear naturally when:

- Counting lattice points and volumes (Minkowski determinants).
- Studying Ramanujan-type identities and permanents of $(0,1)$-matrices.
- Exploring sign-balance, combinatorial congruences, and combinatorial designs.
- Analyzing binary matrix families via “tempered” permanents or signed combos.

Many classical reductions rewrite sums over subsets or permutations as matrix
polynomials, so identities become technical levers for proving congruences,
inequalities, or new binomial-sum evaluations.

## 4. Proof ideas to internalize

1. **Induction + cofactor expansion**
   The engine of many determinant evaluations. Often the cleanest path when the
   matrix is structured: Toeplitz, Hankel, tridiagonal, or Vandermonde-like.

2. **Row operations and change of basis**
   Determinants transform mostly predictably under elementary row operations:
   - swap rows: multiply by $-1$
   - scale row: multiply determinant by that scalar
   - add row to another: determinant unchanged
   This turns hard matrices into triangular/LU form efficiently.

3. **Column-row symmetry + combinatorial bijections**
   For permanents of $(0,1)$-matrices, map permanent terms to
   combinatorial objects and reorganize the sum. Common technique:
   inclusion–exclusion, sign-reversing involutions, or convolution identities.

4. **Schur complement for recursive block evaluation**
   Great for problem types with repeated substructure, often yielding closed
   forms or asymptotics.

5. **Cauchy–Binet for rank insight**
   Use to understand when rank drops, for determinant formulas involving minors,
   and for relating complex product matrices to submatrix determinants.

## 5. Teaching exercises

1. **Cofactor exploration**
   Evaluate
   $$
   \\begin{vmatrix}
   1 & 1 & 1 \\\\
   1 & 2 & 3 \\\\
   1 & 3 & 6
   \\end{vmatrix}
   $$
   and the permanent of the same matrix. Identify exactly which terms cancel
   in the determinant but remain in the permanent.

2. **LU intuition**
   For a lower-triangular $L$ and upper-triangular $U$, compute
   $\\det(LU)$ by hand. Show how pivoting changes the sign and why this gives an
   $O(n^3)$ determinant algorithm.

3. **Permanent counting**
   For the $n \\times n$ matrix of all ones, compute $\\operatorname{per}(J_n)$.
   Explain why this counts permutations and why $n!$ growth matters for
   complexity.

4. **Schur complement practice**
   For block matrix
   $$
   \\begin{pmatrix}
   A & B \\\\
   C & D
   \\end{pmatrix},
   $$
   with $D$ invertible, write out $\\det$ in terms of $\\det(D)$ and Schur
   complement. Then specialize to a numeric $2 \\times 2$ block and verify.

5. **Cauchy–Binet worked example**
   Take $A = \\begin{pmatrix}1 & 2 \\\\ 3 & 4 \\end{pmatrix}$ and compute
   $\\det(A A^T)$ using Cauchy–Binet. Check that it matches $\\det(A)^2$
   directly.

6. **Research-style exercise**
   Read the arXiv:2606.03970 abstract and identify one main theme used to
   derive new determinant or permanent congruences. Write two-sentence summary
   of the technique and one open-ended follow-up question.

## 6. Key implications

- Determinant identities generalize from scalars to rings, polynomial matrices,
  and matrix polynomials; permanent identities often need stronger conditions.
- Many contest and research proofs rely on switching between $\\det$ and
  $\\operatorname{per}$ by sign-reversing or by truncating the signed sum.
- For complexity theorists, the determinant–permanent dichotomy is a central
  organizing theme in algebraic complexity.
- For number theorists, perm/determinant evaluations and congruences are active
  tools in extremal and arithmetic combinatorics.
