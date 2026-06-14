---
name: probabilistic-methods-in-extremal-combinatorics
title: Probabilistic Methods in Extremal Combinatorics
description: Teach the probabilistic method and its modern refinements, emphasizing existence proofs, expectation, alterations, Lovász Local Lemma, entropy methods, and recent work on exponentially small scales. Includes canonical exercises and proof patterns.
---

# Probabilistic Methods in Extremal Combinatorics

These notes cover classic and modern probabilistic combinatorics with teaching focus: high-level technique, when to use it, canonical proofs, worked examples, pitfalls, and exercises.

## 1. Core Motto
Prove existence by showing a random object has the desired property with nonzero probability; constructive algorithms are a separate bonus.

## 2. First Tools
- Expectation: existence of an object with value below/above the mean.
- Alteration: construct, then locally modify to fix defects.
- Symmetry and linearity of expectation for counting objects.
- Lovász Local Lemma: local avoidance of many bad events when each depends on few others.
- Lovász Local Lemma constructive versions via entropy compression or Moser-Tardos.

## 3. Scale of Probability
Classic applications are "high probability": at least a constant fraction of probability. Recent techniques investigate:
- Exponentially small scales.
- Sub-exp tails and concentration refinements.
- Impossibility thresholds via entropy or container methods.
- Small subgraph containment and rare substructures.

## 4. Canonical Examples
- Erdős lower bound on Ramsey numbers.
- Lower bound on the independence number via Turán and random greedy.
- Existence of Ramsey graphs without small cliques.
- Existence of Kővári–Sós–Turán type extremal constructions.
- Existence of graphs with given degree sequence and chosen girth.

## 5. Exposition Pattern For New Topics
When teaching a new result:
1. State combinatorial goal.
2. Present random model and bad events.
3. Compute expectation or apply local lemma.
4. Derive existence bound.
5. Explain role of "scale" if probability is tiny.
6. Mention whether constructive versions exist.
7. Provide 1 compact exercise.

## 6. Teaching Exercises
1. Expectation: in a random graph G(n,1/2) show existence of a graph with maximum degree near n/2 and independence number near 2 log_2 n.
2. Local Lemma: prove there is a 2-coloring of edges of K_n avoiding monochromatic copies of F_1,...,F_k when each F_i depends on few edges.
3. Alteration: adapt Turán's theorem via random multiset deletion to get explicit chromatic bounds.
4. Exponentially small events: outline why naive first/second moment methods fail at extremely low probabilities and when entropy compression rescues existence.
5. Research exercise: read a survey on the Lovász Local Lemma and explain Moser-Tardos in 8 bullets usable for a quick study card.

## 7. Sources To Cite
- Alon and Spencer, *The Probabilistic Method*, 4th ed., 2016.
- J. Sahasrabudhe, *Probabilistic combinatorics at exponentially small scales*, ICM survey, 2025.
- M. Molloy and B. Reed, *Graph Colouring and the Probabilistic Method*.
- Peklo, recent arXiv surveys on entropy compression and constructive versions.
