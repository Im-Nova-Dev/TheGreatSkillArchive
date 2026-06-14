---
name: optimal-execution-and-impl-shortfall
description: Practical framework for measuring, decomposing, and reducing implementation shortfall in trade execution. Covers IS decomposition, VWAP/TWAP algo design, decision price conventions, participation rate pacing, urgency classification, impact-resilience tradeoffs, and execution quality benchmarking for equities, futures, and crypto.
metadata:
  author: hermes scheduled
  version: 0.1
---

# Optimal Execution & Implementation Shortfall

## Core Concept
Implementation Shortfall (IS) measures the difference between a theoretical benchmark price and realized execution economics. It decomposes into explicit costs (commissions, fees) and implicit costs (slippage, market impact, timing risk).

## 1. Implementation Shortfall Formula
Decision price convention:
- `IS = (P_decision - P_avg_execution) / P_decision`

Decomposition:
| Component | Formula | Interpretation |
|-----------|---------|-----------------|
| Explicit cost | `(c_usd + c_fee) / P_decision` | Known before execution |
| Delay cost | `(P_mid_start - P_decision) / P_decision` | Timing from decision to first fill |
| Market impact | `(P_mid_avg_execution - P_mid_start) / P_decision` | Volumes traded vs available liquidity |
| Opportunity cost | `(P_mid_end - P_avg_execution) / P_decision` | Leftover inventory vs mark price |

Benchmark alternatives:
- IS vs participation-priced VWAP: `IS_vwap = (P_vwap - P_avg_execution) / P_vwap`
- IS vs arrival mid: penalizes delay less, common in agency execution claims
- IS vs close price: used in benchmark portfolios requiring end-of-day completion

## 2. Algo Design: VWAP and TWAP Pacing
### VWAP Participation Rate
- Target participation rate: `r_part = alpha_i * |sigma_{30m}| / ADR_30m`, where `alpha_i` is urgency (0.1 conservative to 0.8 aggressive).
- Slice volume per bucket: `V_i = r_part * V_bucket`, where `V_bucket` is historical volume bin size.
- Adaptive: increase `alpha_i` when spread widens > 2× median or depth thins below 7-day min.

### TWAP Fallback
- Use when order book depth is unreliable (illiquid instruments, crypto exotic pairs).
- Add participation limit to prevent front-running: cap at `min(1.5 * avg_bucket_depth, 0.3 * ask_size_at_best)`.

## 3. Urgency Classification
| Urgency | % of order in first 15 min | Typical use case |
|---------|---------------------------|------------------|
| Passive | 3-8% | Single-stock strategies, low alpha |
| Normal | 10-20% | Rebalancing, benchmark tracking |
| Aggressive | 25-50% | High alpha, index tracking near close |
| Immediate | >50% | Forced liquidations, margin calls |

Aggressive urgency rules:
- Require alpha signal strength > threshold: `E[return] > 2 * impact_estimate + delay_cost`
- Use limit order with `limit = mid - 0.5 * spread` for bid-side buys to reduce adverse selection
- Switch to IOG (Immediate-or-Cancel) if book is 2× thinner than weekly average

## 4. Actionable Execution Tactics
### 4.1 Arrival-to-Mid Tracking
- Record `P_mid_arrival` when order is first sent.
- Recompute `P_mid_10s_rolling` at 10-second cadence.
- If `P_mid_10s_rolling - P_mid_arrival` exceeds `0.3 * spread`, reduce participation rate by 20% to avoid adverse flow.

### 4.2 Liquidity-Aware VWAP
- Compute reference VWAP using only historical volume from `9:30-10:30` when available.
- Scale participation by current depth: `adjusted_participation = target_participation * (depth_5 / avg_depth_5)`.

### 4.3 Impact-Resilience Check
- Pre-execution: estimate impact using Almgren-Chriss.
  - Temporary impact: `eta * Q`, where `eta = spread / depth_5`.
  - Permanent impact: `gamma * Q^alpha`, where `alpha ≈ 0.5-0.6 for liquid equities, 0.4 for crypto.
  - Total impact: `eta * Q + gamma * Q^alpha`.
- If estimated impact > 2 × manager-specified cost budget, split execution over ≥ 2 days.

## 5. Execution Quality Benchmarking

Report after each execution run:
- IS total bps: `(P_decision - P_avg_ex) / P_decision * 10000`
- IS vs VWAP bps: manager attribution score
- Fill rate: % of volume filled within trade date
- Time to 50%/90% fill: median / 90th percentile
- Delay cost bps: cost from `P_decision` to first fill
- Spread paid bps: average effective half-spread of fills relative to mid at fill time
- Opportunity cost bps: leftover inventory valued at end-of-day close vs filled average

Benchmark targets:
- IS ≤ 15 bps for large-cap equities, 30 bps for crypto major pairs at normal urgency
- IS vs VWAP ≤ 5 bps for agency-passive execution

## 6. Slippage Tolerance Calibration
- Set tolerance as `max(1.5 * rolling_5m_ATR, 2 * rolling_1h_median_spread)`, in price units.
- Raise tolerance 20% when depth < 50% of 30-day median.
- Record: tolerance used, rejected orders count, and subsequent opportunity cost.

## Verification
After implementation:
- Track IS weekly; reset monthly targets when alpha regime shifts.
- Calibrate eta/gamma monthly using realized fills and VWAP data.

## References / Data Sources
- Exchange OHLCV + tick/trade data.
- Historical volume profiles by time-of-day for TWAP/VWAP weighting.
- Almgren, Thum, Hauptmann, Li (2005): *Equity Market Impact*.

## Related Intel
- `/home/nova/.hermes/intel/finance/slippage-tolerance-and-order-execution-risk.md`
- `finance-trade-execution-and-slippage` skill
