---
name: basis-trade-clawback-management
description: >
  Use when a basis/carry trade turns adverse and you need a defensive exit decision tree,
  collateral-aware sequencing, and conditional reactivation logic. Covers crypto perpetual
  basis trades, spot-futures arb, delta-neutral carry structures, funding-rate blowups,
  borrow/recall risk, and margin-liquidity sequencing. Centered on actionable metrics,
  not commentary.
---

# Basis Trade Clawback Management

When a delta-neutral basis trade's negative leg drawdown approaches the allocated gain buffer, do not stay passively delta-neutral. Switch to clawback mode: sequence exits by liquidity and collateral needs, and reactivate only when the basis spread exceeds the entry level plus a compensating buffer.

## 1. Clawback Trigger

Capture normalized funding metrics first.

```python
def clawback_trigger(trade, funding_series, basis_series, vol_window=20):
    net = (funding_series['spot'] - funding_series['perp']).dropna()
    vol = net.rolling(vol_window).std().iloc[-1]
    signal = -net.iloc[-1] / vol if vol > 0 else 0
    basis_blown = abs(basis_series.iloc[-1]) / trade.entry_basis
    return signal > 1.5 and basis_blown > 1.0
```

Clawback mode is entered when:
- The negative leg P&L exceeds ~60% of the basis gain buffer, AND
- The absolute basis has compressed / inverted enough that carry no longer offsets execution drag.

## 2. Flattening Modality Decision Tree

Choose based on leg liquidity and collateral stack.

- **Accelerated flatten:** Reduce both legs toward target exit. Start with the leg that has higher fill probability and lower slippage.
- **Hedge ratio shift:** Temporarily accept delta exposure on one side to reduce notional on the bleeding leg. Re-hedge after volatility cooldown.
- **Proxy close:** If one leg is illiquid, use a correlated proxy (different venue basis, ETF approximation, next-tenor perp) to reduce exposure, then flatten primary leg in tranches.

## 3. Exit Sequencing Rules

### 3.1 Priority heuristics

Close the **losing leg first** if:
- It is more liquid than the winning leg,
- Its P&L has already locked most of the drawdown,
- Closing it releases margin/collateral for the held leg.

Close the **winning leg first** if:
- You need collateral to avoid liquidation on the loser,
- Funding spread is rate-limiting exit on the winner (same-direction funding accrual makes closure expensive),
- You want to preserve the basis spread for later re-entry.

### 3.2 Margin and collateral accounting

```python
def required_collateral_after_partial_close(trade, leg_to_close_reduction):
    return max(0,
        trade.margin_requirement - leg_to_close_reduction * trade.liquidation_buffer
    )
```

Keep a collateral buffer equal to at least the liquidation threshold of the held leg plus a 10% safety margin.

## 4. Carry Cost Containment

```python
def carry_cost(delta_hold_days, funding_per_day, borrow_per_day, collateral_yield):
    return delta_hold_days * (funding_per_day + borrow_per_day - collateral_yield)
```

Target: `carry_cost < 0.5 * negative_leg_pnl`.

If the carry during clawback exceeds this bound, cut notional further even if transaction costs rise.

## 5. Reactivation Condition

Do not re-enter immediately after flattening. Conditions:

1. `basis > entry_basis * 1.15` (reentry buffer) OR
2. funding spread > 1.5x long-run average AND cross-venue spread confirms signal.

Place reactivation orders as limit ladders, not market orders.

## 6. Macro Cross-Link

Funding rates correlate with macro liquidity conditions:
- Fed TS repo rates, stablecoin issuance growth, and real rates shift trader appetite for leverage.
- Rising real rates compress risk assets and frequently turn funding negative, raising clawback probability.

Use macro liquidity index as an early warning overlay.

## 7. Risk Controls

- Hard stop: if clawback depth exceeds 100% of basis gain buffer, full unwind immediately.
- Funding P&L attribution 5% purity test: separate borrow cost, execution loss, and strategy drift.
- Venue lag tracking: some venues lag funding by 30–90 minutes; avoid redundant entries based on stale leading venue data.
- Currency consistency: keep collateral in the same currency as borrow to avoid FX conversion friction in fast clawbacks.

## 8. When to Apply

Use this skill when:
- You are managing a basis or carry trade that has turned negative,
- You need to choose which leg to close first under stress,
- You want rules for when to stop the strategy temporarily vs permanently,
- You are designing systems that should auto-flatten on clawback criteria.

Do NOT use this as a defensive overlay for directional positions that are not hedgeable in a basis structure.

## 9. Verification

- Record trigger timestamp, signal value, basis_blown, and modality chosen.
- After flatten, confirm both legs closed and no orphan exposure remains.
- Reentry: confirm basis spread passed threshold with at least two independent data sources before re-entering.
