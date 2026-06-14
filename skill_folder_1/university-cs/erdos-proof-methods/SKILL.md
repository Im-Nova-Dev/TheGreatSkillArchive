---
name: erdos-proof-methods
title: Erdős-Style Short Proof Methods
description: Teach compact proof techniques used across combinatorics, number theory, and probability, with canonical examples and reusable proof sketching methods.
---

# Erdős-Style Short Proof Methods

Goal: Give a compact reference for proof techniques that resolve concrete combinatorial, probabilistic, or number-theoretic statements—especially the style of short, elegant proofs the literature associates with Paul Erdős and with modern proof search.

## When to use this skill

- You need a starting strategy for a short proof problem in combinatorics/probability/number theory.
- You want to understand or communicate how a five-to-ten-line argument can finish a long-open conjecture-style question.
- You want to compare proof-craft styles: constructive vs. probabilistic vs. extremal/weight-shifting.

## 1. Canonical Proof Styles

### 1.1 Weight-Shifting / Convexity

Idea. Reassign weights or “budget” among objects to create a favorable examplar.

Template steps:
1. State a convex function bound on a weighted sum.
2. Show that any “imbalanced” configuration can be shifted toward a special configuration without increasing the objective.
3. Conclude a bound or existence claim.

Classic use. Bounds on the minimum number of monochromatic arithmetic progressions, or extremal results for sum-free sets.

### 1.2 Probabilistic Method

Idea. Show a random object exists by proving its expected value is positive.

Template steps:
1. Define a random model on the relevant set of objects.
2. Compute expectation of the target quantity (often count of “bad” events).
3. Derive that a positive-probability object satisfies the claim.

Classic use. Lower bound on Ramsey numbers, existence of graphs with high girth and chromatic number.

### 1.3 Local-to-Global / Degeneracy

Idea. Show a local obstruction is impossible, then lift to global structure.

Template steps:
1. Assume a counterexample with minimal size.
2. Derive a contradiction by dismantling a local part and rebuilding a smaller counterexample.

Classic use. Short proofs about ordinary lines in planar point sets, minimality arguments in hypergraph Turán-type results.

### 1.4 Algebraic / Fourier Reduction

Idea. Use generating functions or character sums to collapse a counting claim to a small number of core terms.

Template steps:
1. Express the target quantity with Fourier weights or an L-function.
2. Identify the dominant term.
3. Bound remainder by tail estimates.

Classic use. Sequences with uniformly small exponential sums; fewnomial discrepancy bounds.

## 2. Proof Sketch Checklist

Use this checklist when summarizing or drafting a short proof:

1. **Statement restatement.** Write the claim in one sentence.
2. **Object class.** What are the finite/infinite objects being studied?
3. **Invariant or weight.** What is preserved or optimized?
4. **Extremal step.** What is the minimal/balanced/maximal witness?
5. **Conclusion.** State the final bound or existence result.

## 3. Compact Example Pattern

Claim-style: A combinatorial or number-theoretic dichotomy/conjecture.

Proof sketch template:
- Assume the worst-case arrangement.
- Apply an averaging/weighting step.
- Exhibit a configuration that must appear.
- Conclude.

This structure matches the “quintet of short proofs” style used across combinatorics, probability, and number theory.

## 4. Exercises

1. Prove an ordinary-line statement via a minimal counterexample + pivot argument.
2. Derive a girth-vs-chromatic-number graph by the probabilistic method. Identify the key expectation.
3. Show a convexity inequality by rearranging weights to a balanced configuration. Name the function that must be convex.
4. State a fewnomial-style counting bound and explain why a counterexample approach works by focusing on the leading term.

## 5. Terminology Reference

- Ordinary line: a line containing exactly two points of a point set.
- Fewnomial: a polynomial with few monomials, often used in real algebraic geometry / discrepancy-style bounds.
- Erdős–Turán discrepancy: a classic sequence uniformity bound; short proofs often target simplified variants.
- K4-free 4-critical graph: a graph needing four colors to become 4-colorable but containing no K4; minimal chord-count conditions yield structure.
- Prime-representing quadratic pattern: questions of the form n − a k^2 prime.
