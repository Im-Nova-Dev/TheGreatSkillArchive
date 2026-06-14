---
name: prime-fractional-distribution
title: Prime Fractional Distribution
description: >
  Teach the distribution of fractional parts {αp} for primes p, including
  Hlawka–Petersen well-distributed sequences, connections to equidistribution
  in arithmetic progressions, Weyl's criterion, and the AI-assisted proof
  resolving an Erdős problem on whether {αp} is well-distributed for all α.
  Covers number theory, fractional parts, modular primes, and proof ideas.
---

# Prime Fractional Distribution

## Concept
Given a real number α and the sequence of prime numbers p_n, study the
**fractional parts**
```
{α p} = α p - ⌊α p⌋   (for p prime)
```
These lie in the interval [0, 1).

A sequence {x_n} is **well-distributed** (Hlawka–Petersen) if, for every
interval I ⊆ [0,1),
```
lim_{N→∞} #{ n ≤ N : x_n ∈ I } / N = length(I)
```
uniformly in I, without exceptional sets.

**Erdős problem:** Is it true that for every irrational α, the sequence
{α p} is well-distributed modulo 1?

## Key Results
1. **Weyl's criterion.** A sequence is uniformly distributed modulo 1 iff
   for every non-zero integer h,
   ```
   lim_{N→∞} (1/N) Σ_{n≤N} e(h x_n) = 0
   ```
   where e(t) = e^{2π i t}. This reduces the problem to exponential sums.

2. **Connection to primes in arithmetic progressions.** Writing
   e(h α p) = e( (h α) p ), the question becomes equidistribution of primes
   in progressions with varying moduli. This links to:
   - Vinogradov's theorem (primes in short intervals)
   - Bombieri–Vinogradov theorem (average GRH)
   - Siegel–Walfisz theorem

3. **Recent resolution (Alexeev, Putterman, Sawhney, Sellke, Valiant 2026).**
   The arXiv paper `2603.29961` gives a short proof that {α p} *is*
   well-distributed, building on prior number-theoretic estimates for
   exponential sums over primes. The proof demonstrates that algorithmic
   techniques from computer science can close longstanding gaps in analytic
   number theory.

## Teaching Outline
1. Define fractional parts and uniform distribution modulo 1.
2. State Weyl's criterion and prove necessity/sufficiency.
3. Reduce {α p} equidistribution to bounding prime exponential sums.
4. Review classical tools: Vaughan identity, exponential sums over primes.
5. Present the main theorem and sketch how the new proof simplifies prior
   arguments.

## Exercises
1. Show that if α = p/q is rational, {α p} is *not* uniformly distributed
   (explain why using periodicity).
2. Use Weyl's criterion to compute {θ n} equidistribution for irrational θ.
3. Explain why bounding Σ_{p≤N} e(θ p) is harder than the same sum over
   all integers n ≤ N (cite square-root barrier / zero-free regions).

## Further Reading
- arXiv:2603.29961 — *Short proofs in combinatorics and number theory*
- Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory*
- Montgomery, *Ten Lectures on the Interface between Harmonic Analysis and
  Analytic Number Theory*
