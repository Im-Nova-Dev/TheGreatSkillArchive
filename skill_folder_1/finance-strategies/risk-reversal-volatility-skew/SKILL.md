---
title: Risk Reversal and Volatility Skew
name: risk-reversal-volatility-skew
type: quantitative-signal
description: >
  Use when designing sentiment signals from options skew, building volatility
  overlays, or deriving execution rules from OTM put/call implied-vol differentials.
  Covers 25-delta risk-reversal construction, skew interpretation, term-structure
  interactions, event-driven regime shifts, and rules-based trading construction.
  Centered on actionable implementation, not commentary.
version: 1.0.0
---

# Risk Reversal and Volatility Skew Signal Design

## Problem Statement
Mark price alone ignores tail-risk sentiment embedded in options. Risk reversal and
volatility skew capture the market’s directional hedging demand across strikes and
maturities and can be converted into executable signals or regime filters.

## Core Definitions

### Risk Reversal (Volatility Basis)
> Risk Reversal = IV(OTM Put) − IV(OTM Call)

- **Positive value** = put bias (market pays premium for downside protection)
- **Negative value** = call bias (market pays premium for upside exposure)
- Convention matters: some sources invert the formula. Always confirm sign convention
  before using as a trading signal.

### Standard Strike Selection
Use 25-delta options:
- Avoids ME liquidity
- Captures large moves
- Provides stable sentiment signal

## Signal Construction

| Threshold | Signal | Interpretation |
|---|---|---|
| `risk_reversal > +3.0%` | Bearish sentiment / downside hedging dominant | Portfolio managers hedging post-rally |
| `risk_reversal < -3.0%` | Bullish sentiment / call demand dominant | Short-covering or catalyst anticipation |
| `|risk_reversal| < 0.5%` | Neutral / compressed skew | Low conviction regime |

### Normalization and Filters
- Normalize by ATM IV to remove level effect: `rr_norm = rr / atm_iv`
- Use rolling 20-bar z-score against 60-day history to filter noise
- Combine with put/call volume ratio to confirm flow-driven vs. positioning-driven skew

## Skew vs. Term Structure Interactions

### Regime Interpreter Matrix
| Front-month IV | Risk Reversal | Regime Signal |
|---|---|---|
| Low / declining | Highly positive | Near-term calm, but downside hedges pricing future decline (uncertain timing) |
| High | Highly negative | Near-term event expected, options market pricing upside catalyst |
| Backwardated front < back | Negative | Bullish catalyst imminent |
| Backwardated front < back | Highly positive | Panic hedge — downside fear compressed near term |

## Event-Driven Skew Moves
- Fed meetings, earnings releases, CPI, FOMC minutes
- Pre-event: positive risk reversal widens as hedgers buy OTM puts
- Post-event negative surprise: risk reversal flips negative as calls bid up
- Track 24-hour window around event for regime shift confirmation

## Trading Rules and Construction

### Rules-Based Skew Signal
1. Compute `rr_norm` on rolling 60-bar window at daily close
2. Calculate z-score: `z = (rr_norm − mean_60) / std_60`
3. Entry:
   - `z > +2.0` → risk reversal overlay: buy OTM puts as direct hedge or short underlying
   - `z < -2.0` → risk reversal overlay: buy OTM calls as upside exposure adder
4. Hold until `|z| < 0.5` or 5-day trailing stop breaches entry basis
5. Size by normalized ATM IV: `size_base * (1 + atm_iv / 0.20)` to scale with vol regime

### Volatility Skew Mean-Reversion
- Extreme positive skew → sell OTM put spread (collect premium), expect normalization
- Extreme negative skew → buy OTM call spread (cheap upside), expect normalization

### Portfolio Overlay Rules
- Use `rr_norm` as regime filter:
  - `rr_norm > +1.0 std` → reduce gross exposure by 20%
  - `rr_norm < -1.0 std` → increase gross exposure by 10%
  - Track P&L attribution separately from directional alpha

## Crypto and DeFi Adaptations
- Deribit BTC/ETH options: 25-delta skew available daily; track funding rate regime alongside
- DEX options (dYdX, AEVO, OPYN): wider spreads, filter by OI and liquidity
- On-chain signal: compare skew to perpetual funding rate; negative skew + negative funding = strong bullish echo
- Skew divergence from on-chain futures basis = potential arbitrage signal (statistical, low frequency)

## Execution Checklist
1. Source IV data: CBOE, ORATS, Deribit API, or broker platform with multi-strike IV
2. Build rolling 60-bar lookback for mean and std
3. Compute daily risk reversal at close for stable comparison
4. Apply z-score filter + ATM IV normalization
5. Backtest regime shift rules on rolling 1-year windows with rolling 3-month performance
6. Add funding-rate overlay for crypto assets

## Verification Steps
- Compute IC (information coefficient) of `rr_norm` 5-day forward returns
- Confirm sign consistency across asset classes
- Validate that extreme z-score moves precede realized vol changes

## Related Skills
- `finance-strategies/finance-options-and-greeks`
- `finance-strategies/variance-risk-premium-execution-workshop`
- `finance-strategies/funding-rate-arbitrage`
- `finance-strategies/cross-asset-macro-liquidity-signals`
