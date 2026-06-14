---
name: short-term-reversal-at-extremes
description: 'Teach short-term reversal at rolling session extremes using microstructure signals: disposition-effect detection, orderbook imbalance, queue depth, and stop-loss/take-profit construction. Encodes actionable entry, filter, and regime rules for quant execution.'
metadata:
  author: hermes scheduled
  version: 0.1
---

# Short-Term Reversal at Session Extremes

## Why It Matters
Retail and leveraged traders exhibit the disposition effect: selling winners too early and holding losers too long. This creates predictable short-term reversals at weekly highs/lows and 5% extremes, exploitable with microstructure filters.

## Core Concepts

### 1. Session Extreme Identification
Rolling extremes provide reversal anchoring points.

```
high_5d = rolling_max(close, 5 sessions)
low_5d  = rolling_min(close, 5 sessions)
distance_to_extreme = (close - high_5d) / atr(14)
```

### 2. Disposition Score
Measures clustering of contrarian flow near extremes.

```
disposition_score =
  signed_volume_near_extreme(last_3_sessions)
  - signed_volume_near_midpoint(last_3_sessions)
```

### 3. Queue Depth Filter
Liquidity at extremes is often thin. Use best bid/ask queue depth and queue age.

### 4. Reversal Probability Edge
- CTR > 2.5 + top-5 depth drop ≥ 35% → liquidity stress.
- Queue depth shallow + near extreme → mean reversion probability rises.
- Combined with aggressor imbalance, these signals reduce false flags.

## Actionable Rules

### Entry
1. Compute rolling 5-session high/low and classify current close relative to it.
2. Compute disposition score over last 3 sessions.
3. Require microstructure confirmation:
   - CTR in 5s window < 2.5
   - Top-5 depth recovery time < 5s if depth dropped
   - Best bid or ask queue depth not exhausted
4. Enter contrarian:
   - Fade long at resistance when disposition score > +threshold
   - Fade short at support when disposition score < -threshold

### Position Sizing
```
size = base_size * (1 + atm_iv / 0.20)
stop = 1 * atr(14)
target = 1.5 * atr(14) to 2 * atr(14)
```

### Regime Filters
- Do not trade during FOMC, CPI, or macro windows above expected surprise.
- Ignore instruments with median daily notional below liquidity threshold.
- Cut exposure if bid-ask spread exceeds 2× 30-day median.

## Formulas Summary
- `distance_to_extreme = (close - high_5d) / atr(14)`
- `disposition_score = signed_volume_near_extreme - signed_volume_near_midpoint`
- `CTR = canceled_quote_size / traded_size` over 5s–10s window
- `size = base_size * (1 + atm_iv / 0.20)`
- `stop = 1 * atr(14)`, `target = 1.5 * atr(14)`

## Risk Filters
- Disable execution during macro announcement windows.
- Ignore penny stocks / illiquid tokens.
- Cap exposure when spread exceeds 2× median.

## Data Sources
- L2 orderbook with timestamped actions (add/modify/delete).
- Trade tick data with signed aggressor flag.
- Rolling session high/low and ATR.

## Source of Truth
- `/home/nova/.hermes/intel/finance/disposition-effect-and-short-term-reversal.md`
