---
name: sum-product-phenomena-and-conjecture
description: >
  Teach sum-product phenomena starting from the Erdős–Szemerédi conjecture and the
  sum-product conjecture, basic bounds in integers and reals, connections to incidence
  geometry, and the 2026 disproof over the real numbers by Bloom–Sawin–Schildkraut–Zhelezov
  (arXiv:2605.28781). Includes elementary proof sketches, exercises, and references.
  Use when studying additive combinatorics, incidence geometry, number theory, or
  theoretical CS.
---

# Sum-product phenomena and the sum-product conjecture

## 1. Basic definitions

For a finite set A in a ring:

- Sum set: A + A = {a + b : a, b in A}
- Product set: AA = {ab : a, b in A}
- k-fold sum/product sets: kA = A + ... + A, A^{(k)} = A * ... * A

## 2. Classical conjectures

- **Erdős–Szemerédi / sum-product conjecture (integers / reals):**
  For every finite set A in an ambient ring,
  max(|A+A|, |AA|) >= |A|^{2 - o(1)} as |A| -> infinity.

- **Many sums and products conjecture (Erdős):**
  For k >= 2 and any epsilon > 0,
  max(|kA|, |A^{(k)}|) >>_{k, epsilon} |A|^{k - epsilon}.

## 3. Prior lower bounds

- **Solymosi (2005):** |A+A|^2 |AA| >= |A|^{4 - o(1)} for reals.
- **Konyagin–Shkredov (multiple works), Cushman 2025:**
  max(|A+A|, |AA|) >= |A|^{4/3 + c - o(1)} with record c = 10/4407.
- **Rudnev–Shakan–Zhai, Rudnev–Worthington–Zhelezov, etc.:**
  refined polynomial-type lower bounds for low-degree polynomial images.

## 4. Connections to incidence geometry

- Elekes–Rónyai: large sum or product set follows from bounding
  |{ (a + b, ab) : a, b in A }| via Szemerédi–Trotter.
- Bourgain–Katz–Tao: finite field sum-product in prime fields => growth in matrix groups.
- Guth–Katz: point-line incidence bound (2015) underpins many improved sums-of-roots bounds.

## 5. The 2026 disproof over R

**Result:** There exists an absolute constant c > 0 and arbitrarily large finite
A subset R with
max(|A+A|, |AA|) <= |A|^{2 - c}.

**Counterexample sketch:** Use algebraic integers in a totally real number field K
of degree d ~ log |A| with small discriminant and controlled regulator.
Let A = G * P inside O_K where:
- G is the group of approximate multiplicative relations ("twisted" units).
- P is a small set of prime ideals.
Via bilinear form control on sums/products in Minkowski embeddings, both
A+A and AA grow like |A|^{2 - c}.

**Scope of disproof:** Theorems hold in:
- R
- Q_p
- Finite fields
- Function fields in positive characteristic

The integer case Z and bounded-degree number fields are **not** disproved; the
construction needs degree growing with |A|.

**Many sums and products:** For any fixed k, one gets
max(|kA|, |A^{(k)}|) <= |A|^{C log k / log log k},
showing the conjecture fails dramatically; the bound is near-optimal for some settings.

## 6. Quick teaching summary

**Takeaway:** Sum-product exponents below 2 exist in controlled algebraic settings,
but the landscape remains rich. Key conceptual tools:
1. Bilinear/partitioning methods (geometric)
2. Algebraic number theory embeddings (arithmetic)
3. Reduction to unit equations and regulator bounds

## 7. Exercises

1. Show directly from Solymosi's exchange argument that subsets of R with structure
   like {1,2,...,n} satisfy max(|A+A|,|AA|) = Theta(|A|^{4/3}).
2. Verify that A = {1, 2, 4, ..., 2^{n-1}} gives |A+A| approx 2n and |AA| approx n^2/2,
   so the product side dominates.
3. Prove that for A = {1,2,...,n}, the number of solutions to x + y = u + v with
   x,y,u,v in A is at least n^3 / 2 - O(n^2), implying at least one of A+A or AA
   is "large" in a very weak sense.

## 8. References and further reading

- T. F. Bloom, W. Sawin, C. Schildkraut, D. Zhelezov, *The sum-product conjecture is false for real numbers*, arXiv:2605.28781 (2026).
- M. B. Nathanson, *Additive Number Theory: Inverse Problems and the Geometry of Sumsets*, GTM 165.
- J. Bourgain, M. Z. Garaev, S. V. Konyagin, *Sum-product estimates via multiplicative energy*, various works 2004–2016.
- M. Rudnev and I. Shakan, *Polynomials and the sum-product phenomenon*, 2020 survey.
- T. Tao and V. Vu, *Additive Combinatorics*, Cambridge Univ. Press, 2006.
- MIT OCW 18.225, Lecture 26: Sum-product problem and incidence geometry (Terence Tao).
