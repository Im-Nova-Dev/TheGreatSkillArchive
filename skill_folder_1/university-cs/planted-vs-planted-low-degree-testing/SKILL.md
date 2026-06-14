---
name: planted-vs-planted-low-degree-testing
title: Planted-vs-Planted Low-Degree Polynomial Testing
description: Teach low-degree polynomial testing thresholds for planted-vs-planted problems, sharp recovery vs. detection thresholds, and related probabilistic method tools.
---

# Planted-vs-Planted Low-Degree Polynomial Testing

Use this skill when studying or teaching the low-degree method for statistical testing and recovery, especially in planted combinatorial models.

## Core Idea

Given observed data, we ask which of two random mechanisms generated it:
- **Planting**: An object or structure is embedded into a noisy background.
- **Planted-vs-planted**: Distinguish between two planted mechanisms with vanishing error.

Low-degree polynomial tests, inspired by sum-of-squares and statistical physics, capture the power of polynomial-time algorithms for these tasks.

## Model Families

### 1. Planted Dense Subgraph (PDS)
- Null: Erdos-Renyi graph G(n, 1/2).
- Planted: Sparse clique/community inside G(n, 1/2), or planted cluster with higher edge density.

### 2. Planted Submatrix (PSM)
- Null: Matrix of independent entries.
- Planted: A submatrix has higher mean (or structured signal) against a background.

Both models admit sharp low-degree thresholds.

## Key Concepts

### Low-Degree Polynomial Distinguishability

A low-degree SoS / polynomial test can distinguish planted distributions if:
```
lim_{n->infty} E_null[P] < lim_{n->infty} E_planted[P]
```
for a polynomial P of bounded degree D.

The **low-degree likelihood ratio** at degree `d` is:
```
L_d = E_planted[f_d] / E_null[f_d]
```
with sharp thresholds emerging from the asymptotics of Hermite/Schur/Chebyshev polynomials aligned to the planted signal.

### Detection Thresholds

- **Strong testing**: vanishing total error (Type I + Type II -> 0) requires signal above a sharp threshold.
- **Weak testing**: accuracy strictly > 1/2 permits smooth transition below the strong threshold.

The recent Skeja et al. result (June 2026) proves the testing threshold matches the low-degree recovery threshold down to constants for community counting in PDS and PSM; weak testing shows a smooth phase rather than a jump.

### Recovery vs. Distinguishability

- **Recovery threshold**: smallest signal where any low-degree method can approximately reconstruct the planted object.
- **Detection threshold**: smallest signal where planted-vs-planted testing is possible.

For many models these coincide; PDS/PSM are canonical examples.

## Methodological Tool: Latent-Variable Expansion

A proof framework building on the Gaussian-space low-degree method:
1. Encode planted differences via Hermite polynomials.
2. Expand the likelihood ratio in a latent-variable basis.
3. Prune non-signal contributions via cancellation/integration.

This framework is useful across combinatorial Gaussian and sparse models.

## Exercises

1. Show that the planted clique detection threshold at degree d = O(n) corresponds to clique size w = O(sqrt{n log n}).
2. Compare strong vs. weak testing in the planted dense subgraph model and explain why weak testing does not have a sharp threshold.
3. For planted submatrix, relate the spectral threshold to the low-degree recovery threshold.

## References

- Skeja, A., Espinoza, D. G., Skerman, F., & Wein, A. S. (2026). Sharp Low-Degree Thresholds for Planted-vs-Planted Testing. arXiv:2606.05266 [cs.LG, cs.CC, cs.DS, math.CO, math.PR, math.ST].
