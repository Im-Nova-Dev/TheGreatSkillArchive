---
title: Erdős Unit Distance Problem Disproof (2026)
description: >
  Teach the Erdős unit distance conjecture, its 2026 disproof by an OpenAI
  model (algebraic number theory + geometry), related sum-product breakthrough,
  and the emerging role of AI in settling long-open extremal combinatorics problems.
  Covers historical bounds, key constants, proof structure, and implications.
category: university-cs
audience: advanced undergraduates, graduate students, theory researchers
prerequisites:
  - Basic combinatorial geometry (extremal point sets)
  - Familiarity with probabilistic method basics
  - Elementary algebraic number theory (field embeddings, ring of integers) helpful
---

# Erdős Unit Distance Problem Disproof (2026)

## 1. The Original Problem (1946)

**Definition.** For a set \( S \subset \mathbb{R}^2 \) of \( n \) points, let
\( u(S) \) be the number of pairs at **unit distance**.

**Conjecture (Erdős, 1946).**
\[
u(S) = O\bigl(n^{1+\epsilon}\bigr)
\]
for every \( \epsilon > 0 \). Erdős believed the true maximum is
\( n^{1+o(1)} \). He also conjectured the precise leading constant:
\[
u(S) \le n^{1 + c/\log\log n}
\]
for some absolute \( c > 0 \).

**Best known upper bound before 2026:**
\[
u(S) = O\bigl(n^{4/3}\bigr)
\]
(Spencer, Szemerédi, Trotter — uses crossing number / cell-crossing method).

**Motivation.** Erdős also posed the related **distinct distances problem** (minimum
number of distinct distances determined by \( n \) points). Guth & Katz (2010)
proved a near-tight lower bound of \( \Omega(n/\log n) \); the conjectured order
is \( n/\sqrt{\log n} \). The unit distance problem is its “dual” extremal
variant and remained open for 80 years.

---

## 2. The 2026 Disproof

### Result
An OpenAI model constructed an explicit point set with
\[
u(S) \ge n^{1+\epsilon}
\]
for an explicit \( \epsilon > 0 \), disproving the upper-conjecture in its
strongest form.

### Key Constants (as of mid-2026)
- Will Sawin independently first proved \( n^{1.014} \).
- Later improvements reached \( n^{1.0318} \) (Sawin et al.).
- The new algebraic-number-theoretic method has a proven theoretical
  upper limit of about \( 1.2143 \); current constructions fall well below this cap.

### Technical Ingredients

1. **Algebraic number theory core.** The counterexample uses a lattice tied to
   the ring of integers \( \mathbb{Z}[\sqrt{D}] \) in a real quadratic field
   \( \mathbb{Q}(\sqrt{D}) \). The norm form
   \[
   N(x + y\sqrt{D}) = x^2 - Dy^2
   \]
   produces many pairs with \( N = 1 \), which then embed into the plane via the
   map \( (x,y) \mapsto (x + y\sqrt{D},\, xy) \) (or similar projection).

2. **Error term tuning.** Earlier constructions heavily used the geometry of
   numbers (Minkowski’s theorem), which only gives \( O(n^{1+o(1)}) \) bounds.
   The breakthrough was recognizing that both \( x^2 - Dy^2 \) **and**
   \( x^2 - D' y^2 \) can simultaneously equal 1 by choosing a second norm form
   tied to the fundamental unit. Counting solutions uses a double-application of
   the Chebotarev density theorem to guarantee many primes splitting completely,
   allowing the Chinese remainder theorem to build many paired residues.

3. **Connection to unit equations.** A unit on the line corresponding to a point
   in the set arises as a solution to a **S-unit equation**
   \[
   u + v = 1, \qquad u,v \in \mathcal{O}_K^\times
   \]
   in the unit group of the ring of integers. Counting such solutions in thin
   sets is done via the **A-step Baker–Stroeker–van der Poorten** method,
   generalized by adding a second coordinate giving the second unit equation.
   The combined system \( u_1+v_1=1 \) and
   \( u_2+v_2=1 \) gives two independent “unit coincidences,” producing the
   \( n^{1+\epsilon} \) explosion.

4. **Optimization over constants.** The AI component primarily searched over
   quadratic fields \( \mathbb{Q}(\sqrt{D}) \) and coefficient choices to
   maximize the exponent \( 1+\epsilon \). The human/machine collaboration
   provided the algebraic framework; the AI performed the constant optimization
   and found that certain small discriminants (e.g., \( D=61 \)) give better
   exponents than previously tested fields.

### Related Breakthrough: Erdős–Szemerédi Sum-Product
Motivated by the unit-distance work, Bloom, Sawin, Schildkraut & Zhelezov
disproved the **Erdős–Szemerédi sum-product conjecture over the reals**
(2026). Both results show that rigid arithmetic structures can survive in
continuous Euclidean spaces at scales larger than previously believed.

---

## 3. Proof Skeleton (Teaching Version)

> Goal: exhibit \( n \) points with \( \gtrsim n^{1.03} \) unit distances.

1. **Choose a real quadratic field** \( K = \mathbb{Q}(\sqrt{D}) \) with class
   number 1 and fundamental unit \( \varepsilon > 1 \).
2. **Define the point set** by embedding norms:
   \[
   S = \{ (N_{K/\mathbb{Q}}(\alpha_i), \operatorname{Tr}_{K/\mathbb{Q}}(\alpha_i))
         : \alpha_i \in \mathcal{O}_K,\ |N(\alpha_i)| \le X \}.
   \]
3. **Count unit-distance pairs.** Two points \( \alpha,\beta \) are at unit
   distance whenever \( N(\alpha-\beta)=1 \). Counting such pairs reduces
   to counting representations of 1 as a difference of two norms, i.e., a
   system of Pell-type equations.
4. **Lower bound via character sums.** Using the Weil bound for Jacobi sums
   and the fact that \( D \) is a sum of two squares in many ways, show that
   the representation count grows like \( X^{1+\delta} \) for some
   \( \delta > 0 \).
5. **Relate \( X \) to \( n \).** The set has \( n \asymp X \), so
   \( u(S) \gtrsim n^{1+\delta} \).

---

## 4. Connections & Implications

- **AI in pure math.** The result is one of the first settled open problems
  where AI provided the explicit extremal construction. The task is
  *construction*, not just pattern recognition, suggesting AI can contribute to
  existence proofs in extremal combinatorics.
- **Extremal combinatorics.** The unit distance problem sits at the boundary of
  discrete geometry, additive combinatorics, and number theory. A disproof at
  \( n^{1+\epsilon} \) does not resolve the exact extremal function but
  dramatically shifts where the boundary lies.
- **Future directions.** Can the exponent be pushed toward the theoretical cap
  \( \approx 1.2143 \)? Are there analogous constructions giving superlinear
  counts of equal areas, equal angles, or repeated distances in dimensions \( d>2 \)?

---

## 5. Teaching Prompts / Checks

1. **Conceptual.** Why does the crossing-number method in computational
   geometry naturally produce \( O(n^{4/3}) \) but not \( n^{1+\epsilon} \)
   counterexamples?
2. **Technical.** Explain why having *two* independent unit equations
   (rather than one) is the key to increasing the exponent.
3. **AI literacy.** What portion of the result is “AI” vs. “classical math”?
   Is the AI contribution optimization, conjecture generation, or formal proof?
4. **Research design.** Propose an experimental search strategy (Python/Sage)
   to find small-\( D \) quadratic fields with the best exponents.

---

## 6. References

1. **OpenAI official announcement (2026).**
   https://openai.com/index/model-disproves-discrete-geometry-conjecture/
2. **Technical proof paper (OpenAI, 2026).**
   https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf
3. **Discussion / write-up (Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Matchett Wood, 2026).**
   (see OpenAI PDF references)
4. **Terence Tao constants page:**
   https://teorth.github.io/optimizationproblems/constants/84a.html
5. **Erdős-Szemerédi disproof (Bloom, Sawin, Schildkraut, Zhelezov, 2026).**
   arXiv preprint
6. **Gil Kalai blog summary (May 21, 2026):**
   https://gilkalai.wordpress.com/
