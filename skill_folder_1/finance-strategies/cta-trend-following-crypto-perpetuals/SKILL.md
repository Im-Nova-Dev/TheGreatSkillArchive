---
name: cta-trend-following-crypto-perpetuals
description: Teaching skill for CTA trend-following strategies on crypto perpetuals (Donchian channels, moving average crossovers, breakout systems)
category: finance-strategies
tags: [cta, trend-following, crypto, perpetuals, donchian, breakout, moving-average]
---

# CTA Trend-Following on Crypto Perpetuals

## Overview
This skill teaches systematic Commodity Trading Advisor (CTA) trend-following strategies adapted for crypto perpetual futures markets, drawing on academic research and practitioner methodologies.

## Core Concepts

### 1. Ensemble Donchian Channels (Zarattini et al., 2025)
- Multiple Donchian channel lookback periods aggregated into a single composite signal
- Reduces single-parameter sensitivity
- Applied to rotational portfolio of top 20 liquid coins
- Volatility-based position sizing essential for crypto's extreme regime changes
- Achieved Sharpe > 1.5 net-of-fees, 10.8% annualized alpha vs Bitcoin

### 2. Short-Term + Market-Beta Model (Benhamou et al., 2025)
- Bayesian graphical model tracking short-term trend, long-term trend, and market-beta exposures
- **Key finding**: MKT+STT (Market + Short-Term Trend) outperforms classic multi-month breakouts
- Short-term trend (10/20/40/60-day) has only 0.24 correlation with market beta — convex payoff cushions during regime shifts
- Optimal weight: ~17% short-term trend, ~83% long-term trend for Sharpe maximization

### 3. Lookback-Straddle Trend Score
- Trend score = delta of fixed-window lookback straddle under GBM
- Scale-free sensitivity via z-scores rescaled by diffusion scale σ√n
- Directional signal: T ≈ +1 near upper boundary, T ≈ -1 near lower, T ≈ 0 for sideways

## Implementation Framework

### Signal Generation
```python
# Multiple Donchian lookbacks
lookbacks = [10, 20, 40, 60, 120, 250, 500]  # days
signals = []
for lb in lookbacks:
    upper = high.rolling(lb).max()
    lower = low.rolling(lb).min()
    signal = (close - lower) / (upper - lower) * 2 - 1  # normalize to [-1, 1]
    signals.append(signal)

# Ensemble: equal-weight or volatility-weighted average
ensemble_signal = np.mean(signals, axis=0)
```

### Volatility-Based Position Sizing
```python
# Target volatility scaling
target_vol = 0.15  # 15% annualized
realized_vol = close.pct_change().rolling(20).std() * np.sqrt(252)
position_size = target_vol / realized_vol
position_size = position_size.clip(0, 2.0)  # cap at 2x
```

### Transaction Cost Mitigation
- Limit trading to top 20 most liquid perpetuals
- Use time-weighted averaging for signal changes
- Implement minimum holding period (e.g., 4-8 hours) to reduce overtrading
- Consider funding rate as implicit carry cost

## Crypto-Specific Considerations

1. **Funding Rate Integration**: Perpetual funding rates create carry drag/benefit
   - Long positions pay funding when rate > 0, reducing trend profit
   - Incorporate funding into signal: net_trend = raw_signal - funding_cost_adjustment

2. **24/7 Markets**: No overnight gaps but weekend liquidity thinning
   - Adjust volatility estimators for continuous trading
   - Consider session-based volatility (Asian/European/US)

3. **Liquidity Tiering**: Top 10 vs 10-20 liquidity gap significant
   - Size positions by adv20 (average daily volume 20-day)
   - Maximum position = 1% of adv20 or fixed notional cap

4. **Correlation Structure**: Crypto trend-following has low correlation with traditional CTA
   - Diversification benefit for multi-asset portfolios
   - BTC/ETH dominate corr matrix; altcoins add idiosyncratic risk

## Backtesting Framework
- Survivorship bias-free universe (all coins traded since 2015)
- Realistic transaction costs: 5-10 bps taker, 2-5 bps maker
- Funding rate simulation from historical funding data
- Walk-forward optimization with expanding window
- Out-of-sample validation on post-2022 data

## Key Metrics for Evaluation
- Sharpe ratio (net of all costs)
- Maximum drawdown and drawdown duration
- Calmar ratio (return/maxDD)
- Correlation with BTC and traditional CTA indices
- Turnover and capacity estimates

## References
- Zarattini, Pagani, Barbon (2025): "Catching Crypto Trends: A Tactical Approach for Bitcoin and Altcoins" — SSRN 5209907
- Benhamou et al. (2025): "Re-evaluating Short- and Long-Term Trend Factors in CTA Replication" — arXiv:2507.15876v1
- Man Group / Graham Capital / CME Group trend-following primers