---
title: Orderbook Imbalance Metrics
name: orderbook-imbalance-metrics
description: >
  Teach orderbook microstructure indicators: OFI, depth-weighted imbalance,
  VPIN, queue-position models, and liquidity elasticity. Use when designing
  execution algorithms, microstructure signals, or liquidity analysis for
  equities and crypto derivatives.
triggers:
  - orderbook imbalance
  - OFI
  - VPIN
  - depth imbalance
  - queue position
  - liquidity elasticity
  - microstructure indicator
  - informed trading
---

# Orderbook Imbalance Metrics

## 1. Core Metrics

### 1.1 Order Flow Imbalance (OFI)
`OFI(t) = delta_bid_depth(t) - delta_ask_depth(t)`
- Positive OFI = buying pressure at the quote.
- Negative OFI = selling pressure at the quote.
- Best for: short-horizon signal generation and execution.

### 1.2 Depth-Weighted Imbalance
`(sum(bid_depth_1..N) - sum(ask_depth_1..N)) / (sum(bid_depth_1..N) + sum(ask_depth_1..N))`
- Multi-level extension of OFI.
- More robust to top-of-book manipulation.

### 1.3 VPIN (Volume-Synchronized Probability of Informed Trading)
- Trade-based bar aggregation reduces time-sampling bias.
- High VPIN = elevated informed flow -> volatility risk.
- Use trade bars: 1/50 of daily volume is common.

### 1.4 Expected Queue Position Cost
`slippage_estimate = queue_depth * avg_trade_size * adverse_selection_prob`
- Derives fill probability and expected impact.
- Ties to adverse-selection cost in execution.

### 1.5 Liquidity Elasticity
`elasticity = depth_change / mid_move`
- Inelastic liquidity: small mid move removes large depth.
- Elastic liquidity: depth recovers quickly after perturbation.

## 2. Signal Construction

### 2.1 OFI + VPIN regime filter
- Compute OFI and VPIN on rolling windows.
- Signal when OFI diverges from VPIN regime:
  - VPIN high + OFI negative -> supply-driven correction likely.
  - VPIN low + OFI positive -> demand-driven momentum pulse.

### 2.2 Depth-weighted breakout confirmation
- Track imbalance at 1%, 2%, 5% from mid.
- A breakout becomes high probability when:
  - imbalance persists across levels > 2% and
  - liquidity wall volume is absorbed and replenishment is weak.

## 3. Execution Tactics

### 3.1 Execution sizing
- Reduce slice size when:
  - VPIN > 0.7 (calibrated threshold)
  - queue position > 15% of visible depth
- Increase participation rate during elastic liquidity.

### 3.2 Timing entries
- Enter during OFI calibration stalls.
- Avoid entries during VPIN spikes unless fill urgency is high.

## 4. Risk and Robustness

### 4.1 Spoofing defense
- Apply time-decay: ignore depth added and canceled within 100-200ms.
- Use mid-price depth vs best-bid/ask depth.

### 4.2 Cross-venue consistency
- Normalize depth by queue length and price level.
- VPIN requires consistent tick pipelines.

## 5. Metrics and Reporting

Track monthly:
- OFIC (order flow imbalance correlation) by asset
- VPIN threshold backtest accuracy
- execution slippage vs queue-based estimate
- liquidity elasticity near entry levels

## 6. Teaching Exercises

1. Collect L3 orderbook for 1 day. Compute OFI and plot vs mid returns.
2. Build VPIN using trade bars. Backtest threshold for volatility events.
3. Compare spike-and-replenish patterns between inelastic and elastic assets.
4. Simulate queue-position cost under adverse-selection probability scenarios.
