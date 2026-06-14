---
name: finance-options-and-greeks
description: "Teach options and derivatives microstructure: dealer gamma exposure regime filtering, options liquidity clusters, implied volatility arbitrage, yield curve trades, structured product mechanics, and how greeks map to portfolio risk and execution behavior."
metadata:
  author: hermes scheduled
  version: 0.1
---

# Finance: Options, Derivatives & Greeks

## Why This Matters
Derivatives are not separate from spot microstructure; dealer hedging flow shapes intraday liquidity, volatility regimes, and gap risk. Greeks are the control-plane mapping between options inventory and realized market behavior.

## Core Concepts

### 1. Dealer Gamma Exposure (GEX)
- **Inputs**: aggregate open-interest-weighted gamma from listed options converted into share equivalents per underlying.
- **Construction**: `share_gamma = OI * gamma * underlying_price * 100`, summed across strikes and tenors with a market-maker inventory skew adjustment.
- **Regimes**:
  - Negative GEX → dealers short gamma: must sell into strength, buy into weakness → moves amplify.
  - Positive GEX → dealers long gamma: sell into strength, buy into weakness → moves dampen and revert.
- **Actionable**: use Z-score of rolling 5-day GEX as an intraday regime filter for participation rate, breakout vs fade selection, and stop width.

### 2. Options Liquidity Clusters
- Liquidity concentrates near high open-interest strikes and major round numbers.
- Cross underlying and futures liquid: option-derived liquidity walls affect spot and futures via hedging, not just options MM inventory.

### 3. Implied Volatility Arbitrage
- Use forward IV vs historical IV gap filtered by GEX regime:
  - Negative GEX: IV tends to gap higher during strength; short-vega premium can be overpriced in crisis spikes.
  - Positive GEX: IV compresses in low-vol range; calendar and ratio spreads harvest term-structure richness.

### 4. Portfolio Greeks Mapping
- Translate options/book greeks into spot behavior:
  - Long gamma = buy dips, sell rips.
  - Short gamma = sell rips, buy dips for hedgers → breakout-friendly.
  - Negative vega = underperform when IV spikes; reduce vega exposure before known event windows.

## Actionable Strategies

1. **GEX-Regime Participation Scaling**
   - ESG/EMA scaled notional inversely proportional to |GEX Z| in ES, NQ.
   - Negative GEX + 0DTE → reduce notional, widen stops, avoid short straddles.

2. **Gamma-Cluster Execution Routing**
   - When crossing high absolute gamma strikes, split orders using iceberg limit placement; C-level liquidity is denser and reduces adverse selection.

3. **Vega Collection in Positive-GEX Ranges**
   - Favor short-vega premium selling in positive-GEX regimes with VIX term structure flat or in contango.

4. **Hedge-Flow Fade**
   - Large put-buy-to-open spikes with rising VIX often represent dealer/hedge-fund tail hedging rather than directional conviction; fade extreme left-tail IV spikes when GEX is positive.

## Risk Controls
- Refresh GEX once daily after standard options expiration to prevent stale OI regimes.
- Override regime with 0DTE expiration days; treat negative GEX + 0DTE as maximum hazard.
- Suppress short-option entries when put/call open interest ratio is above 3.0 at the nearest 10 strikes.

## Verification Criteria
- ES 5-min regime-following trades gated by GEX Z:
  - Negative-GEX breakout-following: hit rate ≥ 52%, profit factor ≥ 1.45, 3-month drawdown ≤ 6%.
  - Positive-GEX mean-reversion: hit rate ≥ 58%, profit factor ≥ 1.7, 3-month drawdown ≤ 8%.
- VIX premium-selling strategy only in positive-GEX regimes.

## References
- Hull, *Options, Futures, and Other Derivatives*.
- Volatility Markets Institute weekly GEX releases.
- CBOE Marginal Volume Surface methodology.
