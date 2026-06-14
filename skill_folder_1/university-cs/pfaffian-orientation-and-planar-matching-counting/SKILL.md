---
name: pfaffian-orientation-and-planar-matching-counting
description: Teach FKT, Pfaffian orientations, and the algebraic complexity of counting planar perfect matchings including the recent near-matching lower bound.
triggers:
  - FKT algorithm
  - Pfaffian orientation
  - planar perfect matching
  - determinant lower bound
  - algebraic circuit complexity
---

# Pfaffian Orientation and Planar Matching Counting

Compact teaching skill: how planar perfect matchings are counted via Pfaffians, and why this is algebraically hard.

## Core Concepts

1. Perfect matching. A set of edges covering every vertex exactly once.
2. Counting vs finding. Finding a perfect matching is polynomial; counting is #P-hard in general.
3. FKT breakthrough. Kasteleyn (1961) and Temperley–Fischer showed planar perfect matchings can be counted in polynomial time.
4. Pfaffian orientation. A choice of signs for edges of a planar graph such that the signed adjacency matrix has a Pfaffian equal to the number of perfect matchings.
5. Pfaffian = sqrt(det). For a skew-symmetric matrix, Pf(M)^2 = det(M). Thus counting = determinant over algebraic circuits.
6. Pfaffian circuits. An algebraic circuit model for determinant over a field. The paper maps Pfaffian computation to this model with n^(ω/2 − o(1)) operations.
7. Hardness result. Counting planar perfect matchings (n-vertex) needs Ω(n^(ω/2 − ε)) algebraic operations over algebraic circuits, matching up-to-constants the Yuster FOCS 2008 upper bound.

## Intuition

Think of the skew-symmetric adjacency matrix as encoding edge orientations in the planar embedding.
A Pfaffian orientation makes the combinatorial count manifest as a determinant/Pfaffian.
If you already know matrix determinant is expensive over algebraic circuits, the lower bound for perfect matchings inherits that hardness because the two problems are essentially the same in this restricted family.

## Selected Historical Works (compact)

- P. W. Kasteleyn, *Graph theory and crystal physics*, 1961.
- M. E. Fisher, *Statistical mechanics of dimers on a plane lattice*, 1961.
- J. W. Moon, *Counting planar perfect matchings with a sign*, 1983.
- R. Yuster, *Planar graph perfect matching is in NC*, FOCS 2008.
- H. M. Cai and J. Cheriyan, *Planar bipartite matching is in AC^0*, 1995.
- The recent result: Curticapean, Wang, arXiv:2606.03975, 2026.

## Exercises

1. Grid. Use FKT to count perfect matchings in a 2×n grid and show this yields Fibonacci numbers.
2. Pfaffian identity. Prove Pf(M)^2 = det(M) for an even-order skew-symmetric matrix M.
3. Reduction. Sketch why determinant is computable by Pfaffian computation of a related graph, suggesting why the lower bound matches.
4. Upper bound. Describe Yuster's FOCS 2008 NC-style reduction for planar perfect matchings.
5. Complexity interpretation. Explain why Ω(n^(ω/2 − ε)) over algebraic circuits is meaningful for parallel computation.

## Teaching Notes

- Connects combinatorics with linear algebra beautifully.
- Good for explaining why #P-complete does not mean “countable only by brute force.”
- Pfaffian orientations are a nice constrained-graph example of working with sign patterns.

## Assumptions / References

- Curticapean, Wang, *Planar Perfect Matching Counting is as Hard as Determinants*, arXiv:2606.03975, 2026.
- Yuster, R. *Planar graph perfect matching is in NC*, FOCS 2008.