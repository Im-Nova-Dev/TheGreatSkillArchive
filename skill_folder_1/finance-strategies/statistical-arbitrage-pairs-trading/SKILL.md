---
name: statistical-arbitrage-pairs-trading
category: finance-strategies
description: Teaching skill for cointegration-based statistical arbitrage pairs trading in crypto markets. Covers Engle-Granger two-step, copula conditional probabilities, rolling walk-forward with FDR control, and production implementation pitfalls.
version: 1.0.0
tags:
  - quantitative-strategies
  - statistical-arbitrage
  - pairs-trading
  - cointegration
  - copula
  - crypto
---

# Statistical Arbitrage Pairs Trading Skill

## Overview
Teaching skill for cointegration-based statistical arbitrage pairs trading in crypto markets. Covers both traditional Engle-Granger + ADF z-score approach and the novel copula conditional probability method (Springer 2025) achieving 3.77 Sharpe on 5-min data.

## References
- `references/statistical-arbitrage-pairs-trading.md` — Full implementation details, benchmarks, checklist, and code skeleton

## Prerequisites
- Python: statsmodels, scikit-learn, pandas, numpy
- Data: High-frequency (1m/5m) OHLCV from single timestamp source
- Universe: Liquid perpetuals/spot vs BTC reference asset

## Core Concepts

### Cointegration vs Correlation
- **Cointegration**: Long-term equilibrium relationship (stationary spread)
- **Correlation**: Short-term linear dependence (spurious on non-stationary series)
- **Engle-Granger 2-step**: OLS y = βx + ε → ADF test on residuals ε

### Copula Conditional Probability Signals (Springer 2025)
- **Reference asset**: BTCUSDT (highly liquid, dominant market cap)
- **Spread**: Sᵢₜ = BTCUSDTₜ - β̂ⁱ Pⁱₜ
- **PIT transform** → fit copula (Tawn Type 1/2, BB7, BB8 best performers)
- **Signals**: h¹ᐟ² = ∂C(u₁,u₂)/∂u₂ = P(U₁ ≤ u₁ | U₂ = u₂)

## Implementation Pipeline
1. **Formation (3 weeks):** EG + KSS cointegration tests, rank by Kendall's τ, select top 2
2. **Trading (1 week):** Fit marginals → copula → conditional prob signals
3. **Rolling window:** 104 weekly cycles, 75% overlap, force-close week-end
4. **Parameters:** α₁ ∈ {10%,15%,20%} entry, α₂=10% exit

## Critical Production Rules
- **No look-ahead bias**: Shift rolling mean/std by 1 bar (QuantInsti)
- **Multiple testing**: Benjamini-Hochberg FDR at 5%
- **Transaction costs**: Explicit fees + slippage (min 5 bps/leg/side)
- **Clock sync**: Common timestamp source for cross-venue (Databento ts_recv)
- **Risk**: Equal capital per pair, stop-loss at z=±3.0

## Performance Benchmarks
| Strategy | Annual Return | Sharpe | Max DD |
|----------|--------------|--------|--------|
| Copula (5m, EG, α₁=20%) | 75.2% | 3.77 | -11.1% |
| Traditional Cointegration | ~35% | ~0.84 | -36% |

## Pitfalls to Avoid
1. Using correlation instead of cointegration for pair selection
2. Look-ahead bias in rolling z-score calculation
3. Ignoring multiple testing correction (false discovery rate)
4. Not modeling funding rates for perpetual futures legs
5. Insufficient transaction cost modeling

## Next Skill Enhancements
- Dynamic cointegration window optimization (AIC/BIC)
- Multi-asset portfolio construction (>2 pairs)
- Regime-aware adaptive thresholds
- CEX-DEX cross-venue stat arb (perps vs AMM pools)