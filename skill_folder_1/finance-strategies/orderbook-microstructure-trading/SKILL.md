---
name: orderbook-microstructure-trading
description: |
  Build short-horizon trading signals from orderbook microstructure: OFI,
  queue position, VPIN/toxicity, fill-rate dynamics, and funding-rate leads.
  Use when selecting Venue, estimating slippage, designing execution algo,
  or teaching microstructure-driven execution.
---

# Orderbook Microstructure Trading

## When to Use
- Build intraday or sub-minute signals on liquid spot and perp markets.
- Diagnose fill-rate decay at the top of book.
- Compare execution quality across venues.
- Improve base execution before embedding into long-horizon strategies.

## 1. Order Flow Imbalance (OFI)
Net signed pressure from changes at the best bid and best ask:
```
OFI = ε_bid * ΔV_bid - ε_ask * ΔV_ask
```
- ε = +1 if volume increased, -1 if decreased, 0 if unchanged.
- Compute 1-second rolling OFI versus its 60-second moving average.
- Cross above +2σ ⇒ short-term bullish 5-30 seconds; flip for negative.

## 2. Effective Spread vs Quoted Spread
- Quoted spread is a poor proxy for execution cost.
- Effective spread measures economic distance based on mid-price:
  `s_eff = 2 * |P_trade - M_t| / M_t`.
- Use s_eff to calibrate participation rate caps.

## 3. Queue Position
- Reveals how much volume sits ahead of your order.
- Higher queue depth ⇒ higher cancellation risk per unit time.
- Order cancellation rate often follows a Poisson arrival process:
  estimate λ from historical top-level cancellations.
- Expected waiting time:
  `E[T] = (V_queue / σ_flow) * (1 - p_fill)`

## 4. VPIN / Order Flow Toxicity
- Volume-Synchronized Probability of Informed Trading (VPIN).
- Compute in fixed-volume buckets instead of time buckets.
- High VPIN ⇒ adverse selection risk rises ⇒ widen quotes or pause quoting.
- Proxy if VPIN unavailable:
  `TOX = |trade_volume_signed| / lquote_depth_change`

## 5. Funding-Rate Lead
Perpetual futures funding rate leads spot by 1-50 minutes during de-pegs or large basis moves. Trade the convergence:
- Short perp / long spot when funding > +3σ.
- Long perp / short spot when funding < -3σ.
- Exit when funding crosses its 20-period MA.

## 6. Execution Calibration
Participation rate:
```
P_t = min(P_max, α * |signal| * ADV)
```
Where:
- `P_max = 0.10 * ADV` (do not exceed 10% of ADV per minute)
- `α` expands in low-toxicity regimes, contracts when VPIN spikes.

## 7. Decorator Checklist
Before trading:
1. Verify adequate L2 depth; OFI is noise when bid+ask < 0.5 BTC/ETH equivalent.
2. Complement OFI with VPIN; OFI alone misleads during spoofing.
3. Use funding lead as an independent leg; do not double-count.
4. Time-of-day filter: avoid first 5 minutes after session changes.
5. Reserve capacity for slippage if VPIN > 0.99 percentile.

## Pitfalls
- OFI prediction window is short; transaction costs erode edge beyond 1 minute.
- Venue latency arbitrage dominates; colocate or use neutral gateway.
- Low-liquidity markets produce noisy OFI; require volume filter >= baseline.
- Funding-rate arbitrage has funding-tailloss risk if spot lending rates diverge.

## Further Reading
- Cont, R. (2011) *Volatility clustering in financial markets*.
- Cartea, A., et al. (2015) *Algorithmic and High-Frequency Trading*.
