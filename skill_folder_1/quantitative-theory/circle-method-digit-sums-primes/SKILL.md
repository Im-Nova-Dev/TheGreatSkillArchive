---
name: circle-method-digit-sums-primes
title: Circle Method For Digit Sums Of Primes (Explicit Surjectivity Threshold)
description: >
  Teach the 2026 breakthrough (arXiv:2606.04677, Lehmann) giving the first explicit
  numerical threshold for the surjectivity of the digit-sum function on primes:
  every integer m ≥ M < 1.78 × 10³² with gcd(m, 9) = 1 equals s(p) for some prime p.
  Covers the Drmota-Mauduit-Rivat (DMR) circle method for digital restrictions on primes,
  explicit major/minor arc constant tracking, Type-II estimates, and the accompanying
  verification code. Use when teaching analytic number theory, circle method effectivity,
  digital problems in primes, or computer-assisted proof techniques.
tags:
  - number-theory
  - analytic-number-theory
  - circle-method
  - primes
  - digit-sums
  - explicit-bounds
  - computer-assisted-proof
skill_type: teaching_and_research
---

## When To Use
Use this skill when explaining:
- how the circle method applies to digital restrictions on primes (Drmota-Mauduit-Rivat framework),
- the distinction between qualitative existence (Harman, DMR) and explicit computable bounds,
- explicit constant tracking across major/minor arcs in additive combinatorics,
- computer-assisted verification of analytic number theory bounds.

## Core Result

### Main Theorem (Lehmann 2026, arXiv:2606.04677)
**There exists an explicit integer `M < 1.78 × 10³²` such that every integer `m ≥ M` with `gcd(m, 9) = 1` occurs as `s(p)` for at least one prime `p`.**

Where `s(n) = s₁₀(n)` is the decimal sum-of-digits function.

### Quantitative Lower Bound
```
A_m(10^{2m/9}) ≥ C_q(m) · 10^{2m/9} / m^{3/2}
```
- `C_q(m)` is **explicit**, **positive** above the sufficient threshold
- `C_q(m)` is **bounded away from 0** along each admissible residue class

### Admissibility Condition
`gcd(m, 9) = 1` is necessary and sufficient because:
- `s(n) ≡ n (mod 9)` (digit sum congruence)
- Primes > 3 are ≡ 1,2,4,5,7,8 (mod 9)

### Application
**Proves the infinitude of OEIS A070027** — primes whose iterated digit-sum chain remains prime until reaching a one-digit prime.

## Methodology: DMR Circle Method With Explicit Constants

### Framework
The **Drmota-Mauduit-Rivat (DMR) circle method** for digital restrictions on primes:
- Classical circle method decomposes [0,1] into major arcs 𝔐 (near rationals a/q) and minor arcs 𝔪
- DMR adapts this to handle digital functions s(n) (sum of digits)
- The key is controlling Type I and Type II exponential sums with digital weights

### Novelty: Full Effectivity
Lehmann's breakthrough makes **every constant explicit**:

| Component | Classical DMR | Lehmann 2026 |
|-----------|---------------|--------------|
| Major-arc estimates | Implicit constants | **Explicit, tracked** |
| Prime exponential sums | Implicit input | **Fully explicit replacement** |
| Minor-arc (Type-II) | Implicit O-notation | **Constant-tracked** |
| Final threshold | Qualitative existence | **M < 1.78 × 10³² (explicit)** |

This is 85 pages of constant tracking across the entire analysis.

### Circle Method Decomposition
Let `r_m(x) = ∑_{p ≤ x} 1_{s(p)=m}` be the counting function.

**Fourier expansion:**
```
r_m(x) = ∫₀¹ S(α) e(-mα) dα
S(α) = ∑_{p ≤ x} e(α s(p))
```

**Major arcs 𝔐:** Union of intervals around a/q with q ≤ Q (explicit).
- Use Vaughan's identity to decompose S(α) into Type I/II sums
- Major-arc main term yields the asymptotic density with explicit singular series

**Minor arcs 𝔪:** Complement of 𝔐 in [0,1].
- Vinogradov/Vaughan Type-II estimates with explicit constants
- Control via rational approximation and Gauss sum bounds

## Teaching Exercises

1. **Digit sum admissibility.** Prove `s(n) ≡ n (mod 9)` and characterize admissible m for primes.
2. **Type I/II decomposition.** Write Vaughan's identity for Λ(n) (von Mangoldt) and explain how digital weights propagate.
3. **Minor arc bound.** Given a rational approximation |α - a/q| ≤ 1/qQ, derive the Type-II sum bound with explicit constants.
4. **Code exploration.** Clone `github.com/JensLehmann/Prime-Digit-Sums` (tag `v1.0-mcom-submission`), run the verification, and trace how M is computed.
5. **Singular series computation.** Compute the singular series 𝔖(m) = ∏_p (1 - ν_p(m)) / (1 - 1/p)^{k-1} for small m and compare with heuristic density.

## Connections

- **gowers-uniformity-norms** — Higher-order Fourier analysis for linear forms; circle method handles the same sums with classical Fourier.
- **hilbert-10-ring-undecidability** — Contrast effective results (this skill) with undecidability in rings without unique factorization.
- **gaussian-prime-circle-method** — Analogous circle method setup over Z[i] instead of digital restrictions over Z.
- **permanent-range-superpolynomial-bound** — Similarly uses additive combinatorics (GAPs, bounded monomial maps) for superpolynomial bounds.

## Resources

- **Paper:** arXiv:2606.04677 (85 pages, submitted to Mathematics of Computation)
- **Code:** github.com/JensLehmann/Prime-Digit-Sums (release v1.0-mcom-submission)
- **Author:** Jens Lehmann

## Open Problems

- Improve the threshold M < 1.78 × 10³² using better minor-arc estimates or new major-arc techniques.
- Extend to other bases b ≠ 10 (digit sums in base b).
- Effective bounds for `r_m(x)` as a function of x (not just existence for large m).

---
*Skill created 2026-06-06 from arXiv:2606.04677*-