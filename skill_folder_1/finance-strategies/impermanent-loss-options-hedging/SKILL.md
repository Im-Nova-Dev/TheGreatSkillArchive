---
name: impermanent-loss-options-hedging
description: >
  Hedge impermanent loss for AMM/DeFi liquidity providers using European vanilla options.
  Covers static model-independent replication, Uniswap V2/V3 payoff mechanics, and practical
  execution checklist.
category: finance-strategies
---

# Impermanent Loss Hedging with Options

## When to Use
- You are staking LP positions in Uniswap V2/V3 and want to hedge IL.
- Building structured products or vaults that need IL protection overlay.
- Pricing IL protection claims or LP incentive programs.

## IL Mechanics

### Uniswap V2
- CFMM: `x * y = L^2`
- Funded LP nominal IL: `IL_funded = sqrt(p_t/p_0) - 1`
- Borrowed LP nominal IL: `IL_borrowed = -0.5 * (sqrt(p_t/p_0) - 1)^2`

### Uniswap V3 (Concentrated)
- Active range `(p_a, p_b)` with liquidity `L`.
- P&L is piecewise; outside range, position becomes single-sided.

## Hedges

### Static (model-independent)
- Replicate IL protection claim with traded OTM European calls/puts.
- No price-process assumptions; perfect hedge if options market is liquid.

### Dynamic (model-dependent)
- Use BSM or log-normal SV for valuation.
- Derive delta/gamma for the IL claim and rebalance with spot or perps.

## Execution Checklist
1. Measure LP notional and current price relative to range/V2 midpoint.
2. Compute IL payoff shape at maturity.
3. Choose static portfolio of OTM options matching payoff convexity.
4. Rebalance hedge before funding windows or expected volatility spikes.
5. Size hedge to LP notional; review after large spot moves.

## Sources
- Lipton, Lucic, Sepp, "Unified Approach for Hedging Impermanent Loss of Liquidity Provision," arXiv:2407.05146, 2024.
