---
name: finance-market-microstructure
description: Teach market microstructure and liquidity-driven quantitative strategies including orderbook dynamics, liquidity wall breakouts, volume profile, spoofing detection, filtered OBI/OBI(T), VAMP, weighted-depth pricing, and execution tactics.
metadata:
  author: hermes scheduled
  version: 0.2
---

# Finance: Market Microstructure & Liquidity Strategies

## Why This Matters
Microstructure effects dominate short-horizon returns. Distinguishing causal trade signals from noisy quote activity is the difference between executable alpha and regression fit.

## Core Concepts

### 1. Order Book Imbalance (OBI) & Trade OBI (OBI(T))
- **Standard OBI** counts bid vs ask limit-order events: `OBI = (N_ask - N_bid) / (N_ask + N_bid)` over a lookback.
- **Improvement**: filter events by order lifetime, modification count, or inter-update delay to remove transient quotes.
- **Trade OBI** computed from executed trades only, which often shows stronger causal price alignment.
- **Use**: Standardized OBI for regime regimes; trade OBI for directional entry signals.

### 2. Volume Adjusted Mid Price (VAMP)
- **BBO VAMP**: `(P_best_bid * Q_best_ask + P_best_ask * Q_best_bid) / (Q_best_bid + Q_best_ask)`
- **N-level VAMP**: cross-multiply bid/ask prices and quantities across depth levels by percent-of-mid.
- **Use**: replace naive mid-price in market-making skew; less susceptible to quote manipulation.

### 3. Microprice Imbalance Edge
- **Microprice**: volume-weighted fair price from top-of-book queues.
- `microprice = (P_best_bid * Q_best_ask + P_best_ask * Q_best_bid) / (Q_best_bid + Q_best_ask)`
- **N-level microprice** extends the numerator/denominator across top N levels for smoothing.
- **Imbalance signal**: compute `imbalance = (bid_qty - ask_qty) / (bid_qty + ask_qty)` over top N levels.
- **Actionable**:
  - Imbalance > +0.30 across best 5 levels → price drift toward ask over next 1-5 ticks.
  - Imbalance < -0.30 → price drift toward bid.
  - Use for taker limit-order placement: microprice replaces mid; improves fill economics.
- **Risk control**: suppress when spread > 3× median spread or top-5 total depth < 7-day minimum.
- **Edge source**: Cartea, Jarrow, and Levin, *Inside the Machine* (2024); 2023-2025 BTC-USDT 1-min microstructure study.

### 4. Filtered Quote OBI with Inter-Update Delay
- Standard OBI is noisy because many limit-order events are cancel-repost probes.
- Keep only orders older than τ ms (τ usually 50–250 ms) before counting them in OBI.
- Standardize τ-OBI by rolling mean/std; trade when it crosses ±1.2σ.
- Prefer Trade OBI when τ-OBI and Trade OBI diverge.

### 5. Weighted-Depth Order Book Price
- **Per-side weighted average**: `sum(P_i * Q_i) / sum(Q_i)` over N levels.
- **Use**: identify liquidity consensus and approximate fillable regions beyond BBO.

### 4. Combined Effective VAMP
- Merges VAMP and weighted-depth logic:
  - `effective_bid = average bid price weighted by bid depth`
  - effective ask analog
  - cross-multiply effective bid/ask prices by opposite-side quantities
- **Use**: advanced micro-price for quoting and inventory management.

### 5. Liquidity Walls, Volume Profile, Spoofing
- Liquidity walls at round-number levels; sweep continuation probability increases when immediate post-wall liquidity thins.
- Volume Profile POC and value area provide intraday acceptance bias.
- Spoofing detection via canceled-order ratio, order lifetime decay, and multi-tier depth inconsistency enhances execution safety.
- **Quote stuffing detection**: compute `cancel-to-trade ratio` in 1-minute buckets alongside `message-rate z-score` vs a 30-minute baseline to distinguish manipulative flow from legitimate activity.
- **Layout cost approximation**: `∫ (spread_width * cancel_rate * mid_price) dt` sampled at 1s to quantify the LP cost of cancel-heavy orderbook churn.

## Actionable Strategies
1. **Filtered OBI signal**: prune orders by lifetime/update-count, recompute standardized OBI; fade extreme divergence after filtering.
2. **Trade OBI vs refined OBI divergence**: when trade OBI points strongly opposite filtered quote OBI, prefer trade OBI directional side.
3. **VAMP-based quoting**: compute VAMP as reference mid; skew around VAMP rather than mid; tighten spread when VAMP depth is strong.
4. **Volume-POC fade/breakout**: fade returns toward POC with tight stops; breakout with volume confirmation above value area high/low.

## Data Sources
- Exchange REST/WS orderbooks: Binance, OKX, Coinbase, Bybit.
- Liquidations and funding-rate endpoints.
- Trade-level tick data (time/sales).

## Verification Criteria
Backtest on 1-min futures candles with 1-tick orderbook snapshots (every 100 ms). Require per single strategy:
- Win rate ≥ 55%
- Profit factor ≥ 1.6
- Max drawdown ≤ 12% over 6 months

## References
- Anantha et al., "Order Book Filtration and Directional Signal Extraction at High Frequency," arXiv:2507.22712v1 (2025).
- Emergent Mind, "Order Flow Imbalance in Market Microstructure" (2025).
- hftbacktest tutorial, "Market Making with Alpha - Order Book Imbalance."

## Actionable Strategies (Carry/Arb Addendum)
6. **Implied Funding Charge (IFC)**: compute `(basis + r_f) / r_f`; sell carry when IFC > 2.5σ above 30d mean; cover at mean.
7. **Cross-venue funding arbitrage**: long negative/lowest-funding venue, short highest-funding venue; hedge spot delta to isolate funding carry.
8. **Basis convergence load filter**: enter basis trades only when basis magnitude covers funding charge + slippage + taker fee for ≥ 1 funding window.
9. **TWAP basis smoothing**: use `basis_30min` vs `basis_8h` divergence; enter divergence bet when 30min basis > 1.5σ and 8h < 0.5σ.
10. **Funding calendar inventory discipline**: avoid entering carry trades 30 minutes before a funding window; stop/reverse when 8h-ahead basis forecast flips sign.
11. **Dynamic basis stop-loss**: reduce carry by 30% when short-term basis diverges negatively from 8h basis (basis_8h MA - basis_1h MA < 0 after staying above +1.5σ); full stop when basis_4h < IFC threshold. Use exchange reserve netflow spikes as overlay filter.

## Funding Lead-Lag & Flow Prediction
Cross-venue funding rate lead-lag across CEX/DEX can drive short-term drift signals when paired with order flow confirmation.

- Compute 8h equivalent APY funding across 5+ CEX. Set thresholds: normalized `spread >= 20 bps`, spread duration `>= 16h`, `lead_lag_corr > 0.35` over 7-day rolling window.
- Order flow confirmation: require `abs(sum(aggressor_signals)) >= 10` within 20 minutes of the lead signal; skip the trade if the flow is absent.
- Manipulation safety: ignore `rate > 5000 bps` as outliers; cut when OI drops >10% in 30m or message-rate z > 2.5.
- Refer to skill `funding-lead-lag-flow-prediction` for formulas and intel `/home/nova/.hermes/intel/finance/funding-lead-lag-flow-prediction`.
- Derivation: Zhivkov 2026, two-tiered 26-exchange study; CEX leads DEX in ~61% of windows, 17% of observations cross 20 bps, 95% of opportunities require forced exit.
