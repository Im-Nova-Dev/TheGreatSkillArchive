---
name: quantum-time-lower-bounds
title: Quantum Time Lower Bounds via Permutation Invariance
description: >
  Teach the sample-to-time reduction framework for proving tight quantum time lower
  bounds on permutation-invariant properties of quantum states, including theorems for
  group-invariant embeddability, reductions, and canonical applications such as purity
  estimation, inner product estimation, and reflection-operator implementation.
tags:
  - quantum complexity
  - quantum time lower bounds
  - permutation invariance
  - sample complexity
  - quantum algorithms
  - quantum states
  - group invariant testing
---

# Quantum Time Lower Bounds via Permutation Invariance

Source: “Quantum Time Lower Bounds by Permutation Invariance”, Qisheng Wang,
arXiv:2606.05099v1, 03 Jun 2026.

## 1. Why quantum time is harder than sample/query complexity

For many tasks, sample complexity does not imply time complexity. For example,
state certification in $N$ dimensions has sample complexity
$\Theta(N/\varepsilon^2)$ but known time complexity
$\widetilde{O}(N^2/\varepsilon^5)$. The paper gives the first systematic framework
for tight quantum time lower bounds based on quantum sample complexity.

**Key definitions:**
- $T(P)$ — quantum time complexity (elementary gate count) for property $P$.
- $S(Q)$ — quantum sample complexity (number of copies needed) for property $Q$.
- Trivial baseline: $T(P_n) \ge S(P_n)$.

## 2. Core reduction theorems

### Theorem A: Fully permutation-invariant properties (Theorem 1.1 / 3.2)

If a 1-qubit property $\mathcal{Q}_1$ is embeddable in an $n$-qubit
permutation-invariant property $\mathcal{P}_n$, then

$$ T(\mathcal{P}_n) \ge n \cdot S(\mathcal{Q}_1) $$

This is an $n$-factor improvement over the trivial baseline.

### Theorem B: Partially permutation-invariant properties (Theorem 1.2 / 3.1)

Let $\mathcal{G} = \text{Sym}(A_1) \times \dots \times \text{Sym}(A_k) \le \text{Sym}(n)$
with $A_1, \dots, A_k$ partitioning $[n]$. If an $m$-qubit property $\mathcal{Q}_m$
is $\mathcal{G}$-invariantly embeddable in $\mathcal{P}_n$, then

$$ T(\mathcal{P}_n) \ge R \cdot S(\mathcal{Q}_m), \quad
   R = \min_{j \in [k]: A_j \cap [m] \ne \emptyset} \left\lfloor \frac{|A_j|}{|A_j \cap [m]|} \right\rfloor $$

Theorem A is the special case $m=k=1, A_1=[n] \Rightarrow R=n$.

**Important remark:** These $n$-factor lower bounds require permutation/group invariance.
For non-invariant properties, the time-to-sample ratio can be polylog$(n)$ or constant.

### Qudit generalization (Theorems 3.3, 3.4)

Both theorems extend to $d$-level qudit systems without changing the lower-bound form.

## 3. Tightness and canonical applications

Combining the sample-to-time reductions with known optimal sample complexities gives
exact time bounds; all stated lower bounds are matched by known algorithms.

| Task | Lower bound | Optimal algorithm | Time / Samples |
|------|-------------|-------------------|----------------|
| Purity estimation $\text{tr}(\rho^2)$ | $\Omega(n/\varepsilon^2)$ | SWAP test | $O(n/\varepsilon^2)$ / $O(1/\varepsilon^2)$ |
| Purity testing | $\Omega(n/\varepsilon)$ | SWAP test | $O(n/\varepsilon)$ / $O(1/\varepsilon)$ |
| Inner product estimation | $\Omega(n/\varepsilon^2)$ | SWAP test | $O(n/\varepsilon^2)$ / $O(1/\varepsilon^2)$ |
| High-order power trace $\text{tr}(\rho^k), k\ge3$ | $\Omega(nk/\varepsilon^2)$ | Shift test | $O(nk/\varepsilon^2)$ / $O(k/\varepsilon^2)$ |
| Multipartite productness testing | $\Omega(nm/\varepsilon^2)$ | Harrow–Montanaro | $O(nm/\varepsilon^2)$ / $O(1/\varepsilon^2)$ |
| Reflection $e^{-i\rho t}$ for pure $\rho$ | $\Omega(n/\delta)$ | LMR protocol | $O(n/\delta)$ / $O(1/\delta)$ |
| Samplizer | $\Omega(nQ^2/\delta)$ | Wang–Zhang samplizer | $\widetilde{O}(nQ^2/\delta)$ / $\widetilde{O}(Q^2/\delta)$ |
| Pure-state trace distance / fidelity | $\Omega(n/\varepsilon^2)$ | Wang–Zhang estimator | $O(n/\varepsilon^2)$ / $O(1/\varepsilon^2)$ |

## 4. Intuition and assumptions

- **Main source of hardness:** A permutation-invariant property of $n$ objects
  can only depend on the multiset, not on any individual component. Querying $O(1)$
  copies is therefore insufficient to learn $O(n)$ distinguishable parameters, forcing
  either $n$ times more samples or $n$ times more time.
- **Embeddability requirement:** The smaller property must embed into the invariant
  structure. This is often satisfied by restricting the large property to a subspace
  spanned by $m$ qudits arranged with only $A_j$ symmetry.
- **Technique:** “Derandomization” sample lower bounds via symmetry, then lifting the
  resulting information-theoretic barrier to time via the reduction theorems.

## 5. Teaching exercises

1. **Reduction walkthrough:** For $n$-qubit purity estimation $\text{tr}(\rho^2)$,
   show why the 1-qubit purity property embeddably captures the global property, and
   derive the $n$ factor in the lower bound.
2. **Partial invariance:** Take $n=6$, partition $[6]=\{1,2\}\cup\{3,4,5\}\cup\{6\}$,
   $m=1$, and compute $R$ for each block intersecting $[m]$.
3. **Noninvariant counterexample:** Explain why entangled states whose time–sample
   ratio is polylog$(n)$ break the reduction argument.
4. **Connection to known results:** Explain why this framework unifies lower bounds for
   purity testing, inner product estimation, and the Wang–Zhang samplizer.

## 6. Key implications

- Unifies several quantum subfield lower bounds under one symmetry-based method.
- Provides the first systematic answer to “tight quantum time lower bounds.”
- Open question: extend beyond permutation-invariant properties to broader group
  families, such as weakly symmetric states, and further collapse the gap between time
  and sample complexity for non-invariant tasks.
