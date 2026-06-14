# Statistical Arbitrage / Pairs Trading in Crypto - Reference

**Date:** 2026-06-06
**Category:** Quantitative Strategies / Statistical Arbitrage
**Sources:** Databento (2025-02), Springer Financial Innovation (2025-01), QuantInsti (2025)

## Key Insights

### 1. Cointegration ≠ Correlation
- Correlation fails on non-stationary price series (spurious correlations)
- Cointegrated series track closely long-term despite short-term correlation variations
- Two-step Engle-Granger: OLS regression y = βx + ε, then ADF test on residuals ε

### 2. Novel Copula-Based Approach (Springer 2025)
- Uses BTCUSDT as reference asset for stationary spread processes
- Spread: Sᵢₜ = BTCUSDTₜ - β̂ⁱ Pⁱₜ
- Solves continuity violation in low-liquidity assets (frequent zero 5-min returns)
- 5-min data with EG test + α₁=20% entry → 205.9% total return, Sharpe 3.77

### 3. Implementation Pipeline (Rolling Walk-Forward)
1. **Formation (3 weeks):** Test cointegration (EG linear, KSS nonlinear), rank by Kendall's Tau, select top 2
2. **Trading (1 week):** Fit marginals → PIT → fit copula → conditional probability signals
3. **Signal Rules:** h¹ᐟ² < 0.5-α₁ & h²ᐟ¹ > 0.5+α₁ → Long S¹, Short S²
4. **Parameters:** α₁ ∈ {10%,15%,20%} entry, α₂=10% exit

### 4. Critical Production Requirements
- **No look-ahead bias:** Shift rolling variables by 1 day (QuantInsti)
- **Multiple testing control:** Benjamini-Hochberg FDR at 5%
- **Transaction costs:** Model explicitly (5 bps/leg/side minimum)
- **Clock sync:** For cross-venue, use common timestamp source (Databento ts_recv)

### 5. Performance Benchmarks (Out-of-Sample)
| Strategy | Annual Return | Sharpe | Max DD |
|----------|--------------|--------|--------|
| Copula (5m, EG, α₁=20%) | 75.2% | 3.77 | -11.1% |
| Traditional Cointegration | ~35% | ~0.84 | -36% |
| Buy & Hold BTC | Variable | ~1.0 | -50%+ |

## Actionable Implementation Checklist

- [ ] Data: High-freq (1m/5m) OHLCV from single timestamp source
- [ ] Universe: Liquid perpetuals or spot pairs vs BTC reference
- [ ] Cointegration: EG + ADF (p<0.05) + KSS (critical -1.92)
- [ ] Hedge ratio: Rolling OLS with 100-bar window
- [ ] Spread: y - βx, z-score with rolling mean/std (shifted 1)
- [ ] Entry: |z| > 1.5 (traditional) or copula conditional prob thresholds
- [ ] Exit: z crosses 0 (traditional) or copula exit rules
- [ ] Risk: Equal capital per pair, force-close end of period, stop-loss at z=±3
- [ ] Costs: Include exchange fees, slippage, funding rates for perps

## Next Research Targets
1. Dynamic cointegration window optimization (AIC/BIC lag selection)
2. Multi-asset portfolio construction (beyond 2-pair limit)
3. Regime-aware adaptive thresholds (volatility/liquidity regimes)
4. CEX-DEX cross-venue pairs (perps vs AMM pools)