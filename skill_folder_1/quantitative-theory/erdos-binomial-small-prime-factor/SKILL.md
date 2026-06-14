---
name: erdos-binomial-small-prime-factor
description: >
  Teach the Erdős–Lacampagne–Selfridge least prime factor conjecture for binomial
  coefficients, the classical context and bounds, and the 2026 short proof of a
  related problem from arXiv:2603.29961. Includes elementary Kummer-based estimates,
  the role of factorial prime divisors, and simple exercises.
  Use when introducing combinatorial number theory, binomial coefficients, or
  algorithmic lower bounds on arithmetic functions.
---

# Erdős–Lacampagne–Selfridge smallest-prime-factor problem for binomial coefficients

## Problem statement (restricted form)

For integers `1 <= k <= n/2`, let

```
lpf( n choose k ) = smallest prime p with p | (n choose k).
```

The classical conjecture, with finitely many exceptions, is

```
lpf( binom(n,k) ) <= max( n/k , 13 ).
```

A related stronger one-sided statement proved by Ecklund for `n > k^2` is

```
lpf( binom(n,k) ) <= C * (n/k)
```

for some constant `C`, and there are counterexamples near boundary regimes.

## Classical tools and proof ingredients

1. **Legendre/Kummer valuations**
   - `v_p( binom(n,k) )` equals the number of carries when adding `k` and `n-k` in base `p`.
   - This directly controls whether a small prime divides the binomial coefficient.

2. **Small primes always appear (Erdős–Selfridge style)**
   - If `n > 17.125 k` then a prime `p <= n/k` always divides `binom(n,k)` except `binom(7,3)=5*7`.

3. **Exceptions and near-misses**
   - Known explicit exceptions for the bound
     `lpf( binom(n,k) ) > n/k`:
       - `binom(62,26)`: lpf = 19, n/k -> 2.38
       - `binom(95,96)`, `binom(47,466)`, `binom(28,428)`
   - These show the bound is tight only in very sparse regimes.

4. **Lower bounds on `g(k)`**
   - Define
     `g(k) = min { n > k : lpf( binom(n,k) ) > k }`.
   - Current lower bound:
     `g(k) >= exp( c (log^3 k / log log k)^{1/2} )`.

## The 2026 short proof context

Alexeev, Putterman, Sawhney, Sellke, and Valiant, arXiv:2603.29961,
answered three open questions raised by Erdős with short proofs, one of
which concerns the distribution of small prime factors of binomial
coefficients.

Pedagogical takeaway: the result shows that a combination of
Kummer's carry interpretation and a short extremal argument can
pin down the small-prime-factor behavior that previously required
heavy computation or long arguments.

## Intuition

- Binomial coefficients encode arithmetic across many residues.
- Kummer's theorem converts "is there a small prime factor?" into a
  question about digit carries: easy to reason about combinatorially.
- The `n/k` threshold is natural because `binom(n,k)` contains about
  `k` factors each near `n/k`.

## Exercises

1. For `p=2`, use Kummer's theorem to compute `v_2( binom(10,3) )`.
2. Show that if `p <= n/k` and `p` is prime, then under some digit-base
   conditions the inequality `lpf(...) <= n/k` holds.
3. Why does the example `binom(7,3)=35` defeat a naive strongest conjecture?
4. Verify the small counterexamples in the list above with a short script
   factoring `binom(n,k)` and printing its least prime factor.

## References

- Erdős, Lacampagne, Selfridge (1993), *Estimates of the Least Prime Factor of a Binomial Coefficient*.
- Ecklund (1969), *On prime divisors of binomial coefficients*.
- Alexeev et al., arXiv:2603.29961 (2026).
- Erdős problem catalog tag: https://www.erdosproblems.com/tags/binomial%20coefficients
