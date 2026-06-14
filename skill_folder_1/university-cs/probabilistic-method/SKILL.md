---
name: probabilistic-method
description: Teach the probabilistic method in combinatorics including existence proofs via expectation, Lovász local lemma, alteration method, and recent applications to multicolor Ramsey lower bounds with teaching exercises and a worked proof sketch.
---

# Probabilistic Method

## Core idea
- Prove existence by showing a random object has the desired property with nonzero probability.
- Key tools: expectation, first/second moment, alteration, Lovász local lemma, entropy method.

## Canonical examples
1. **Lower bound on Ramsey numbers** `r(t, t) >= 2^{t/2}` (Erdős, 1947).
2. **Existence of graphs with large girth and chromatic number** (random graph alteration).
3. **Linearity of expectation counterexamples**: two-colorings of edges with no large monochromatic clique.

## Proof sketch template
1. Define a probability space relevant to the combinatorial object.
2. Show `Pr[bad event] < 1` or `E[# of good objects] > 0`.
3. Conclude existence.

## Recent theory intel
- Builds on Sawin 2023 and Campos–Pohoata 2026.
- For multicolor Ramsey numbers `r(t; ℓ)`, using a dense spherical random geometric graph improves state-of-the-art lower bounds to
  `r(t; ℓ) >= 2^{0.383796(ℓ−2)t + t/2 + o(t)}` with a small exponential gain for `ℓ ≥ 3`.
- The gain comes from replacing the Erdős–Rényi random graph with a spherical random geometric graph `H(M, d, p)`:
  - vertices are points on `S^{d−1}`
  - edges depend on thresholded inner products
  - edge dependencies suppress independent sets more sharply than Erdős–Rényi for densities `p ∈ (0.42, 1/2)`
- Parameter `c_{t,t}` = infimum over `K_t`-free graphs `G` of `Pr[s i.i.d. uniform vertices form an independent set]`
  directly controls multicolor Ramsey lower bounds via Sawin's theorem:
  `r(t; ℓ) >= c_{t,t}^{−(ℓ−2)/t} 2^{binom(t−1)}{2}`.
- Key geometric probability bound: with `d ~ D^2 t^2`, a spherical random geometric graph is `K_t`-free with high probability, while `t` uniform random vertices form an independent set with probability roughly `exp(-γ t^2 + o(t^2))`.

## Teaching approach
- Work through Erdős's original 1947 Ramsey lower bound.
- Explain why negative correlation in geometric graphs suppresses independent sets.
- Derive the Sawin reduction from `c_{t,t}` to multicolor Ramsey bounds.
