---
name: sperner-lemma-and-borsuk-ulam
title: Sperner's Lemma and the Borsuk–Ulam Theorem
description: Teach combinatorial topology through Sperner's lemma, the Brouwer fixed point theorem, and the Borsuk–Ulam theorem. Covers deterministic proofs, the combinatorial-to-topological bridge, applications to fair division, ham sandwich, and fixed-point computation, plus exercises.
source: classical
tags: [combinatorics, topology, theoretical-cs, fixed-point, discrete-math]
---

# Sperner's Lemma and the Borsuk–Ulam Theorem

Combinatorial topology: instead of continuous paths or metrics, we encode topological facts as **counting/elections** on triangulations. This lets an algorithmist extract a concrete point satisfying a geometric existence claim.

---

## 1. Sperner's Lemma

### Setup
Given a triangulation of a simplex into small simplices.

Label rule (Sperner labeling) for a 2D triangle:
- Vertices on edge AB get labels 1 or 2 only.
- Vertices on edge BC get labels 2 or 3 only.
- Vertices on edge CA get labels 3 or 1 only.
- Interior vertices may receive any of {1,2,3}.

### Theorem
In any Sperner-labeled triangulation of a simplex, the number of **fully-labeled** small simplices is **odd**.

This remains true in any dimension.

### Proof Sketch (2D)
- Consider the dual graph whose nodes are small triangles; link adjacent triangles across a properly labeled edge.
- Boundary edges of type (1–2) appear an **odd** number of times (count with orientation).
- Therefore the number of (1–2) boundary edges is odd.
- Inside, each fully-labeled triangle has exactly one boundary edge with the induced (1–2) edge; non-fully-labeled triangles contribute 0 or 2 such edges.
- Thus the count of fully-labeled triangles is odd.

### What It Buys
It gives a **computable** witness to Brouwer's fixed point theorem without continuity analysis.

---

## 2. Brouwer Fixed Point via Sperner

**Brouwer Fixed Point Theorem:** Every continuous map $f: \Delta^n \to \Delta^n$ has a fixed point.

**Combinatorial reduction:**
1. Approximate $\Delta^n$ by a fine triangulation.
2. Define a labeling: a vertex $v$ gets label $i$ where $f(v)$ lies in the coordinate-$i$ facet of $\Delta^n$.
3. This is a valid Sperner labeling.
4. By Sperner's lemma, a fully-labeled simplex exists; its barycenter approximates a fixed point.
5. Refine to convergence by continuity of $f$.

This is one of the cleanest constructive routes to BFPT and the basis of algorithms for fixed points.

---

## 3. Borsuk–Ulam Theorem

In dimension $d$:  
**Any** continuous map $f: S^d \to \mathbb{R}^d$ has a pair of antipodal points mapped to the same point:  
$$f(x) = f(-x)$$ for some $x \in S^d$.

### Proof Sketch via Sperner + Triangulation
- Triangulate $S^d$ equivariantly under antipodal automorphism.
- Use a continuous map to construct a Sperner labeling (or degree-based parity) on simplices.
- By Sperner, an odd-labeled simplex must exist; lifting by symmetry gives antipodal identification.
- Equivalently, one can establish the **degree** of the map $x \mapsto f(x) - f(-x)$ is odd, forcing a zero by the intermediate value theorem on appropriate arcs.

### Corollaries (All Follow from Borsuk–Ulam)
- **Ham Sandwich:** a single hyperplane cuts any $d$ finite measures simultaneously in half.
- **Necklace Splitting:** Two thieves can split a necklace with $t$ types of beads fairly using at most $t$ cuts.
- **Borsuk–Ulam for combinatorial sets:** For any bipartition of the vertices of a regular simplex into two sets, there is a facet whose vertices come equally from both sides.
- **Kneser graphs:** The lower bound on their chromatic numbers follows via a topological argument.

---

## 4. Applications to Theoretical Computer Science

| Application | Mechanism |
|---|---|
| **DFA state complexity** | No boolean DFA computes majority with $o(n)$ states. Uses Borsuk–Ulam. (Kainen–Kövári) |
| **Circuit depth** | Lower bounds via sign-rank/sperner-based communication complexity. |
| **Combinatorial Game Equilibria** | Nash equilibria in two-player games exist; one proof approximates via fixed-point combinators. |
| **Halving problem / epsilon-nets** | Works by detecting a point via Borsuk–Ulam from measure balancing. |
| **Superimposed codes / combinatorial search** | Uses parity arguments derived from Sperner. |

**Algorithmic angle.** The Lemke–Howson algorithm for Nash equilibria is best understood as a path-following walk whose correctness relies on Sperner's lemma indexing.

---

## 5. Teaching Exercises

1. **Sperner count.** Start with the one-interior-edge triangulation of a triangle, label vertices, and trace the dual-graph argument to verify the odd count rule.

2. **No-derangement labeling.** Given an $n \times n$ board colored with $n$ colors, each row and column containing all colors exactly once, show via Borsuk–Ulam that there is a **transversal** hitting all $n$ colors.

3. **Fair division.** Using the ham-sandwich instantiation: give a protocol dividing two players' pieces simultaneously in half by two cuts. Argue optimality.

4. **Higher-dimension Sperner.** Write the statement for $d=3$. Describe the labeling constraints on faces of a tetrahedron and prove the parity argument generalizes.

5. **Constructivity.** Given a picture of a Sperner triangulation, design an algorithm that finds a fully-labeled simplex in polynomial time in the number of small simplices.

6. **Borsuk–Ulam limitation.** Prove that the theorem fails for maps $f: S^d \to \mathbb{R}^{d-1}$ directly; explain the obstruction via the antipodal degree.

---

## 6. Connections to Other Topics
- **Simplicial homology** and fixed-point indices.
- **Combinatorial Neckenlace splitting** — purely group-action proof + Borsuk–Ulam.
- **Graph limits / regular partitions**: regularity lemma has a "Sperner" flavor in forcing homogeneity classes.
- **Discrete Morse theory**: provides homological viewpoint on these parity results.

---

## 7. References
- J. Matoušek, *Using the Borsuk–Ulam Theorem*, Springer 2003. (Canonical readable source.)
- H. Edelsbrunner, *Algorithms in Combinatorial Geometry*.
- Sperner, E. (1928). *Neuer Beweis für die Invarianz der Dimensionszahl und des Gebietes.*
- D. W. Kainen & T. Kövári, "Borsuk–Ulam implies ..."
- Goldberg & West (2005), "Necklace splitting problems."



