---
name: truly-linear-fpt
title: Truly Linear FPT (TLFPT) — The 2026 Breakthrough
description: Teach the 2026 Curticapean-Wang definition and separation of Truly Linear FPT (O(n + f(k))) from Linear FPT (O(n) · f(k)), including the diagonalization proof, treedepth/BFS-width parameters, and concrete problems in TLFPT (SAT, Vertex Cover, k-Path, H-Coloring). Use when covering parameterized complexity, Big Data algorithmics, or complexity class separation techniques.
tags:
  - parameterized-complexity
  - complexity-theory
  - fpt
  - big-data
  - treedepth
  - bfs-width
  - diagonalization
skill_type: lecture
prerequisites:
  - Basic parameterized complexity (FPT, W-hierarchy)
  - Basic complexity theory (P, NP, reductions)
  - Graph theory fundamentals (treewidth, treedepth, BFS/DFS)
estimated_minutes: 50
---

# Truly Linear FPT (TLFPT)

## Core Definition

**TLFPT** = problems solvable in **O(n + f(k))** time
- **Additive** linear dependence on input size n
- Parameter dependence confined entirely to f(k)

This contrasts with:

| Class | Time Complexity | Meaning |
|-------|-----------------|---------|
| Classical FPT | f(k) · n^c | Multiplicative; polynomial in n |
| Linear FPT (LFPT) | O(n) · f(k) | Linear multiplicative factor |
| **Truly Linear FPT (TLFPT)** | **O(n) + f(k)** | **Additive** — single linear pass over input |

## Main Result (arXiv:2606.02492)

**Theorem**: **TLFPT ⊊ LFPT** (strict subset, proven via **diagonalization**)

This is the first formal separation showing additive linear FPT is strictly weaker than multiplicative linear FPT.

## Motivation

> "Today, however, the scale of data has changed: scientists study Big Data, which is so large that even quadratic dependence in the total input size n is unaffordable. Therefore, what constitutes a practical algorithm has also changed."

Classical parameterized complexity treats f(k)·n and f(k)+n as equivalent. **At massive scale, this equivalence breaks down.** TLFPT is a theoretically rigorous and practically necessary refinement for Big Data regimes.

**Authors**: Bumpus, Downey, Eagling-Vose, Enright, Fellows, Kutner, Larios-Jones, Martin, Rosamond, Yates (10 authors, including parameterized complexity pioneers Rod Downey and Michael Fellows)

## Problems Proven in TLFPT

| Problem | Parameter(s) | Notes |
|---------|--------------|-------|
| **SAT** | — | Boolean satisfiability |
| **Vertex Cover** | solution size k | Classic FPT problem |
| **Min-Max Matching** | — | |
| **(n-k)-Coloring** | k | Complement of k-Coloring |
| **Diverse Pair of Matchings** | — | |
| **k-Path** | path length k | |
| **H-Coloring** | — | Homomorphism to fixed graph H |

## Key Parameters Enabling TLFPT

| Parameter | Description | Why Suited for TLFPT |
|-----------|-------------|---------------------|
| **Treedepth** | Min height of rooted forest whose closure contains graph | Enables DFS-based linear-time techniques |
| **BFS-width** | BFS analogue of treewidth | Enables BFS-based linear-time techniques |

## Technical Approach

1. **Depth-First Search (DFS) techniques** — aligned with **treedepth**
2. **Breadth-First Search (BFS) techniques** — aligned with **BFS-width**
3. **Linear-time data structures** — avoiding hidden logarithmic factors
4. **Single-pass or constant-pass** input processing

The structural parameters treedepth and BFS-width are "particularly well-suited" because they directly support the linear-time graph traversal primitives that avoid revisiting large portions of the input.

## Diagonalization Proof Sketch (TLFPT ⊊ LFPT)

The separation uses a **time-constructible diagonalization** against LFPT machines:

1. Enumerate all LFPT deciders for a fixed parameter k
2. Construct a language that on input (x, k) simulates the k-th machine for n·g(k) steps with g growing slowly
3. Flip the answer if simulation halts within budget
4. Show the diagonal language is in LFPT but not in TLFPT

The key is that LFPT allows n·f(k) time which can simulate TLFPT's O(n + f(k)) budget many times over, enabling the diagonalization.

## Teaching Exercises

1. **Hierarchy Comparison**: Prove that if a problem admits an O(n log n + f(k)) algorithm, it is in LFPT but not necessarily in TLFPT. Where does the log factor matter at scale?

2. **Treedepth Exercise**: Show that Vertex Cover on graphs of treedepth d can be solved in O(n + 2^d) time by dynamic programming on the treedepth decomposition. Explain why this is TLFPT with parameter d.

3. **BFS-width Exercise**: Describe how a BFS layering of a graph with BFS-width w enables an O(n + 2^w) algorithm for Independent Set. Compare to standard treewidth-based approach.

4. **Diagonalization Analysis**: In the TLFPT ⊊ LFPT proof, why doesn't the same diagonalization separate LFPT from classical FPT? What property of the O(n + f(k)) bound is essential?

5. **Practical Implications**: Suppose you have a Vertex Cover algorithm with f(k) = 2^k and n = 10^9. Compare runtime estimates for O(n + 2^k) vs O(n · 2^k) at k = 20, 30, 40. What does this say about "practical FPT" at Big Data scale?

## Significance

- **First formal definition** of additive linear FPT
- **Separation result** via diagonalization
- **New complexity class** for the Big Data era
- **Framework** for analyzing which problems admit *truly* linear-time parameterized algorithms
- **Bridges** classical parameterized complexity and modern streaming/sublinear algorithms
- **Elevates treedepth/BFS-width** as first-class parameters alongside treewidth

## Reference

B. M. Bumpus, R. Downey, T. Eagling-Vose, J. Enright, M. R. Fellows, D. C. Kutner, L. Larios-Jones, B. Martin, F. Rosamond, E. Yates, *O(n + f(k)): Truly Linear FPT*, arXiv:2606.02492, June 2026 (42 pages).

## Connections

- **streaming-algorithms**: TLFPT algorithms often use single-pass patterns
- **sublinear-algorithms**: Related to sublinear time on massive inputs
- **parameterized-complexity-fundamentals**: Builds on classical FPT framework
- **treewidth-and-decompositions**: Treedepth/BFS-width as structural parameters