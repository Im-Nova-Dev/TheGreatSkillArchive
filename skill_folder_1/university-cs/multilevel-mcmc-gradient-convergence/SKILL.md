---
name: multilevel-mcmc-gradient-convergence
title: Multilevel MCMC Gradient Convergence and Multilevel Adaptive Stochastic Optimization
description: Teach convergence of multilevel Markov chain Monte Carlo gradient estimators and their use in adaptive stochastic gradient methods, with exercises.
---

# Multilevel MCMC Gradient Convergence and Multilevel Adaptive Stochastic Optimization

Use this skill when explaining or teaching:
- finite-time MCMC gradient estimation bias vs. computational cost,
- multilevel Monte Carlo (MLMC) for gradients,
- multilevel Adagrad / AMSGrad convergence under bounds on bias, second, and third moments,
- rate comparisons between standard adaptive gradient and MLMC-adaptive variants.

## Core Concept

In stochastic optimization, exact gradients are often intractable and are replaced by finite-time MCMC estimates. These estimates are biased, and naive bias reduction raises cost substantially.

A multilevel Monte Carlo (MLMC) gradient estimator breaks the MCMC estimate into a telescoping sum over increasing truncation levels. The key insight is that expensive high-accuracy estimators are averaged with many cheap low-accuracy estimators to control both bias and variance.

## Key Result (arXiv:2601.22799, 2026)

For a multilevel MCMC gradient estimator with maximal truncation level \(T_n\) at iteration \(n\):

- Bias decays as \(O(T_n^{-1})\)
- Expected computational cost grows as \(O(\log T_n)\)

Under conditions controlling:
1. estimator bias,
2. second moment,
3. third moment,

the resulting multilevel adaptive gradient algorithms achieve:

\[
\mathbb{E}[f(x_n) - f(x^*)] = O\!\left(\frac{\log n}{\sqrt{n}}\right),
\]

i.e., convergence rate \(O(n^{-1/2})\) up to logarithmic factors.

## Algorithmic Sketch

### Multilevel MCMC Gradient Estimator

Choose a sequence of truncation levels \(0 = L_0 < L_1 < \dots < L_m = T_n\). For each level \(l\), run an MCMC method for \(N_l\) steps to produce an estimate. The multilevel estimator is:

\[
\nabla f^{\mathrm{ML}}(x) = \sum_{l=1}^{m} \bigl(\mathbb{E}_\pi[\phi(x,\cdot) \mid \text{level } l] - \mathbb{E}_\pi[\phi(x,\cdot) \mid \text{level } l-1]\bigr),
\]

where level 0 is a very cheap rough approximation and level \(m\) is the most accurate.

Optimal allocation typically sets \(N_0\) large and roughly doubles \(N_l\) for higher levels.

### Multilevel Adaptive Variants

The estimator is plugged into:
- **Multilevel Adagrad**: accumulate squared past ML gradients per-coordinate.
- **Multilevel AMSGrad**: same with monotone long-term maximum window.

Convergence proofs require bounding:
- bias growth across iterations,
- gradient variance and higher moments under the adaptive cumulative sum.

## Comparison with Standard Methods

| Approach | Bias decay | Cost per iteration | Convergence rate |
|---|---|---|---|
| Single-level MCMC SGD | \(O(M^{-1})\) | \(O(M)\) | Depends on bias/variance balance |
| MLMC gradient + SGD | \(O(T_n^{-1})\) | \(O(\log T_n)\) | \(O(n^{-1/2} \log n)\) |
| Standard Adagrad | 0 | \(O(1)\) oracle | \(O(1/\sqrt{n})\) |
| Multilevel Adagrad | \(O(T_n^{-1})\) | \(O(\log T_n)\) | \(O(n^{-1/2} \text{ polylog})\) |

## Why This Matters

This framework is important whenever:
- stochastic-gradient training uses internal MCMC, e.g., variational inference with implicit distributions,
- adaptive optimizers must run with finite Monte Carlo burn-in without fully mitigating burn-in each iteration,
- one wants near-optimal cost/accuracy tradeoffs for randomized gradient methods.

## Proof Ideas and Exercises

1. **Moment bounds.** Assume each level estimator has bias \(b_l\), variance \(v_l\), and cost \(c_l = O(2^l)\). Show that choosing \(N_0 = O(1)\) and \(N_l = O(2^l)\) keeps the MLMC estimator variance constant while cost is \(O(m)\) and bias \(O(2^{-m})\). Exercise: derive the variance of the telescoping MLMC estimator.

2. **Convergence sketch.** Show that if the objective is smooth and the MLMC gradient is an unbiased estimator up to controlled bias and bounded second/third moments, then a Robbins–Monro step-size schedule yields \(O(n^{-1/2})\) rates. Exercise: write the one-line SGD iterate analysis under biased gradients.

3. **Adaptive amplification.** Compare Adagrad’s diagonal preconditioning term with constant and MLMC gradients. Explain why Adagrad’s adaptive step-size helps absorb small bias increments across iterations. Exercise: prove that Adagrad is robust to small uniform bias if bias satisfies a mild growth condition.

4. **Empirical side exercise.** On a small variational autoencoder or importance-weighted autoencoder objective, implement a deterministic gradient baseline, a single-level MCMC sampler with burn-in \(M\), and a two-level MLMC estimator. Plot convergence for fixed total wall-clock budget.

## Teaching Notes

- Start with standard MCMC gradient motivation, then introduce MLMC telescoping as a variance-reduction technique rather than a full-spectrum algorithm.
- Emphasize that the cost \(O(\log T_n)\) comes from doubling allocations across levels, tuning the same idea that makes multilevel Monte Carlo efficient for PDEs.
- If students are unfamiliar with Adagrad/AMSGrad, train only the convergence rate for SGD before adding adaptivity.

## Quick Reference

- Paper: Godichon-Baggioni et al., "Convergence of Multi-Level Markov Chain Monte Carlo Adaptive Stochastic Gradient Algorithms," arXiv:2601.22799, 2026.
- Subject: math.ST + optimization
- Key technical getters: MLMC gradient, bias \(O(T_n^{-1})\), cost \(O(\log T_n)\), rate \(O(n^{-1/2})\) up to logs.
