---
title: Cross-Asset Macro Liquidity Signals & Regime Detection
name: cross-asset-macro-liquidity-signals
description: >
  Framework for cross-asset market regime detection using Gaussian HMM (Kroniq Regime Radar).
  Covers 9 features across 5 asset classes, 5-state regime classification,
  early-warning signals, and regime-aware risk management.
triggers:
  - cross asset regime detection
  - hmm market regimes
  - kroniq regime radar
  - regime aware risk management
  - credit spread leading indicator
  - macro liquidity signals
---

# Cross-Asset Macro Liquidity Signals & Regime Detection (Kroniq Regime Radar)

## Core Thesis

Standard quantitative risk models assume financial returns follow a normal distribution with constant volatility. This assumption fails during regime shifts, producing **11.58 percentage point underestimation of annual tail risk** for S&P 500 returns spanning 2020 COVID crisis and 2022 Fed rate shock (Jan 2020 – Dec 2024).

---

## Feature Set (9 Features × 5 Asset Classes)

| Asset Class | Ticker/Source | Features |
|-------------|---------------|----------|
| **Equities** | SPY | Returns, Volatility |
| **Volatility** | VIX | Level, Term Structure |
| **Rates** | TLT (20+ yr Treasuries) | Returns, Duration-adjusted |
| **Gold** | GLD | Returns, Inflation hedge proxy |
| **Credit** | ICE BofA US High Yield (FRED: BAMLH0A0HYM2) | Spread level, Spread change |

---

## Model Architecture

- **Algorithm:** Gaussian Hidden Markov Model (HMM)
- **Search Space:** K = 3 through K = 9 states
- **Validation:** BIC (Bayesian Information Criterion) sweep
- **Robustness:** 5 independent random seeds per K
- **Stability Filter:** Minimum state-size validation (rejects micro-states)

**Optimal Configuration: K = 5 states** — only configuration passing all stability criteria.  
Models at K=6,7,8 produce unstable micro-states (as few as 9 days), inconsistent with reliable live regime routing.

---

## The Five Regimes

| Regime | Label | Persistence | Characteristics |
|--------|-------|-------------|-----------------|
| State 1 | **Low-Vol** | 95.5% | Calm, low volatility, stable correlations |
| State 2 | **Bull** | 92.7% | Rising equities, compressed credit spreads |
| State 3 | **Neutral** | 92.5% | Transitional, mixed signals |
| State 4 | **Macro** | 81.7% | Rate-driven stress, widening credit spreads, VIX elevated |
| State 5 | **Crisis** | 73.0% | Panic selling, VIX > 48, severe drawdowns, flight to quality |

**Critical Structural Property:** No direct transitions from calm states to crisis — crisis entry requires passage through Macro stress state.

---

## Early Warning: COVID-2020 Case Study

| Signal | Date | Lead Time |
|--------|------|-----------|
| Stage 1: Macro Stress | Oct 1, 2019 | **141 days** before SPY peak (Feb 19, 2020) |
| Stage 2: Crisis Classification | Feb 28, 2020 | Before **79% of total drawdown** |

**Key Insight:** Credit spread features provide marginal early-warning signal — equity/volatility features alone only gave 23 days lead time.

---

## Out-of-Sample Performance (2021–2024)

### Walk-Forward OOS (Quarterly Retraining) — Production Simulation

| Metric | Kroniq (K=5) | Buy-and-Hold SPY |
|--------|--------------|------------------|
| Sharpe Ratio | **0.881** | 0.859 |
| Max Drawdown | **-17.46%** | ~-25% |
| CAGR | **9.97%** | ~9-10% |

All walk-forward metrics exceed buy-and-hold Sharpe (0.859).

---

## Production Implementation Notes

1. **API Design:** Framework designed as institutional API for dynamic risk exposure adaptation
2. **Retraining Cadence:** Quarterly walk-forward retraining balances stability vs. adaptivity
3. **Latency:** Sub-second regime classification suitable for daily rebalancing
4. **Feature Pipeline:** Requires reliable daily close data for 5 asset classes + FRED HY spreads
5. **Risk Integration:** Regime posterior probabilities → position sizing / risk budget allocation

---

## Actionable Takeaways for Practitioners

- **Credit spreads are the leading indicator** — include HY spread level & changes in regime models
- **5 states is the stability sweet spot** — more states create micro-regimes unusable for allocation
- **No direct calm→crisis transitions** — monitor Macro state as gatekeeper signal
- **Walk-forward > static training** — quarterly retraining maintains edge in live markets
- **Regime probabilities ≠ binary classifier** — use posterior probabilities for continuous risk budget scaling

---

## Related Skills

- `finance-strategies/market-microstructure-lob-forecasting`
- `finance-strategies/orderbook-resilience-discrete-events`
- `finance-strategies/funding-rate-arbitrage`