---
name: probabilistic-method-intro
title: Probabilistic Method and Extremal Combinatorics
description: Master the probabilistic method in combinatorics including first-moment, second-moment, the Lovász Local Lemma, deletion method, and flag-algebra SDP bounds. Teaches both classical and modern algorithmic proof techniques.
depends_on:
  - graph-theory
  - probability
---

# Probabilistic Method and Extremal Combinatorics

Teaches the probabilistic method and its algorithmic applications. Covers both existential proofs and constructive algorithms, including the modern flag-algebra method for semi-definite programming bounds in extremal combinatorics.

---

## 1. The Probabilistic Method

### Core idea
To prove the existence of a combinatorial object satisfying a property, define a random object and show it satisfies the property with non-zero probability.

### Canonical template
1. Define a probability space Ω of objects.
2. Compute or bound `Pr[object has desired property]`.
3. Conclude object exists.

### Why it matters
It converts probabilistic intuition into rigorous non-constructive existence proofs, and modern variants guarantee efficient construction.

---

## 2. Classic Proofs

### Ramsey Numbers (upper bound)

**Theorem.** `R(k, k) ≤ 4^k`

- Randomly color edges of `K_n` with probability 1/2.
- Count monochromatic `K_k`'s.
- Expectation ≤ `n choose k / 2^{k-1}`.
- Set n = 4^k → expected < 1 → some coloring avoids monochromatic `K_k`.

### Turán's Theorem (unique extremal)

**Theorem.** `ex(n, K_r) ≤ (1 - 1/(r-1)) * n^2 / 2`

- Random graph `G(n, p)` on n vertices.
- Expected edges = `(n choose 2) * p`.
- Clique constraint forces p ~ 1/(n-1).
- Optimize to recover Turán bound.

### Matching in Bipartite Graphs (Häll's Marriage via Expectation)

**Theorem.** If every `S ⊆ L` satisfies `|N(S)| ≥ |S|`, perfect matching exists.

- Probabilistic proof via expectation of a random injection.

---

## 3. Second Moment + Chebyshev

### Threshold phenomena

**Definition.** `p_0(n)` is threshold for property `P` if:

- `p << p_0`: `Pr[P] → 0`
- `p >> p_0`: `Pr[P] → 1`

**Example.** `K_4`-free random graph `G(n, p)`:
- `X` = number of `K_4`'s.
- `E[X] = Θ(n^4 p^6)`
- `Var(X)` bounded via dependency graph.
- Chebyshev: `Pr[X=0] > 0` when `E[X]` small and variance controlled.

### Key insight
Variance requires dependency graph — vertices are copies of forbidden subgraph, adjacency = shared edges.

---

## 4. Lovász Local Lemma (LLL)

### The lemma

**Symmetric LLL.** Let `A_1, ..., A_m` be events with dependency graph `D` and each `Pr[A_i] ≤ p`. If:

```
ep(d+1) ≤ 1
```

then `Pr[∧ ¬A_i] > 0` (all bad events avoided).

**Asymmetric LLL.** `Pr[A_i] ≤ x_i * Π_{A_j ∈ D(A_i)} (1-x_j)` for some `x_i ∈ (0,1)`.

### Probabilistic Proof of LLL

Use induction + resampling argument to show:

`Pr[bad] ≤ Σ Pr[A_i] * small_factor < 1` when symmetric condition holds.

### Algorithmic LLL (Moser-Tardos)

**Theorem.** Under same conditions, resampling algorithm finds satisfying assignment in expected polynomial time.

```
Initialize all variables arbitrarily.
While some bad event A_i holds:
    uniformly resample all variables in A_i
```

**Key idea.** Expected resamples per event ≤ 1/(dependency-graph-degree). Total runs → expected `O(m)`.

---

## 5. Deletion Method

**Template.** Prove `G(n, p)` has property `P` with high probability:

1. Run `G_{n,p}`. Let `B` = bad events.
2. Remove one edge from each bad event.
3. Remaining graph retains `P` because bad events destroyed.
4. Bound: `E[remaining edges] = (n choose 2)p - E[number of bad events]`.

**Example.** Triangle-free graph with many edges.
- Start from `G(n, p)`.
- Delete one edge from each triangle.
- Remaining edges: `(n choose 2)p - E[triangles]`.
- Optimal p gives ~ `n^2/5` edges → improves naive bound of `n^2/4`.

---

## 6. Alteration Method

**Template.** Improve parameters on a random structure by post-processing.

**Example.**
- Random graph yields high independence number (almost `2 log_{1/(1-p)} n`).
- Delete vertices in independent sets.
- Get induced subgraph with independence exactly `α`.
- Amplifies small independence: if `α ≥ k` with prob > 0 → get induced subgraph.

---

## 7. Modern Tool: Flag Algebras

**Overview.** Razborov's flag-algebra method converts extremal combinatorics into a semi-definite programming (SDP) problem.

**Method.**
1. Enumerate small configurations ("flags").
2. Build convex combination bounds from Cauchy-Schwarz / flag algebra.
3. Reduce to finite SDP.
4. Solve numerically → get bounds (often tight).

**Strengths.**
- Handles forbidding multiple configurations simultaneously.
- Gives rigorous numerical bounds for open problems.

**Limitations.**
- Computationally heavy; enumerates flags combinatorially.
- Bounds may not be tight; proofs lack human insight.

**Example applications.**
- Bounds on `ex(n, {C_3, C_4})` and Ramsey numbers `R(3, t)`.
- Density of `C_5`-free and other graph families.
- 3-graph Turán densities.

---

## 8. Hypergraph Container Method

**Idea.** Instead of proving all independent sets small, construct containers `C_1, ..., C_m` covering all independent sets, each with small independence number `ℓ`.

**Template.**
1. Define hypergraph `H = (V, E)`.
2. Ordering + lemma: each independent set ⊆ some container.
3. Count containers: polynomial in `vol(E)`.

**Key theorem (independent sets in triangle-free graphs).**
`|I(G)| ≤ 2^{(1+o(1)) * n * Δ(G) / (2 log Δ(G))}` when `G` triangle-free and max degree `Δ`.

Proof via container + entropy method.

---

## 9. Entropy Method

### Shannon entropy recap
`H(X) = -Σ p(x) log p(x)`

### Subadditivity
`H(X, Y) = H(X) + H(Y|X) ≤ H(X) + H(Y)`

### Application: Counting independent sets in bounded-degree graphs

**Theorem (via entropy).** `|I(G)| ≤ 2^{(1+o(1)) * α(G)} * (some factor)`

Approach:
1. Sample independent set `X` from distribution.
2. `H(X) = H(X_1, ..., X_n)`.
3. Use `H(X_i | X_1, ..., X_{i-1}) ≤ log(1 + degree(i))`.
4. Sum gives log(|I|) ≤ `Σ log(1+deg(i))`.

---

## 10. Differential Method

**Idea.** Instead of discrete `A_n`, use `|A_n|`. Show `|A_{n+1}| ≤ f(|A_n|)`. Then iterate bound.

**Classic example.** Kővári–Sós–Turán (KST) theorem: `ex(n, K_{2,t}) ≤ O(n^{3/2})`.

**Proof sketch.**
1. Count ordered copies of `K_{2,t}`.
2. Fix pairs and count shared neighbors.
3. Sum over degrees: `Σ (d_i choose 2) ≥ n * (avg degree)^2`.
4. Solve quadratic → `O(n^{3/2})`.

---

## 11. Connections & Cross-Cutting Themes

- **Moment method** → concentration bounds → existence proofs
- **Alteration & deletion** → convert bounds to constructive statements
- **LLL/Moser-Tardos** → existence + algorithmic
- **Containers** → bounding independence numbers
- **Entropy** → unifies counting, compression, container proofs
- **Flag algebras** → SDP-based optimal extremal bounds

**Unifying principle:** Convert discrete existence questions into continuous optimization (entropy, Lovász extension, convex polytope faces, SDP relaxations).

---

## Exercises (Progressive)

### Level 1 — Warmup
1. Reconstruct `R(3,3)=6` and explain why `R(k,k) ≤ 4^k`.
2. Derive Turán's theorem using the probabilistic method.

### Level 2 — Technique drill
3. Show `K_n` has an orientation with no directed `K_3` for `n ≤ 5` and construct one for `n=7`.
4. Prove random `G(n, p)` has expected independence number ~ `2 log_{1/(1-p)} n`. Use alteration to bound suffices.
5. Apply LLL to vertex-coloring hypergraph avoiding monochromatic edges.

### Level 3 — Proof design
6. **Deletion method.** Write proof showing `G(n, c√n)` can be made triangle-free retaining `Θ(n^{3/2})` edges.
7. **Entropy bound for `K_{2,t}`-free graphs.** Derive `O(n √t)` via entropy.
8. **Container method sketch.** For 3-uniform hypergraph with each edge in ≤ `d` sets, bound `|I(H)|`.
9. **LLL algorithmic.** Implement Moser-Tardos for SAT satisfying LLL conditions.
10. **Flag algebra exercise.** Formulate SDP for 2-coloring to prove `R(4,4) > 17` numerically or cite known bound.

---

## Quick Reference Card

| Tool | When to Use | Complexity |
|---|---|---|
| First moment | Upper bound on object count | `O(1)` calc |
| Second moment + Chebyshev | Tight concentration, threshold | Variance estimation |
| Deletion method | Remove bad events to keep structure | Subtract `E[bad]` |
| Alteration | Modify random object to improve parameters | Extra modification |
| LLL | Avoid many rare bad events | `ep(d+1) ≤ 1` check |
| Moser-Tardos | Algorithmic LLL | Expected `O(m/d)` resamples |
| Containers | Bound independence number of hypergraph | Poly in `vol(E)` |
| Entropy | Counting, compression, asymptotic | `H(X) = …` |
| Differential | Recursive combinatorial bounds | Recurrence solve |
| Flag algebras | Multi-constraint extremal density | SDP solver |