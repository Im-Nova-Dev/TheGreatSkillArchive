---
name: erdos-hajnal-conjecture
category: university-cs
description: "Teach the Erdős-Hajnal conjecture in extremal combinatorics: statement, history, known results (P5, E-graph), iterative sparsification framework, comb structures, equivalence-relation technique. Covers the 2026 breakthrough for P5 (Nguyen–Scott–Seymour) and the 2026 extension to the E-graph (Huang–Ju–Zhou)."
tags: [extremal-combinatorics, ramsey-theory, graph-theory, induced-subgraphs, iterative-sparsification]
---

# Erdős-Hajnal Conjecture — Teaching Skill

## Learning Objectives
- State the Erdős-Hajnal conjecture and explain its significance
- Understand the Ramsey-theoretic context: cliques vs independent sets in H-free graphs
- Trace the history: from original 1989 conjecture to 2026 breakthroughs
- Explain the iterative sparsification framework (Nguyen–Scott–Seymour)
- Describe the comb structure (Chudnovsky–Scott–Seymour–Spirkl)
- Apply the equivalence-relation technique for the E-graph extension

## Core Concept: Erdős-Hajnal Conjecture
> **Conjecture (Erdős–Hajnal, 1989):** For every graph H, there exists c = c(H) > 0 such that every n-vertex graph G with **no induced copy of H** contains a **clique or independent set of size at least n^c**.

Contrast with Ramsey's theorem: arbitrary graphs contain cliques/independent sets of size Ω(log n). EH says H-free graphs have *polynomially* large cliques/independent sets.

## Known Results Timeline
| Graph H | Status | Reference |
|---------|--------|-----------|
| P₄ (4-vertex path) | ✓ c = 1/2 | Trivial (split graphs) |
| All 5-vertex graphs | ✓ | NSS 2026 (P₅ case implies all) |
| **E-graph** (6-vertex) | ✓ | Huang–Ju–Zhou 2026 |
| C₅ (5-cycle) | ✓ | Chudnovsky–Scott–Seymour–Spirkl 2023 |
| 6-vertex graphs (most) | ✗ | Open |
| Bulb graph, paw, etc. | Various | See NSS survey |

## The Iterative Sparsification Framework (NSS 2026)

Three-step reduction chain for proving EH for a graph H:

1. **EH conjecture for H** → **Generalized Nice property**
   - A graph class C is "nice" if whenever G ∈ C has small max degree, G has large clique/independent set
   - Extended to "generalized nice" for the sparsification process

2. **Generalized Nice** → **Comb-related property**
   - Uses "comb" structure from CSSS 2023
   - A comb in G: (A,B) partition where A is anticomplete to B, and A contains a stable set of size ≥ |A|^c

3. **Comb-related property** → **Verify H satisfies it**
   - Structural analysis of H-free graphs
   - For H = P₅: NSS complete this in 130+ pages
   - For H = E-graph: Huang–Ju–Zhou add **equivalence-relation technique**

## The E-Graph (New 2026 Result)
- Start with P₅ = v₁–v₂–v₃–v₄–v₅
- Add pendant edge at middle vertex v₃ → new vertex v₆ adjacent only to v₃
- **6 vertices, 5 edges** — just beyond the 5-vertex frontier

## Equivalence-Relation Technique (Novel in E-graph Paper)
- Defines appropriate equivalence relations on vertex sets
- Proves an **auxiliary graph** satisfies EH
- Handles the extra complexity from the pendant edge
- Demonstrates framework robustness beyond P₅

## Teaching Exercises

### Exercise 1: Ramsey vs EH
Prove: If G has no induced P₃, then G is a disjoint union of cliques. Deduce EH holds for P₃ with c = 1.

### Exercise 2: P₄ = Split Graphs
Show a graph is P₄-free iff it is a split graph. Prove EH for P₄ with c = 1/2.

### Exercise 3: Induced Subgraph Density
Define "nice" property formally. Show: if G is nice and Δ(G) ≤ n^ε, then ω(G) ∨ α(G) ≥ n^c.

### Exercise 4: Comb Definition
Define a comb in a graph G. Prove: if every H-free graph contains a comb, then EH holds for H.

### Exercise 5: E-Graph Structure
Draw the E-graph. List all its induced subgraphs of size ≤ 4. Explain why it's "just beyond" the 5-vertex classification.

## Key References
1. **Erdős–Hajnal (1989)** — Original conjecture
2. **Nguyen–Scott–Seymour (2026)** — "Induced subgraph density. VII. The five-vertex path" PLMS 132(3): e70133
3. **Chudnovsky–Scott–Seymour–Spirkl (2023)** — "Erdős-Hajnal for graphs with no 5-hole" PLMS 126(3): 997–1014
4. **Huang–Ju–Zhou (2026)** — "Erdős-Hajnal beyond the five-vertex path" arXiv:2606.06258

## Prerequisites
- Basic graph theory (cliques, independent sets, induced subgraphs)
- Ramsey's theorem
- Familiarity with polynomial vs logarithmic bounds
- Basic combinatorial proof techniques

## Assessment Questions
1. Why does EH for P₅ imply EH for all 5-vertex graphs?
2. What is the "generalized nice" property and how does it relate to sparsification?
3. Explain the comb structure and its role in the reduction chain.
4. What new technique does the E-graph proof introduce?
5. What is the current frontier of graphs for which EH is known?