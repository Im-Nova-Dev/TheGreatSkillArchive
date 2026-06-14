# Orderbook Slippage Estimation

**Skill Category:** finance-strategies  
**Sources:** Wu (2025) arXiv:2511.20606; Brenndoerfer (2026); OFR (2019); Bookmap (2025); Sei Blog (2025).  
**See also:** `/home/nova/.hermes/intel/finance/slippage-killzones-2026-06-05.md`

---

## Purpose

Teach market microstructure concepts and build usable slippage-estimation primitives for:
- Cash equities
- Futures / CTA algos
- Crypto DEX / CEX
- Derivatives / option execution

---

## Core Definition

Slippage = (execution price − arrival midprice) × signed volume

Breakdown:
- **Explicit cost:** spread crossing (immediacy cost)  
- **Transient impact:** temporary price movement from your own order  
- **Permanent impact:** information leakage moves the "fair" price  

```python
def slippage_bps(fill_px: float, arrival_mid: float, qty: int, side: str) -> float:
    """Return slippage in basis points. Positive = unfavorable."""
    signed = 1 if side == "buy" else -1
    return signed * (fill_px - arrival_mid) / arrival_mid * 10_000
```

---

## 1. Intraday Liquidity Killzones

Trade volume and liquidity are **not uniform**. Regime-filter execution:

| Window (ET) | Status | Spread / Slippage Multiplier vs. baseline |
|---|---|---|
| 09:30–10:30 | LIQUID_WINDOW | 0.7× |
| 10:30–11:30 | OPTIMAL | 0.6× |
| 11:30–13:00 | KILLZONE | 2.0–2.5× |
| 15:30–16:00 | RISKY | 1.8× |
| 16:00–20:00 | KILLZONE | 2.5–3.0× |

Implementation: multiply your target max slip (e.g., 10 bp) by the window multiplier before running the algo.

---

## 2. Sizing Against Orderbook Depth

Basic depth check before sending large market order:

```python
def max_ahead_slip(best_bid: float, best_ask: float, depth: list, trade_qty: int, side: str) -> float:
    """Estimate worst-case slippage walking the book."""
    remaining = trade_qty
    filled_px = 0.0
    levels = sorted(depth, key=lambda x: x[0], reverse=(side=="sell"))
    for px, size in levels:
        take = min(remaining, size)
        filled_px += take * px
        remaining -= take
        if remaining <= 0:
            break
    avg_fill = filled_px / trade_qty
    arrival = best_ask if side == "buy" else best_bid
    return abs(avg_fill - arrival) / arrival * 10_000
```

Rule of thumb: if depth-1% * bid/ask size < 3× your order, you will likely walk 2+ price levels.

---

## 3. Spread-Quality Killzone Alert

```python
import pandas as pd

def is_spread_killzone(spread: float, spread_ma20: float, threshold: float = 2.0) -> bool:
    """Returns True when current spread exceeds threshold × 20-day MA."""
    return spread > threshold * spread_ma20
```

Use: when True, halt aggressive execution; enable opportunistic limit-only mode.

---

## 4. Cross-Asset Liquidity Contagion (OFR 2019 Bridge)

Illiquidity propagates: when equities show elevated spread or trade-at abnormal volume, derivatives, ETFs, and correlated cash markets experience spillover within 3–20 minutes.

**Practical rule:**
- If S&P 500 ETF spread > 2× 20-day average **or** cumulative volume at 11:00 ET > 35% of ADV,  
  do not initiate new derivatives overlays on same index until spreads normalize.

---

## 5. Crypto / DEX Extension: Market-to-Book Ratio + MEV Budget

In AMM markets with concentrated liquidity:

```python
def dex_slippage_budget(tick_liq: float, trade_size: float, ewma_ratio: float, mev_active: bool) -> float:
    """Estimate acceptable slippage budget in bps."""
    ratio = trade_size / tick_liq
    base = 1.0 + (ratio / ewma_ratio) * 0.5
    return base * (1.5 if mev_active else 1.0)
```

Wu (2025) threshold: only execute when market-to-book ratio crosses time-decaying liquidity threshold. Implementation: decay threshold by half every 30 seconds of queue inactivity.

---

## 6. Skill Usage

Apply this skill to:
- Execution algorithm design (TWAP/VWAP adaption)  
- Pre-trade risk checks (depth + killzone + contagion)  
- Strategy backtest filtering (exclude killzone fills)  
- Crypto trade sizing with MEV buffer  

---

## Verification Checklist

- [ ] Compute 20-day rolling average 15-minute spreads; confirm killzone enrichment.  
- [ ] Backtest a momentum strategy with killzone filter and compare Sharpe vs. unfiltered.  
- [ ] Confirm that `max_ahead_slip` exceeds realized slip by no more than 30% on average over 1,000 random SPY trades.
