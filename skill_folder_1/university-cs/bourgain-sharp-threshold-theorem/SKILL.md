---
name: bourgain-sharp-threshold-theorem
description: "Teaches Bourgain's sharp threshold theorem connecting global Boolean behavior, threshold width, and Fourier structure. Includes KKL/Friedgut-Kalai connections, hypercontractivity proof strategy, recent extensions, and exercises."
---
# Bourgain Sharp Threshold Theorem for Boolean Functions

A **sharp threshold** for a monotone increasing Boolean function `f: {-1,1}^n -> {-1,1}` means `f` transitions from typical 0 to typical 1 over a window of width `o(p_c)`, where `p_c` is its critical probability. Bourgain proved that if `f` cannot be approximated by a low-degree Boolean function, then it must have a sharp threshold.

## 1. Core Concepts

- **Boolean function**: `f: {-1,1}^n -> {-1,1}` with Fourier expansion `f(x) = sum_{S subseteq [n]} hat{f}(S) chi_S(x)`.
- **Total influence**: `I(f) = sum_{i=1}^n Inf_i(f)` where `Inf_i(f) = E[ (f - f^{oplus i})^2 ]`.
- **Critical probability**: `p_c(f)` such that `E_p[f] = 1/2`.
- **Noise operator**: `T_rho f(x) = E_{y~N_rho(x)}[f(y)]`.
- **Hypercontractivity**: for `1 <= p < q`, `||T_rho f||_q <= ||f||_p` via Bonami-Gross hypercontractivity.

## 2. Bourgain's Theorem (informal)

If `f` is global -- meaning it cannot be approximated by any low-degree Boolean function -- then `f` has a sharp threshold. Equivalently, global means large Fourier dimension, and primes the function to be not essentially a junta on any small set of coordinates.

**Formal consequence (Friedgut-Kalai style):** if `f` is not essentially a junta, then `w(f) = O( log(delta) / I(f) )`.

## 3. Proof Strategy

1. Decompose influence by Fourier degree: `I(f) = sum_k k h_k(f)`, with `h_k` the degree-k influence.
2. Use hypercontractivity to bound tails of `h_k`.
3. If `f` is not a junta, many degrees contribute to influence and must decay in controlled ways.
4. Relate threshold width `w(f)` to `I(f)` via log-Sobolev or concentration inequalities.
5. Show `w(f) << p_c(f)`.

## 4. Key Connections

- **KKL theorem**: `max_i Inf_i(f) >= c * I(f) log n / n`.
- **Friedgut-Kalai sharp threshold theorem**: if `f` is not essentially a junta, then `w(f) = O( log(delta) / I(f) )`.
- **Friedgut-Kalai monotone graph properties**: every nontrivial monotone graph property has a sharp threshold.

## 5. Intuition

A global function feels the entire input. Because averaging theorems concentrate sharply around the equipartition point, hard-to-approximate functions cannot support the gradual transitions that soft-threshold functions require. Functions depending on a small set of coordinates can switch coordinate-by-coordinate, producing a soft threshold.

## 6. Applications

- **Random graph theory**: thresholds for connectivity, Hamiltonicity, and appearance of cliques.
- **Social choice**: noise sensitivity and threshold behavior for majority-like rules.
- **Statistical physics**: percolation thresholds and critical behavior.
- **Learning theory**: global versus local concept classes in PAC learning.

## 7. Recent Strengthenings (2000s-2020s)

- **O'Donnell-Servedio-style**: refined Fourier entropy and influence inequalities.
- **Keevash**: hypercontractivity for global functions sharpening Bourgain's result and resolving Kahn-Kalai conjectures in many cases.

## 8. Teaching Exercises

1. **Influence computation**: compute `I(OR_n)` and `I(Maj_n)` explicitly.
2. **Fourier degree and juntas**: show `OR_n` is not determined by any `o(n)` coordinates.
3. **Hypercontractivity verification**: verify `||T_rho f||_q <= ||f||_p` for a simple `f`.
4. **KKL-style reasoning**: prove `max_i Inf_i(OR_n) >= c log n / n`.
5. **Soft-threshold design**: build a monotone Boolean function with a soft threshold and explain why it is not global.

## 9. Key References

- Bourgain, J. "On the distribution of the Fourier coefficients of Boolean functions."
- Friedgut, E. and Kalai, G. "Every monotone graph property has a sharp threshold."
- O'Donnell, R. "Analysis of Boolean Functions" (survey / expository text).
- Keevash, P. "Hypercontractivity for global functions and sharp thresholds."
