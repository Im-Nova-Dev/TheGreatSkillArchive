---
name: ramsey-number-lower-bounds-and-ai-search
description: >
  Teach classical and modern lower bounds for Ramsey numbers, the probabilistic method and constructive explicit constructions, the computational tradition of custom search algorithms, and the 2026 AI-driven unified meta-algorithm
  result arXiv:2603.09172 with improved lower bounds including R(4,16) ≥ 174, R(4,20) ≥ 237, and a reproducibility gap that prior work rarely documented algorithms for. Use when covering extremal
  combinatorics, probabilistic combinatorics, computational combinatorics, AI-assisted mathematics, or algorithmic search.
---

# Ramsey Number Lower Bounds and AI Search

## 1. Ramsey Numbers and the Lower Bound Problem

Given graphs G and H, the Ramsey number R(G,H) is the smallest n such that every red/blue edge-coloring of Kn contains either a red copy of G or a blue copy of H. For complete graphs R(s,t), exact values are known only for very small s,t. The central algorithmic challenge is to **exhibit** a red/blue edge-coloring of Kn with **no** monochromatic subgraph of the forbidden sizes; this gives the lower bound R(s,t) > n.

## 2. Classical Lower Bound Techniques

- Probabilistic method: random colorings show almost surely many n complete with no large monochromatic clique (Erdős). Good for existence, not for explicit constructions.
- Greedy / density-greedy: iteratively choose colors limiting clique growth.
- Product / concatenation constructions: combine small-color-free graphs into larger ones.
- Cyclic / algebraic constructions: use Paley, polarity, or block design graphs to get structure.
- Tabu / local search: randomized greedy with禁忌 or annealing-style improvements.

## 3. Modern Computational Landscape

Historically each new lower bound required a **bespoke search algorithm**. Benchmark papers almost never published their search code or pseudocode, leaving a reproducibility gap. Lower-bounds tables for R(4,t) and R(3,t) grew slowly because each algorithm produced only a handful of results.

## 4. The 2026 Unified Meta-Algorithm Result

arXiv:2603.09172 — Nagda, Raghavan, Thakurta (March 2026; updated April 2026) introduced a single unified meta-algorithm based on an LLM-guided code mutation agent called **AlphaEvolve** that:

- Generates candidate graph search algorithms instead of hand-coding them individually.
- Reuses one search recipe across small and large Ramsey targets.
- Reproduces all prior known lower bounds where exact values are known.
- Matches or beats the best published lower bounds on a wide collection of cases.
- Publicly provides the algorithmic process, partially closing the reproducibility gap.

### Key Improvements

| Ramsey Number | Prior Lower Bound | New Lower Bound |
|---------------|-------------------|-----------------|
| R(3, 13)      | 60                | 61              |
| R(3, 18)      | 99                | 100             |
| R(4, 13)      | 138               | 139             |
| R(4, 14)      | 147               | 148             |
| R(4, 15)      | 158               | 159             |
| R(4, 16)      | 170               | 174             |
| R(4, 18)      | 205               | 209             |
| R(4, 19)      | 213               | 219             |
| R(4, 20)      | 234               | 237             |

## 5. Why R(4,16) Jump is Interesting

A +4 jump from 170 to 174 is unusually large for a single paper in a mature area. It means the search algorithm found a 174-vertex 2-coloring avoiding K4 and K4, which previous hand-tuned searches missed.

## 6. Technical Context

- Objective: maximize n subject to no K_s in red and no K_t in blue.
- Search space: ~2^(n choose 2) colorings; impossible to enumerate for n = 200+.
- Practical reductions:
  - Symmetry breaking via fixed red edges or automorphism-free initial segment.
  - Positive-degree constraints to bound neighborhoods.
  - Local search to fix red-blue conflicts and recover feasibility.
- Modern lower-bound constructions rely heavily on SAT/CP backbones and unsatisfiability-guided pruning.

## 7. Implications

- Meta-algorithm design is becoming a first-class combinatorial tool.
- Algorithmic transparency/audit is now a bottleneck if results are to be trusted and extended.
- Lower-bound records previously considered near the limit of computational reach can now advance faster.

## 8. Exercises / Teaching Probes

1. Show why a random 2-coloring of Kn with n = c sqrt(2) 2^{s/2} fails to force a monochromatic K_s in one color; derive the probabilistic lower bound for R(s,s).
2. Prove that any coloring of K_6 contains a monochromatic K_3; generalize to R(3,3) = 6.
3. Sketch how an LLM-guided search could treat algorithmic search as a code-generation task: what prompt, reward, and mutation operators make sense?
4. For R(4,t), explain why the known lower bound constructions are sparse and why tabu search is typically more successful than pure greedy.
