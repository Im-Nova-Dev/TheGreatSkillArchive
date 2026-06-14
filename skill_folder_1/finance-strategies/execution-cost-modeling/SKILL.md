---
name: execution-cost-modeling
description: >
  Teach execution cost modeling for single-asset and cross-asset trading.
  Covers explicit fees, implicit costs (slippage, market impact, timing risk),
  spread capture, latency cost, venue/strategy constraints, cross-asset overlay,
  and execution analytics.
hero: false
---

# Execution Cost Modeling

Use this skill to estimate, reduce, and explain the full cost of executing a trade
or a trading strategy before considering alpha, not after.

## 1. Cost Taxonomy

### Explicit Costs
- Fees: commission, clearing, exchange, broker platform.
- Taxes: transaction tax, slippage taxation in local jurisdictions.

### Implicit Costs
- Spread cost: half the spread at entry and exit.
- Market impact: temporary + permanent price movement.
- Timing risk: holding period cost, gap risk.
- Latency cost: faster execution reduces queue exposure.
- Opportunity cost: missed fills vs. price improvement.

## 2. Cost Model Formula (Single Leg)

```
Total Cost ~= 0.5 * Spread + Impact + TimingRisk + Fees + Latency
```

- Spread: bid-ask mean, or depth-weighted microprice.
- Impact: square-root or power law of participation rate vs. ADV.
- TimingRisk: sigma * sqrt(holding_hours / 252 * 6.5) for equities.
- Fees: flat + tiered/volume schedule.

## 3. Market Impact Models

### Almgren-Chriss Framework (institutional orientation)
```
Impact = gamma * sigma * sqrt(T) + eta * sigma * participation
```
- `gamma`: temporary impact coefficient
- `eta`: permanent impact coefficient
- `T`: horizon in days
- `sigma`: daily volatility
- `participation`: fraction of ADV

Adjust parameters by venue, asset class, and regime (high vol = higher impact).

### Simple Square-Root Impact Estimate
```
Impact ≈ c * sigma * sqrt(Q / ADV)
```
- `Q`: order quantity
- `c`: 0.1 -> 0.3 typical for liquid equities

## 4. Cross-Asset Cost Considerations

### ETF vs Cash Equities
- ETF arbitrage cost: creation/redemption fee + bid-ask spread on basket.
- Tracking error cost: management fees, cash drag, rebalance costs.

### Futures Basis
- Carry cost: dividend or yield adjustment.
- Convergence cost: basis mean-reversion speed vs. roll timing risk.

### FX Spread Cost
- Bid-ask as % of notional; reduce with limit orders or algorithms.
- Avoid stacking small orders into liquidity walls.

### Crypto Derivatives
- Perpetual swap funding rate drag.
- Funding basis vs spot cost; check holding period advantage.

## 5. Execution Strategies by Cost Driver

| Driver               | Mitigation                               |
|---------------------|------------------------------------------|
| Spread              | Limit orders, mid-price, DLP routing     |
| Impact              | Slicing, TWAP/VWAP, Iceberg             |
| Timing risk         | Accelerate when signal decays fast       |
| Latency             | Colocation, FIX, priority fee             |
| Fees                | Tiered pricing, maker vs taker rebates   |

## 6. Advanced Topics

### Implementation Shortfall (IS)
```
IS = (DecisionPrice - ExecutionPrice) / DecisionPrice - Bench
```
- Benchmark: arrival, VWAP, or close.
- Components: delay cost, fees, impact, regret.

### Optimal Execution Horizon
- Minimize `gamma * sigma * sqrt(T) + eta * sigma * (X / T) + lambda * T`
  where `X` is total quantity and `lambda` is risk aversion.

### Liquidity-Aware Cost Bucketing
- Split cost by: order book depth, time of day, venue, and execution algo.

### Execution Risk-Adjusted Performance
- Convert alpha estimate into Sharpe as:
  ```
  Sharpe ≈ (ExpectedReturn - TotalCost) / ExecutionVolatility
  ```

## 7. Teaching Exercises

### Exercise 1: Cost Calculator
Build a cash-equity estimator:
- inputs: spread, sigma, Q, ADV, fees, horizon (hours)
- outputs: expected slippage, impact, total cost bps

### Exercise 2: Impact Parameter Fit
Given historical fills and ADV, fit `c` in simple sqrt model.

### Exercise 3: Cross-Asset Trade
Compare ETF vs cash execution for a basket of 50 names.

### Exercise 4: Optimal Horizon
Given `sigma`, `gamma`, `eta`, compute T that minimizes cost.

## 8. Common Pitfalls

- Ignoring temporary vs permanent impact.
- Using close price as decision price when trading near close.
- Treating ADV as static; liquidity regimes cluster.
- Neglecting latency exposure in macro or volatility events.
- Assuming spread = quoted half-spread; depth-weighted gap matters.

## 9. Verification Checklist
- [ ] All explicit costs included.
- [ ] Impact model calibrated to recent regime.
- [ ] Cross-asset basis/funding included.
- [ ] Horizon vs impact tradeoff analyzed.
- [ ] Sensitivity to ADV and participation tested.
