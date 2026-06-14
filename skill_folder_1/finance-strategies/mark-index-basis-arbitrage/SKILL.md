---
name: mark-index-basis-arbitrage
description: >
  Use when trading perpetual futures and you need to exploit mark/index basis divergences,
  size liquidation buffers, and route entries/exits around funding windows.
  Covers mark price construction, spoofing fingerprints, venue selection,
  and tactical short-at-spike setups. Centered on actionable execution rules.
---

# Mark/Index Basis Arbitrage and Liquidation Buffer Scheduling

Use this skill when continuous delta exposure makes liquidation buffer sizing and mark/index timing the primary risk drivers across CEX and DEX venues.

## 1. Core Definitions

- **Index price:** volume-weighted average of spot prices across 8-11 spot exchanges.
- **Mark price:** liquidation and unrealized PnL reference price. Incorporates index price, funding rate time value, moving-average basis, and venue-specific cushion.
- **Basis:** `mark_price - index_price`, expressed in absolute or percentage terms.

Standard formula elements:
```text
Mark Price = Median(
  Index × (1 + Funding Rate × Time to Funding / 8),
  Index + 2.5-min Basis MA,
  Contract Price
)
```

## 2. State Classification

```text
Normal    : rolling 20-bar absolute spread < 0.5%
Elevated  : 0.5% - 1.5%
Spike     : > 1.5%
```

Mark/index spread can diverge 0.5%-2% from the index during fast volatility without immediate arbitrage.

## 3. Trading Rules

### 3.1 Short-at-spike setup

- Trigger: `spike = True` for at least 2 consecutive updates AND funding >= 0.3% per 8hr interval.
- Entry: short perpetual at mark price; delta hedge with spot or cross-exchange perp.
- Exit condition: spread reverts to normal OR funding window closes and carry exceeds tolerance.
- Target capture: 0.5%-2% from mark/index mean reversion, not price direction.
- Timing constraint: avoid holding through funding checkpoint if post-spike funding is negative to longs.

### 3.2 Liquidation buffer sizing

- Maintenance margin = venue-specific minimum.
- Initial margin target:
  `initial_margin = maintenance_margin × (1 + 0.25 + max(0, (spread - 0.005) × 10))`
- Keep swing margin 20-25% above minimum to avoid cascade-triggered liquidation during mark spikes.

### 3.3 Spoofing detection

- Compute rolling ratio: `index_volatility / mark_volatility` over 20 bars.
- A ratio >= 3.0 is a spoofing fingerprint: mark volatility is artificially elevated without corresponding spot activity.
- Do not initiate new positions during suspected spoof events; wait for 2-bar confirmation of mean reversion.

## 4. Venue Routing Heuristic

Route heavy directional flow to venues with:
- Tight mark/index fencing (spike frequency is lower).
- Funding window aligned to your forecast horizon.
- Stable cross-venue time synchronization.

Avoid venues where funding and mark/index divergence co-move, since that amplifies cascade risk.

## 5. Joint Monitoring Checklist

1. Compute rolling 20-bar mark/index spread.
2. Compute rolling 20-bar `index_vol / mark_vol` ratio.
3. Track normalized funding greater than 0.3% per 8hr interval as an ER flag.
4. If funding ER and spread spike coincide, treat as elevated squeeze risk and reduce leverage.
5. Update liquidation cushion formula inputs before each funding checkpoint.

## 6. Execution Sequence

- If spike detected and funding post-window is negative: reduce size 15 minutes before checkpoint.
- If spike persists after funding: enter short with half notional; add on second spike bar.
- Delta hedge within the same venue or via cross-venue spot to avoid single-leg liquidation.
- Close short leg first if it is more liquid; otherwise close correlated proxy before primary.

## 7. Verification

- Record `spread`, `funding`, `index_vol`, `mark_vol`, `spike_flag`, and `liquidation_cushion` per entry and exit.
- After mean reversion, confirm PnL attribution: spread capture vs. funding drag vs. execution cost.
- Review `index_vol / mark_vol` ratio monthly to recalibrate spoof detection threshold.

## 8. Related Skills
- `finance-strategies/funding-rate-arbitrage`
- `finance-strategies/basis-trade-clawback-management`
- `finance-strategies/optimal-hedging-frequency`

## 9. References
- Session detail and source material: `references/2026-06-05-funding-freq-and-mark-index-basis.md`
