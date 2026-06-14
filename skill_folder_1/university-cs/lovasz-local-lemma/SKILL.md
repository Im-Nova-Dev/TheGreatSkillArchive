---
name: lovasz-local-lemma
title: Lovász Local Lemma
description: Teach the Lovász Local Lemma including symmetric and asymmetric forms, constructive proofs, algorithmic versions, and applications in combinatorics, graph theory, and theoretical computer science with proofs and exercises.
source: https://arxiv.org/abs/2501.00001
tags: [combinatorics, probability, theoretical-cs, graph-theory]
---

# Lovász Local Lemma

## What It Solves
Shows that in a probability space, a set of **"bad" events** — each with small probability and only limited dependence on many others — has a nonzero probability of avoiding all bad events.

## Core Results

### Symmetric LLL
Let \(A_1, \dots, A_n\) be events with:
- \(\Pr[A_i] \le p\) for all \(i\),
- each \(A_i\) depends on at most \(d\) other events,
and suppose: \[ ep(d+1) \le 1 \]
Then: \[ \Pr\left[\bigwedge_{i=1}^n \overline{A}_i\right] > 0 \]
So a jointly-avoiding assignment exists.

### Asymmetric LLL
Replace by:
- \(p_i = \Pr[A_i]\),
- dependency set \(D_i \subseteq [n] \setminus \{i\}\) with \(|D_i| \le d_i\),
- a set of numbers \(x_i \in (0,1)\) satisfying \(x_i \Pr[A_i] \le (1-x_i)\left(\prod_{j\in D_i} (1-x_j)\right)\).

Then: \[ \Pr\left[\bigwedge_{i=1}^n \overline{A}_i\right] \ge \prod_{i=1}^n (1-x_i) > 0. \]

## Proof Ideas

1. **Entropy/induction proof (Erdős–Lovász).**
   Define a topological ordering respecting dependencies where each node has few neighbors. Replace one event at a time, each losing limited probability mass.

2. **Moment/generating-function proof (Beck).**
   Using the polynomial \(P(t) = \mathbb{E}[\exp(-t X)]\) where \(X\) is the number of bad events; bound the expected loss when conditioning.

3. **Constructive proof (Moser, Tardos).**
   Run a resampling procedure:
   - Pick any violated \(A_i\).
   - Resample the variables inside \(A_i\)'s scope independently until done.
   The key invariant is that each resampling event is **short**: terminates quickly because the LLL condition bounds "local chaos."

### Moser-Tardos Analysis Sketch
Maintain a directed dependency graph; each resampling touches at most \(d+1\) events. Under \(p = \Pr[A_i]\), the expected number of resamplings is \(\le n\). This gives a **polynomial-time** constructive proof.

## Teaching Exercises

1. **Dependency graph exercise.**
   Given an arithmetic progression property and a random graph coloring, build the dependency graph and compute \(p\) and \(d\). Verify the symmetric LLL condition.

2. **Asymmetric tightness.**
   For circle-choosing problems on points in convex position, write down different \(p_i\) and choose \(x_i\) to make the inequality tight.

3. **Algorithm simulation.**
   Implement the Moser-Tardos resampler for hypergraph 2-coloring. Plot number of resamplings vs. \(d\) under the LLL regime and beyond it.

4. **Counterexample.**
   Construct a set of events where \(\Pr[\bigwedge \overline{A}] = 0\) despite bounded degree. Notice that the bound \(ep(d+1) \le 1\) is only sufficient, not necessary.

5. **Cut-and-color application.**
   Prove the LLL gives a proper coloring of a maximum-degree-\(\Delta\) graph with \((\Delta+1)/2\) colors in the independent-set version.

## Recent Context
After the algorithmic breakthrough by Moser (2003) and Moser-Tardos (2009), many **data structure** problems, SAT solving successes, and discrepancy bounds cite the LLL as the canonical *"evidence is sparse enough to escape"* result.

## Related Concepts
- Janson's inequalities
- Correlation inequalities (FKGG)
- Variable-proximity in SAT
- Irregular LLL in combinatorial geometry
