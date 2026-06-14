name: cheeger-inequality-and-spectral-sparsification
description: Teach Cheeger's inequality, spectral sparsification for graphs and CSPs, connections between analytic and combinatorial expansion, and recent spectral CSP sparsification results with compact exercises and proof sketches.
category: university-cs
tags: [linear-algebra, probability, graph-theory, spectral-methods, expansion]

# Cheeger's Inequality and Spectral Sparsification

## Purpose
Provide a compact, high-quality teaching resource connecting:
1. Graph Laplacians and Rayleigh quotients.
2. Cheeger's inequality: algebraic ↔ combinatorial expansion.
3. Spectral graph sparsifiers: Spielman-Srivastava effective-resistance sampling.
4. Spectral CSP sparsification: extending spectral methods to constraint satisfaction.
5. Example-driven exercises showing why spectra capture global structure.

Target audience: advanced undergrad/grad CS theory; algorithms and discrete math researchers.

---

## 1. Key Concepts

### 1.1 Graphs and Laplacians
- Unweighted simple undirected graph $G = (V,E)$, $|V| = n$.
- Adjacency matrix $A$, degree matrix $D$, Laplacian $L = D - A$.
- Quadratic form: $x^\top L x = \frac12 \sum_{(u,v)\in E} w_{uv}(x_u - x_v)^2$.
- Eigenvalues: $0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_n$.

### 1.2 Conductance (Cheeger constant)
- $S \subseteq V$, $|S| \le n/2$: $\phi(S) = \frac{|\partial S|}{\min\{vol(S), vol(\bar S)\}}$.
- $\phi(G) = \min_{|S|\le n/2} \phi(S)$.
- Volume $vol(S) = \sum_{v\in S} \deg(v)$.

### 1.3 Cheeger's Inequality (classical)
- $\frac{\lambda_2}{2} \le \phi(G) \le \sqrt{2\lambda_2}$.
- Proof sketch:
  - Upper bound: Cheeger via Nibble / iterative improvement.
  - Lower bound: use Fiedler vector (unit-norm $x$ minimizing $x^\top L x$) and sweep over $x$-threshold cuts; each cut has conductance at most $\sqrt{2\lambda_2}$.
- Intuition: small eigenvalues force slow decay of Dirichlet energy ↔ poor expansion.

### 1.4 Spectral Sparsifiers (Spielman-Srivastava, 2011)
- Target: sparse weighted graph $H$ on $V$ with $O(n \log n / \varepsilon^2)$ edges preserving all cuts to $(1\pm \varepsilon)$.
- Equivalent to preserving Laplacian quadratic forms: $\forall x$, $(1-\varepsilon)x^\top L_G x \le x^\top L_H x \le (1+\varepsilon)x^\top L_G x$.
- Key tool: effective resistance $R_{uv} = (e_u - e_v)^\top L^\dagger (e_u - e_v)$.
- Sampling edges with probability $\propto w_{uv} R_{uv}$ gives a spectral sparsifier with $\tilde O(n/\varepsilon^2)$ edges.
- Consequence: cut values preserved and low-conductance cuts detected by spectrum.

---

## 2. Recent Extension: Spectral CSP Sparsification

Source: Khanna, Putterman, Sudan, “A Theory of Spectral CSP Sparsification,” arXiv 2504.16206 (extending SODA 2024 combinatorial sparsifiers).

### 2.1 Problem
Given a CSP instance with constraints $C_i$, we want a small weighted subset of constraints preserving some “energy” of assignments.

### 2.2 Field-Affine CSPs
Predicates $P(x_1,\dots,x_r) = \mathbf{1}\!\left[\sum_j a_j x_j \neq b \pmod p\right]$.
Captures graph cuts, hypergraph cuts, XORs, and general $\mathbb{F}_p$ predicates.

### 2.3 Spectral Energy
- Extends quadratic form from graphs to CSPs.
- Enables defining a second eigenvalue for CSP instances that captures expansion-like separation.

### 2.4 Generalized Cheeger's Inequality
- For even-arity XOR CSPs, a Cheeger-style inequality relates this second eigenvalue to combinatorial expansion.
- This is the first Cheeger analog beyond graph/hypergraph spectral setting to CSP instances.

### 2.5 Main Result
- Polynomial-time construction of a spectral sparsifier of near-quadratic size for all field-affine CSPs.

Implications:
- Reduces constraint checking to small representative subsets.
- Enables faster local/parallel/ distributed algorithms where each constraint needs low-degree spectral representation.

---

## 3. Connections to Other Theory

| Concept | Link |
|---|---|
| Expander mixing lemma | Bounds on set intersections via eigenvalues. |
| Szemerédi regularity lemma | Foundational combinatorial struct. result, not spectral. |
| Approximate nearest neighbor | Spectral embeddings used in metric sparsification and dimension reduction. |
| Lovász local lemma | Dependent-event analysis; spectral sparsification bounds dependent structure. |
| VC dimension | Sample complexity bounds via capacity; spectral methods help bound covering numbers. |

---

## 4. Exercises

### Exercise 1: Rayleigh characterization
Let $L$ be a graph Laplacian. Prove that $\lambda_2 = \min_{x: x^\top 1 = 0, x\neq 0} \frac{x^\top L x}{x^\top x}$.
*Consequence:* Fiedler vector gives cut of conductance $O(\sqrt{\lambda_2})$.

### Exercise 2: Expanders
Show that the complete graph $K_n$ has smallest nonzero eigenvalue $\lambda_2 = n$ and conductance $1 - 1/n$.
*Idea:* eigenvalues computed exactly from regular structure; compare with Cheeger bound.

### Exercise 3: Effective resistance and spectrum
Prove that $R_{uv} \le \text{dist}_G(u,v) \le (n-1)R_{uv}$. Use this to argue why long-path edges get sampled heavily.
*Takeaway:* effective resistance overcomes local-degree bias in cut preservation.

### Exercise 4: Spectral vs. combinatorial sparsifier
Give an example of two graphs $G,H$ that preserve all cuts exactly but have very different $\lambda_2$.
*Follow-up:* If $H$ is a spectral sparsifier of $G$, must $\lambda_2(H)$ approximate $\lambda_2(G)$?
*Hints and solution sketch:* Counterexamples exist; exact cut preservation is too weak for spectral equivalence.

### Exercise 5: Cut-preserving vertex sparsifiers (ICALP 2025)
Show that exact planar cut sparsifiers require $2^{\Omega(k)}$ size in the worst case, while $1+\varepsilon$ approximation suffices with $\tilde O(k/\text{poly}(\varepsilon))$.
*Concept:* demonstrates exponential gap between exact and approximate compression.

---

## 5. Advanced Reading

- Spielman, Teng: “Spectral Sparsification of Graphs,” STOC 2008 / TOCS 2011.
- Batson, Spielman, Srivastava: “Twice-Ramanujan Sparsifiers,” STOC 2008.
- Khanna, Putterman, Sudan: “A Theory of Spectral CSP Sparsification,” arXiv 2504.16206.
- Davies-Peck: “On the Locality of the Lovász Local Lemma,” STOC 2025.
- Chen, Tan: “Cut-Preserving Vertex Sparsifiers for Planar and Quasi-Bipartite Graphs,” ICALP 2025.

---

## 6. Quick Reference: Cheeger Bounds

| Object | Cheeger bound role |
|---|---|
| Graph | $\lambda_2/2 \le \phi \le \sqrt{2\lambda_2}$ |
| Hypergraph | Sweep cuts generalize, constants worsen. |
| XOR CSP | Khanna-Putterman-Sudan generalize to spectral eigenvalue/expansion |
| Planar sparsifier | Gap between exact ($2^{\Omega(k)}$) and approx ($\tilde O(k)$) |

---

## 7. One-Line Takeaways

1. Cheeger’s inequality is the bridge between continuous linear algebra and discrete expansion.
2. Spectral sparsifiers preserve global cut structure using $\tilde O(n)$ edges.
3. Extending spectral ideas to CSPs opens parallel/distributed algorithmic applications.
4. Approximate spectral preservation is exponentially easier than exact.
