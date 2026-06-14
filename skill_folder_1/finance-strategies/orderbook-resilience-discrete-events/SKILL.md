---
name: orderbook-resilience-discrete-events
description: Teach orderbook resilience around discrete liquidity events: liquidation cascades, flash crashes, news spikes, and auction gaps. Includes two-regime decomposition, depth recovery lags, spread-only metric flaws, execution-quality scoring, and MM parameter adaptation.
---

# Orderbook resilience around discrete liquidity events

Use this skill when you need to measure, model, or trade around post-event orderbook recovery on CEX or DEX venues, especially perpetual futures venues subject to liquidation cascades.

## Core concept

Liquidity recovery is not uniform across orderbook dimensions. After a discrete shock (liquidation cascade, flash crash, news spike), quoted spreads typically revert quickly while resting depth contracts persistently. Treating spread recovery as full liquidity recovery systematically underestimates post-event execution costs.

## Two-regime framework

### Regime 1: Pricing liquidity (fast)
- Quoted spread reversion to pre-shock levels within days.
- Midprice and microprice recover rapidly as arbitrageurs return.
- Tighter spreads signal reduced adverse-selection risk.

### Regime 2: Inventory liquidity (slow)
- Market-maker depth at best bid/ask contracts for 1–3+ weeks.
- Net quoting size stays depressed even as spreads widen competitive.
- Depth recovery often follows an exponential decay with halflife ~7–21 days depending on venue and asset.

## Measurement protocol

1. Track spread quantiles: median, 75th percentile, 95th percentile quoted spread at minute frequency.
2. Track depth metrics: size at best bid/ask, cumulated size within 0.5%, 1%, and 2% of midprice.
3. Classify state after each event:
   - If spread < 1.2x pre-event AND depth > 0.8x pre-event: regime 1, pricing recovered.
   - If spread < 1.2x pre-event AND depth < 0.8x pre-event: regime 2, inventory impaired.
   - If spread > 1.2x pre-event: full stress, both regimes impaired.

## Execution-quality scoring

Legacy TCA:
- Execution quality = weighted fill price vs arrival midprice.

Corrected post-event TCA:
- Include depth-adjusted impact: estimated market impact = sigma * sqrt(size / depth_at_level).
- Adjust for regime 2 by applying depth haircut factor: `depth_factor = max(0.5, depth_ratio)` if spread appears recovered but depth is impaired.

## Market-making adaptation after cascade

- Spread target: maintain competitive quoted spreads to reclaim market share.
- Quote size: reduce by 20%–40% vs. pre-cascade to reflect slower inventory recovery.
- Skew: widen passive side on the thinner quote size to manage inventory.
- Time horizon: expect 2–4 weeks before depth normalization allows full risk capacity.

## Crypto and perpetual futures specifics

- Dynamic margin requirements can trigger forced deleveraging even when spread looks normal.
- Funding-rate spikes often coincide with or follow liquidation cascades, compounding inventory stress.
- On-chain DEX venues may exhibit slower depth recovery than CEX due to lack of HFT maker coordination.

## Actionable rules

1. Post-cascade classification: compute spread_ratio and depth_ratio 1 hour after event ends.
2. If spread_ratio < 1.2 and depth_ratio < 0.8, route flow to deeper venue or use TWAP sizing.
3. Set depth recovery target before restoring full position limits: `target_depth = 0.85 * pre_event_depth`.
4. Reassess market-making risk limits weekly until both spread and depth ratios exceed thresholds for 5 consecutive days.

## Pitfalls

- Spread-only metrics after cascade overstate execution quality.
- Depth metrics require normalization by volatility; threshold should widen in high-vol windows.
- OTC/block flow can temporarily inflate apparent depth without improving executable depth.

## Verification

- Track predicted vs actual execution cost under both regime classifications.
- Calibrate depth halflife by venue and asset using exponential decay model on post-cascade depth ratio.
- Log number of execution-hours where regime 2 was active but flow was treated as regime 1.
