---
name: berry-random-waves-clt
title: Central Limit Theorems for Berry’s Random Wave Model
description: >
  Teach the Wiener chaos decomposition approach to Berry’s random
  monochromatic waves, the missing 2D/3D CLT results, and how Hermite
  polynomial integrals govern limit theorems for local functionals on
  increasing domains. Includes intuition, key statements, and exercises.
tags:
  - probability
  - random waves
  - Wiener chaos
  - central limit theorem
  - spectral theory
  - mathematical physics
---

# Central Limit Theorems for Berry’s Random Wave Model

Source: F. Grotto, “The Missing Central Limit Theorems for Local Functionals of
Berry’s Random Wave Model”, arXiv:2606.06489, 2026.

## 1. Background and model

In the 1970s, Berry conjectured that high-frequency eigenfunctions of the
Laplace–Beltrami operator on a generic compact Riemannian manifold behave like
random waves.  One standard model is:

> **Definition.** A *Berry random wave* of frequency λ is a Gaussian random
> function defined on a domain D ⊂ ℝⁿ by
>
>     f(x) = Σ_{|k| ≤ λ} a_k Φ_k(x)
>
> where Φ_k are fixed normalised modes and the coefficients a_k are complex
> Gaussian with E[a_k] = 0 and E[|a_k|²] = 1.

This model produces stationary, isotropic, real-holomorphic-looking fields.
In spectral geometry and mathematical physics, one is often interested in
**local functionals** such as

    I_G(f) = ∫_D G(f(x), ∇f(x)) dx

for a smooth function G.  For large domains D, what is the distribution of
I_G(f)?

## 2. Wiener chaos decomposition

The Gaussian random field f can be analysed via the **Wiener chaos
decomposition** (also called the *Malliavin–Shrikhande* or *Hermite*
decomposition).  Any polynomial functional can be written uniquely as a sum

    F = Σ_{d ≥ 0} F_d

where F_d lies in the d-th Wiener chaos.  For a Gaussian random variable,
only the first two chaoses matter.  For non-linear functionals of f on a
domain, higher chaosasd.

A fundamental structural fact:

- chaos orders d are orthogonal: E[F_d G_e] = 0 unless d = e

and a normalised Hermite basis H_d on ℝ gives an explicit orthogonal basis of
each chaos component.

## 3. Classical limit theorem structure

For a local functional I_G, the variance grows like |D| and one expects a
limit distribution.  By the fourth moment method and Wiener chaos, the typical
outcome is:

| Dominant chaos order | Limit law |
|----------------------|-----------|
| 0 (mean) | degenerate |
| 1 | Gaussian |
| 2 | Gaussian / chaos-2 |
| 3 | not normal (skewed) |
| 4 | Gaussian or chaotic depending on symmetry |

More precisely, if only the low-order chaoses contribute, the limit is
Gaussian.  If higher-order chaosasd contribute non-trivially, one can obtain
a **non-Gaussian Wiener chaos limit**, or, after suitable scaling, a CLT after
centering and rescaling.

## 4. The missing 2D and 3D cases (Grotto 2026)

For dimensions n = 2 and n = 3, Berry random waves had no complete CLT
description for local integral functionals.  The gaps occurred because:

1. In dimension 2 the modal summations behave like a Wigner-type process whose
   third chaos can be nonzero.
2. In dimension 3 the modal structure is more balanced, but explicit
   combinatorial control of the trispectrum was missing.

Grotto’s paper proves:

> **Theorem (informal).**  For local smooth functionals I_G on a large disc
> D_R ⊂ ℝ² or ℝ³, as R → ∞ the distribution of I_G under the Berry model
> converges to a Gaussian after appropriate centering.  The Wiener chaos
> expansion shows that the third-degree Hermite contribution and the
> trispectrum stabilize in the limit, giving the full CLT in these dimensions.

This closes the table: limit theorems for monochromatic random waves are now
completely characterized via Wiener chaos for all spatial dimensions where the
model is well posed.

## 5. Key technical ingredients

- **Hermite polynomial expansion.** Local functionals are expanded in
  homogeneous polynomials of f and ∇f, each term corresponding to a chaos
  order via the Gaussian–Hermite duality.
- **Wiener iterated integral asymptotics.** The scaling of modal sums uses
  bounds on Wick contractions and graph counting.
- **Mellin transform / stationary phase.** Evaluates diagonal and
  near-diagonal modal contributions via oscillatory integral asymptotics.
- **Trispectrum bounds.** In dimension 3 one must control 4-fold correlations;
  these are the key new estimates closing the missing cases.

## 6. Connections to other topics

- **Chaos expansions in stochastic analysis.** The same tools appear in
  stochastic PDEs and Gaussian random field geometry.
- **Berry–Tabor conjecture.** Relates random waves to spectral statistics of
  integrable systems; CLTs for wave functionals are a natural test case.
- **Free and boolean probability.** Higher-order Wiener chaosasd correspond to
  cumulants in non-commutative probability; connections exist through the
  jump-type distributions.
- **Gowers uniformity and high-order Fourier analysis.** Both replace linear
  phases with polynomial/homogeneous structure to detect higher-order
  correlations.

## 7. Teaching exercises

1. **Chaos order count.** Given F = ∫_D φ(f(x)) dx with φ(t) = t³,
   identify the maximum Wiener chaos order appearing in F and write the
   corresponding Hermite coefficient process.

2. **Variance scaling.** Show that for a ball D_R ⊂ ℝⁿ, the variance of
   I_G(f) grows linearly with volume |D_R| when G is smooth and bounded.

3. **Gaussian limit of quadratic functionals.** Prove that if G depends only
   on f and ∇f linearly, the chaos expansion truncates at order 2 and the
   central limit follows from a standard Gaussian limit theorem in chaos.

4. **Vandermonde computation.** For the 1D model on an interval, compute the
   spectrum for Dirichlet eigenfunctions and simulate Berry random waves via
   truncated Fourier series; numerically verify the CLT for ∥f∥_{L²} over
   growing intervals.

5. **True/False.** “If the third Wiener chaos of I_G is nonzero then I_G
   cannot satisfy a CLT.”  Explain why the answer is false in general and
   characterize when it becomes true.

## 8. References

- F. Grotto, “The Missing Central Limit Theorems for Local Functionals of
  Berry’s Random Wave Model”, arXiv:2606.06489 [math.PR], 2026.
- M. Berry, “Regular and irregular semiclassical wavefunctions”, *J. Phys. A*
  10 (1977), 2083–2091.
- D. Nualart, *The Malliavin Calculus and Related Topics*, 2nd ed., 2006.
- J.-P. Kahane, *Some Random Series of Functions*, 2nd ed., 1985.
