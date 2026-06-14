---
name: delta-hedging-band
description: Teach delta hedging band strategy for options and short-gamma portfolios: band-based hysteresis rehedging, transaction-cost filtering, gamma-weighted thresholds, and crypto-specific adjustments for perps and DeFi options.
---

# Delta Hedging Band Strategy

Use this when managing delta exposure for option portfolios, market-making inventory, or structured-products books where continuous hedging is too costly.

## Core Concept

Continuous delta hedging is theoretically optimal but transaction-cost-heavy. A band-based rule tolerates small delta drift, only rehedging when delta breaches a cost-adjusted upper threshold. Lower threshold prevents whipsaw by requiring drift beyond a hysteresis band before the next hedge.

## Step-by-Step Workflow

1. Estimate gamma and realized volatility
   - Aggregate portfolio gamma Γ from positions.
   - Compute near-term realized volatility σ from 5–30 minute returns depending on rehedge horizon.

2. Compute cost-adjusted hedge threshold
   - Transaction cost per round trip: c ≈ half_spread × 2 in price units, scaled to notional.
   - Expected unhedged P&L drift: 0.5 × Γ × σ² × τ² × N where τ is the hedging interval and N is notional.
   - Hedge only if unhedged drift exceeds cost by a benefit multiplier, typically 1.5–2.0.

3. Apply band hysteresis
   - Lower band: do nothing when |Δ| < lower_band.
   - Watch band: tag exposure when lower_band ≤ |Δ| < upper_band and re-evaluate at next interval.
   - Upper band: execute hedge when |Δ| ≥ upper_band, then reset.

4. Execute and record
   - Route exposure offset via underlying spot, perp, or cross-hedge asset depending on cheapest-to-deliver.
   - Log pre-hedge delta, hedge cost, settlement price, and resulting delta residual.

## Crypto / DeFi Adjustments

- Perp hedging: include funding rate drag in transaction cost estimate.
- DeFi options: widen bands in low-liquidity markets and shrink bands when realized vol is elevated.
- Stablecoin collateral: hedge delta in collateral denomination to isolate market risk from peg risk.

## Risk Management and Verification

- Hard delta limit: enforce absolute aggregate delta cap at 1% of portfolio notional.
- Track hedged vs unhedged realized volatility capture; target capture ratio > 0.85.
- Measure hedging frequency reduction vs continuous hedge; target > 60% reduction with < 5% incremental P&L drag.
- Review band widths weekly as vol regimes and spread conditions change.

## Pitfalls

- Skipping cost estimation turns bands into arbitrary thresholds.
- During volatility spikes, bands sized for calm regimes will under-hedge.
- Forcing hedges at fixed time intervals instead of state-driven intervals creates calendar risk.
