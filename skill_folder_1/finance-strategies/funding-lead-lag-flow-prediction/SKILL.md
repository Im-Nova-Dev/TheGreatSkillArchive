---
name: funding-lead-lag-flow-prediction
description: Teach funding-lead-lag and flow-based short-term forecasting in crypto perpetual futures, including cross-venue funding rate lead-lag computation, lead thresholding, order flow confirmation, manipulation filters, and trade construction for 1–8 hour drift predictions.
metadata:
  author: hermes scheduled
  version: 0.1
---

# Funding Lead-Lag & Flow Prediction

## Why It Matters
Funding rates encode the cost of carry and directional pressure across venues. CEX funding rates lead DEX rates in ~61% of integrated windows, and funding spreads of >= 20 bps can predict short-term price drift when paired with aggressive order flow confirmation.

## Core Concepts

### 1. Normalized Funding Rate
Standardize across differing payment intervals to an 8h equivalent APY:

```
r_8h = rate * (8 / h)
APY = (r_8h * 3 * 365) / 100
```

### 2. Cross-Venue Lead-Lag
Compute pairwise lead-lag by cross-correlation over a 7-day rolling window:

```
lead_corr(i,j) = max_{lag in 0..6} corr(r_i_t, r_j_{t-lag})
```

- CEX funding rates typically lead DEX and mid-tier CEX venues.
- Use top 2 highest-correlation pairs as lead/lag indicators once correlation > 0.35 per hour samplings.

### 3. Short-Term Drift Signal
Trigger only when:
- `spread = max(e in E_s: r_e) - min(e in E_s: r_e) >= 20 bps`
- Spread `duration >= 2 funding windows` (>=16h for 8h funding)
- Leading venue changed sign in last 2 windows; lagging venue is delayed

Directional bias:
- Higher funding on lagging venue suggests traders expect price to rise there; expect short-term upward drift on the lagging venue.
- Lower funding on lagging venue suggests downward drift.

### 4. Order Flow Confirmation (CRITICAL)
Do not trade funding signals without same-side aggressive confirmation in the 20 minutes after the lead signal:
- Count marketable trades hitting the bid vs asking using trade-level tick data.
- `aggressor_side = sign(price - mid_at_trade)`
- Require `abs(sum(aggressor_signals)) >= 10` over 20-minute window.

Fade funding signals when:
- Total message rate exceeds `rolling_z > 2.5`
- Cancel-to-trade ratio in that window exceeds 3x the 30-minute baseline
- OBI age filter shows >60% of orders on the predicted side are <50ms old

### 5. Manipulation & Safety Filters
- Ignore funding rates exceeding ±5000 bps as API outliers.
- Require spread persistence >1 hour before entering; cut fast-reverting noise.
- Stop if `OI_change_30m < -0.10` on either leg or OBI imbalance flips.
- Cover when basis between spot and futures flips sign or when lead-lag cross-correlation drops below threshold for 2 windows.

## Trade Construction
- Notional: delta-neutral pair across lead and lag venues.
- Entry: enter at lead signal + order flow confirmation.
- Stop: when spread turns negative or OI drops >10% on either venue.
- Target/Exit: partial cover at cross-venue spread compression to 10 bps; full exit at sign flip or end of 4th hour if target not reached.
- Forced exit required in 95% of opportunities to avoid spread reversal losses.

## Formulas Summary
- `spread = max(r_e) - min(r_e)` over selected venues
- `APY = r_8h * 3 * 365 / 100`
- `lead_lag_corr(i,j) = max_{lag in 0..6} corr(r_i_t, r_j_{t-lag})`
- `aggressor_sum = sum(sign(price - mid_at_trade))` over 20-minute window

## Source of Truth
- `/home/nova/.hermes/intel/finance/funding-lead-lag-flow-prediction.md`
