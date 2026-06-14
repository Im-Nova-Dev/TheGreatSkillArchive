---
name: queue-position-liquidity-tails
description: Teach queue position analysis, liquidity tails, and hidden liquidity detection in limit order books for execution quality and short-term alpha. Use when designing or evaluating order execution, microstructure signals, or adverse-selection hedging.
---

# Queue Position and Liquidity Tails in LOBs

Use this skill to assess execution risk, predict short-term volatility, and improve order routing decisions by analyzing queue depth, quote age, hidden liquidity, and cancellation clustering.

## 1. Quote-age decay and fill latency
- Resting limit orders submitted far from the touch or into lightly populated queue levels exhibit longer fill latency.
- As the order ages, the probability of adverse selection rises unless it is refreshed or canceled.
- **Action:** compute an effective queue depth that discounts visible depth by quote age, e.g., `effective_depth = f(visible_depth, age_in_events)`.

## 2. Queue-position convexity
- Orders near the inside quote experience convex fill-time behavior:
  - adverse flow → queue can be swept quickly;
  - benign flow → partial fills at better prices may occur.
- **Action:** monitor number of units ahead in the queue and use it to adjust order aggressiveness or split size decisions.

## 3. Hidden liquidity and iceberg detection
- A thin visible book can mask large hidden orders.
- Hidden liquidity presence can be inferred via:
  - execution-at-quote larger than visible depth added in the same interval;
  - probing tests with small marketable orders;
  - comparing executions at unchanged best quote versus advertised size.
- **Action:** when hidden liquidity is detected, reduce aggressive order flow and widen protective stop distances.

## 4. Liquidity elasticity and cancellation signals
- Sudden cancellations of depth ahead in the queue signal liquidity withdrawal and upcoming volatility.
- Compute a rolling cancellation/refresh ratio at each price level; spikes predict quote shaving and widening spreads.
- **Action:** when cancellation heat index rises, shift to marketable orders only with tighter size and stop-loss triggers.

## 5. Cross-venue queue inference
- For multi-venue assets, compare queue build-up and fill rates across lit venues.
- Persistent divergence can indicate latency arbitrage or H2L routing that exposes resting orders.
- **Action:** prefer venues where resting liquidity has been stable and queue replenishment is high.

## 6. Metrics and formulas
- Effective queue depth = visible depth at best quote minus stale/aged orders.
- Hidden liquidity proxy = sum(executions at unchanged best quote) - visible depth added, over interval.
- Cancellation heat index = canceled depth at level / total depth canceled across levels, over last k events.

## 7. Integration
- Combine with OFI/MLOFI by weighting OFI by front-of-queue depth ratio to estimate realistic impact.
- Use cancellation heat to adjust volume-profile breakout filters around HVN/LVN levels.
- Apply hidden-liquidity signal as a de-risking filter in funding-rate and pairs strategies.

## Sources
- OFI/MLOFI and price impact research: Cont et al., 2010; Su et al., 2021; Xu et al., 2019.
- Empirical LOB microstructure studies on cancellation, refresh, and iceberg detection.
