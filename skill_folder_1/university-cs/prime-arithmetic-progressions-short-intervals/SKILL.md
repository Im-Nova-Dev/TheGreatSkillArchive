---
name: prime-arithmetic-progressions-short-intervals
description: >
  Teach the 2025 breakthrough on prime arithmetic progressions in short
  intervals beyond the classical 17/30 barrier, based on Le Duc Hieu
  arXiv:2509.04883. Covers the main theorem, pseudorandom machinery,
  the Guth–Maynard zero-density estimates, the Green–Tao transference
  principle, and worked exercises in analytic/combinatorial number theory.
  Use when teaching additive prime number theory, short-interval sieves,
  transference principles, or pseudo-randomness controls.
difficulty: advanced
tags:
  - number-theory
  - combinatorics
  - prime-APs
  - sieves
  - short-intervals
  - transference-principle
references:
  - https://arxiv.org/abs/2509.04883
---

# Prime Arithmetic Progressions in Short Intervals Beyond the 17/30 Barrier

## Core Result (Theorem 1.1)

For every fixed integer `k ≥ 3` and every exponent `θ > 17/30`, the count of
`k`-term arithmetic progressions of primes inside short intervals `[x, x + x^θ]`
satisfies

```
# { k-APs of primes in [x, x + x^θ] } ≫_{k,θ} N² / ( (φ(W)/W)ᵏ (log R)ᵏ )
```
with `N ≍ X^θ / (log X)^{1/2+o(1)}`, which simplifies to

```
# ≍ X^{2θ} / (log X)^{k+1+o(1)} .
```

The lower bound is uniform for all `x ∈ [X, 2X]`.

## Why `17/30` Matters

Earlier GPY/Green–Tao arguments could not push below `θ = 17/30` because the
best available zero-density estimates for `ζ(s)` yielded `μ(θ) ≥ 3/4` for
smaller exponents. Guth and Maynard’s improved zero-density estimates give
`μ(θ) < 3/4` once `θ > 17/30`, thereby removing the exceptional-set
obstruction and enabling uniform asymptotics.

## Key Ideas

1. **`W`-trick:** Use `W = ∏_{p ≤ (1/2) log log X} p` to align primes inside a
   single residue class modulo `W`, removing small-prime obstructions.
2. **Shifted GPY sieve majorant:** Build a quadratic majorant `ν_{x,b}(t)` for
   the normalized von Mangoldt function on the aligned progression inside
   `[x, x + x^θ]`.
3. **Pseudorandomness:** The uniform short-interval Prime Number Theorem for
   `θ > 17/30`, plus zero-density estimates, shows `ν_{x,b}` satisfies
   linear-forms and correlation conditions up to complexity `k−2`, uniformly
   in `x`.
4. **Green–Tao transference:** Apply the relative Szemerédi form to obtain
   lower bounds on `k`-APs in the pseudo-random majorant, which transfers to
   the primes themselves.

## Auxiliary Result (Proposition 1.3)

For any `q ≥ 1`, `a` coprime to `q`, and `ε > 0`, there exist infinitely many
`x` such that

```
# { p prime : x < p ≤ x + (log x)^ε, p ≡ a (mod q) } ≫_{ε,q} log log x .
```

This is a Maynard-type dense-cluster lemma restricted to a fixed congruence
class in tiny intervals.

## Dependent Tools / Prerequisites

- Brun/Halberstam sieve methods
- Szemerédi theorem and relative Szemerédi framework
- `U^k` Gowers norms
- Vinogradov–Korobov zero-density estimates for `ζ(s)`
- GPY and Maynard sieve machinery

## Exercises

1. **`θ` Threshold Reasoning.** If future zero-density work lowers the critical
   barrier from `17/30` to `θ₀`, which portion of the argument changes first?
   Sketch the dependency chain.

2. **`W`-Trick Scaling.** Derive `W = (log X)^{1/2+o(1)}` from the definition
   `w = (1/2) log log X` using Mertens’ third theorem.

3. **Complexity Requirement.** Explain why the correlation conditions on the
   sieve majorant are only needed up to complexity `k−2` rather than `k`.

4. **Sparse-Set Perspective.** Compare the new uniform short-interval result
   with the “Green–Tao theorem for sparse sets” and explain why an exceptional
   set arises in the “almost-all” variant (Theorem 1.2).

## Further Reading

- Le Duc Hieu, *Arithmetic progressions of primes in short intervals beyond the
  17/30 barrier*, arXiv:2509.04883 [math.NT] (Sep 2025).
- B. Green and T. Tao, *The primes contain arbitrarily long arithmetic
  progressions*, Annals of Math. 168 (2008).
- K. Maynard, *Small gaps between primes*, Annals of Math. 181 (2015).
- K. Ford, B. Green, J. Maynard et al., *Long gaps between primes* and
  subsequent work.
