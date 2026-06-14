---
name: market-microstructure-execution
description: >-
  Teach market microstructure and order execution concepts: microprice, queue-position
  modeling, adverse selection, implementation shortfall, and orderbook dynamics. Use when
  a task needs strategy logic built around market impact, fill probability, liquidity,
  or execution benchmarking against microstructure-based price benchmarks.
---

# Market Microstructure & Execution

**Definition:** Analyze orderbook snapshot behavior, microprice construction, queue depth,
and adverse selection so strategies can be expressed as executable logic rather than
abstract signal logic.

## 1. Core teaching topics
1. Microprice vs midprice and when to use each as benchmark.
2. Queue-depth fill modeling (exponential and power-law forms) with per-asset calibration.
3. Adverse-selection signals from ledger-level L2 data (cancels, fills, imbalance thresholds).
4. Implementation shortfall decomposition: timing, market impact, and opportunity cost.
5. Routing rules: when to post passively and when to cross the spread aggressively.

## 2. Level 2 data pipeline
1. **Ingest** L2 updates (price, qty, side, operation insert/update/delete, sequence number).
2. **Validate** sequence ordering; reject stale/fragmented frames.
3. **Wash-trade correction** on each book snapshot:
   - Match orders with equal price, opposite side, time overlap.
   - Zero out paired quantities, keep unmatched for imbalance tracking.
4. **Aggregate to features** at target frequency (10 ms, 100 ms).
5. **Forward-fill** gaps only up to a staleness cap (e.g., 3 seconds).

## 3. Microprice implementation
```
P_micro = (P_best_ask * Q_best_bid + P_best_bid * Q_best_ask) / (Q_best_bid + Q_best_ask)
P_mid   = (P_best_bid + P_best_ask) / 2
delta   = (P_micro - P_mid) / P_mid
```
- When |delta| > baseline, book imbalanced enough to trade toward microprice.
- Convergence half-life: microprice reverts to mid within 2–5 ticks under balanced regimes.

## 4. Queue-position fill model
**Exponential decay (start):**
```
P_fill(queue_depth) = exp(-alpha * queue_depth)
```
**Power-law fallback:**
```
P_fill(queue_depth) = queue_depth^(-beta)
```
- Calibration: fit on historical cancel/fill outcomes per asset per time-of-day regime.
- Validation: rank-orders fills vs non-fills matches model probability well (Kendall tau > 0.2).
- Use quantile bucketing if sample size is small (< 1k queued orders).

## 5. Adverse-selection trigger
| Condition | Signal direction |
|---|---|
| Imbalance >= +2 sigma | Buy aggression expected within 100–500 ms |
| Imbalance <= -2 sigma | Sell aggression expected |
| Cancel-rate spike at head | Passive placement is being picked off |
| Depth shadow drop at best bid/ask | Opposing wall about to be consumed |

## 6. Execution tactics
- **Cap passive size:** Keep order <= 15–20% of displayed depth at level to avoid dominance
  and front-running exposure.
- **Smart price benchmark:** Use microprice for immediate performance; midprice for day-scale
  P&L reporting.
- **Queue snapping defense:** If cancel-rate head rises > baseline, widen limit or switch to
  aggressive market order within next N milliseconds.
- **Imbalance threshold (tunable):**
  - start at +2.0 sigma for initial signal
  - scale by inverse of spread normalized by price = (best_ask - best_bid) / price
- **Submission profile:** 1st passive attempt, 2nd micro-timed reprice, 3rd aggressive fallback
  within a 300 ms window before re-evaluating.

## 7. Common pitfalls
1. Treating midprice as execution benchmark (adds micro noise to implementation shortfall).
2. Modeling fill without cancel-rate conditioning (causes >40% error in queue-position estimates).
3. Using only top-of-book features; depth beyond best levels predicts reversals and flow toxicity.
4. Ignoring latency tiers: latency > 3 ms vs <= 1 ms changes effective fill rate by ~25% in crypto.
5. Overfitting alpha thresholds on one asset; always validate on at least 3 sibling instruments.

## 8. Metrics to track
| Metric | Target | Alert threshold |
|---|---|---|
| Implementation shortfall vs microprice | < 0.1% | >= 0.2% |
| Passive fill rate | > 35% | < 25% |
| Adverse selection contribution | < 40% of shortfall | >= 55% |
| Queue depth ratio (order size / depth) | 10–20% | > 30% or < 3% |
| Cancel rate at head (per second) | < baseline | > 2x baseline |

## 9. Delivery checklist
- [ ] Calculation of P_micro, P_mid, and delta per monitoring tick is correct.
- [ ] Fill model chosen: exponential or power-law fit tracked in repo.
- [ ] Adverse-selection thresholds expressed as z-scores computed on trailing lookback.
- [ ] Execution policy determines aggressor/passive/reprice branch explicitly.
- [ ] Metrics definitions documented for equivalent computation across backtest and live.
- [ ] Validation uses multi-asset out-of-sample data.
