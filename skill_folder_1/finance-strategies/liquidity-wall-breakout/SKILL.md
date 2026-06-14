---
name: liquidity-wall-breakout
description: Teach liquidity wall breakout detection: constructing clustered limit-order walls from orderbook depth, identifying accumulation/defense/liquidation signatures, volume-confirmed breakout rules, and fade-versus-trend decisions.
---

# Liquidity wall breakout

Use this skill when you need a practical, execution-oriented workflow for detecting, validating, or trading orderbook liquidity walls and their breakouts.

## Core concept
A liquidity wall is abnormal concentration of resting limit orders near the bid or ask. It acts as support/resistance until absorbing orders consume it, traders cancel it, or liquidity providers fade. Breakouts from walls often lead to short-term directional moves when accompanied by completed trade volume.

## Step-by-step workflow

1. Scan for concentration
- Compute midprice and inspect size within 0.5%-2% of bid/ask.
- Use a multiplier, e.g., wall_size > 1.5x or 2x the mean resting size in that range.
- Merge nearby levels to avoid double-counting stackedLimitOrders.

2. Classify wall character
- Accumulation: small to medium trades consume the wall but the wall reappears at similar levels within minutes.
- Defense: large opposing orders reject price repeatedly.
- Liquidation-driven: wall vanishes after a single sweep with above-average executed volume.

3. Detect breakout
- Price closes past the wall on the relevant timeframe.
- Completed trade volume in the breakout candle exceeds recent average.
- Opposite-side depth is thinner than before breakout.

4. Decide setup direction
- Bullish breakout: bid wall breaks upward with buy execution delta positive.
- Bearish breakout: ask wall breaks downward with sell execution delta positive.
- Fade setup: if breakout volume is weak and depth returns quickly, fade the move back toward the wall.

## Monitoring and execution
- Timeboxing: 3-10 minutes for liquid markets; 10-30 minutes for lower timeframes or illiquid assets.
- Execution delta: compute net signed volume over the last N seconds to separate absorption from distribution.
- Fade rule: fade if post-breakout depth restores within 1-3 minutes and breakout volume is below a multiple of recent average, e.g., 1.25x.

## Risk management
- Size the position using wall height and breakout depth, not account balance.
- Set initial stop beyond the wall plus a spread buffer.
- Reduce exposure if time since breakout exceeds the timebox without follow-through.

## Pitfalls
- Stale quote walls in illiquid markets act as noise; increase size thresholds and minimum liquidity requirements.
- Breakouts during scheduled news, auction closes, or exchange status events have lower predictive value.
- Avoid trading small-cap or exotic markets where orderbook depth changes unpredictably.

## Verification
- Log candidate walls, wall_size_multiple, breakout_volume_multiple, breakout_time_minutes, and post-breakout depth_recovery_flag.
- Review weekly to tune thresholds and timebox rules by asset class and market regime.
