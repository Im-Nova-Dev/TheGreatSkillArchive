---
title: Uniform Graph Regularity and the Szemerédi Lemma
tags: [graph-theory, extremal-combinatorics, regularity-lemma]
prerequisites: [basic-graph-theory]
---

# Uniform Graph Regularity and the Szemerédi Regularity Lemma

## 1. Statement

For every graph G and ε>0, there is a partition V1,...,Vm of V(G) with m ≤ N0(ε) such that:
- all Vi have size ≤ ε|V|
- all but εm2 pairs (Vi,Vj) are ε-regular

## 2. ε-Regular Pairs

A pair (A,B) is ε-regular if |e(X,Y)/|X||Y| - e(A,B)/|A||B|| ≤ ε for all X⊆A, Y⊆B with |X|≥ε|A|, |Y|≥ε|B|.

## 3. Proof Sketch

Iteratively refine partitions: for each irregular pair, split the larger part by degree into ≤2k pieces. Count irregular pairs decrease geometrically. After O(ε-5) steps, all pairs become regular or negligible.

## 4. Applications

- Roth's theorem: any subset of {1..N} of size ≥ δN contains a 3-AP.
- Graph removal lemma: few copies of H in G ⇒ few edges to remove.
- Property testing: regularity is the basis of Frieze-Kannan weak regularity.

## 5. Strengthened Form (Frieze-Kannan)

For every graph G and ε>0, there is a partition with:
- |Vi| ≤ ε|V| + 1
- O(ε-2) parts
- ε-regularity holds for all but ε|V|2 pairs

This matches the "uniform" version with controllable part sizes.

## 6. Key Idea

Regularity partitions big graphs into "random-like" bipartite pieces plus a bounded-error remainder. Arithmetic patterns in sets of integers reduce to counting copies in these pseudo-random graphs.

## 7. Practice

- Use regularity to show any n-vertex graph with > n2/50 edges contains K3,3.
- Show Szemerédi's theorem for 3-term APs as a corollary.

## 8. Limitations

- Tower-type bound on number of parts is unavoidable in general.
- For specific graph classes, polynomial bounds exist.
