---
name: signed-volume-toxicity
description: >
  Use when designing short-horizon execution logic, routing orders,
  or teaching how trade flow composition predicts immediate adverse drift.
  Covers signed volume imbalance, participation decay, adverse-selection window,
  volume clustering, and actionable substitution rules for execution venues.
metadata:
  author: hermes scheduled
  version: 1.0
---

# Signed Volume Toxicity for Short-Horizon Execution

## Concept
Signed volume toxicity captures whether recent trades are leaning on one side
of the book in a way that predicts near-term price drift. It complements
static orderbook imbalance by measuring post-trade flow pressure and
participation decay in the minutes after execution.

## Core Metrics
- Signed Volume Imbalance (SVI):
  `(buy_trade_volume - sell_trade_volume) / total_trade_volume` over a rolling window.
- Trade Participation Decay:
  `volume_away_from_mid / volume_at_or_near_mid`. Rising values mean larger trades
  are crossing the spread instead of interacting with the quote.
- Adverse Selection Window:
  Midprice move in the 500 ms post-trade interval, signed by trade direction,
  compared to contra-side depth within 0.25%.
- Volume Clustering Ratio:
  Share of window volume executed in the top 5 trades versus a uniform baseline.
  Higher values correlate with institutional or forced-flow events.

## Operational Usage
1. Slice urgency control:
   - SVI near +/- 0.6 or higher => reduce aggression.
   - Prefer passive participation when toxicity is high.
2. Venue routing substitution:
   - Prefer lit venues when hidden-trader footprint is elevated.
   - Reduce dark-pool aggressiveness when participation decay is above median.
3. Cost estimate expansion:
   - Widen expected implementation shortfall by 15-35% when toxicity is in
     the top quartile and spread is compressed.
4. Regime gating:
   - Solid executed SVI + spread compression + declining depth = active toxicity regime.
   - Combine with realized volatility filter to avoid fakeout moves.

## Skill-Driven Checklist
- [ ] Compute SVI and participation decay on 30-second and 1-minute horizons.
- [ ] Flag an active toxicity regime when at least two metrics exceed thresholds.
- [ ] Adjust execution plan based on regime rather than narrative.
- [ ] Validate post-trade by comparing realized slippage to toxicity-adjusted forecast.
- [ ] Log toxicity regime and chosen venue to execution ledger for attribution.

## Macro and Market Structure Link
Toxicity spikes frequently align with deleveraging waves, macro announcements,
and funding-rate volatility in crypto markets. A short-horizon toxicity filter
acts as a micro-liquidity stress overlay on top of broader regime filters.

## Example Trigger Table
| Condition                                  | Action                              |
|---------------------------------------------|-------------------------------------|
| SVI > 0.65, spread near low                 | Reduce limit aggression, widen clip |
| Participation decay > median + 1 std dev    | Prefer lit over dark pool routing   |
| Adverse selection window > 0.25% midsigned  | Suspend aggressive slicing          |
| Volume clustering ratio > 1.4x baseline     | Treat as informed-flow risk         |

## Source-of-Truth Intel
- `/home/nova/.hermes/intel/finance/2026-06-05-signed-volume-toxicity.md`
