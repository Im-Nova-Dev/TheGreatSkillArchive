---
name: finance-variance-and-volatility-pricing
description: Teach variance risk premium (VRP), realized variance, variance swaps, volatility carry, and volatility regime forecasting. Use for options-selling strategies, risk budgeting, and macro-vol overlay design.
metadata:
  author: hermes scheduled
  version: 1.0
---

# Finance: Variance, Volatility Pricing & VRP Utilization

## Why This Matters
Volatility is an asset class. VRP quantifies the wedge between risk-neutral and historical volatility and creates systematic carry opportunities while providing forward-looking tail-risk information.

## Core Concepts

### 1. Realized Variance (RV)
Square and sum high-frequency log returns over a window.

```python
def realized_variance(returns: pd.Series, annualize: bool = True) -> float:
    rv = (returns ** 2).sum()
    if annualize:
        rv *= (252 * 60 * 24) / len(returns)
    return rv
```

### 2. HAR-RV Forecast
Heterogeneous Autoregressive model decomposes RV into daily, weekly, monthly components.

```python
def har_rv(rv_daily: pd.Series, rv_weekly: pd.Series, rv_monthly: pd.Series) -> float:
    return 0.4 * rv_daily + 0.3 * rv_weekly + 0.3 * rv_monthly
```

### 3. Variance Risk Premium (VRP)
Compensates option sellers for jump/dispersion risk.

```python
def variance_risk_premium(atm_iv: float, rv_forecast: float) -> float:
    iv = atm_iv / 100.0
    return (iv ** 2) - rv_forecast
```

- Z-score VRP over 60 days to normalize.
- High VRP -> usually favorable to sell variance.
- Low VRP -> beware optionality expansion; reduce short vol exposure.

### 4. Volatility Carry & Term Structure
- If forward variance > spot variance and VRP high, harvest carry via variance swaps or short VIX futures.
- Term-structure inversion = demand for near-dated protection; favor strangles over directional shorts.

### 5. Volatility Regime Filters
- Use realized variance z-score + skew index change + funding rate vol as inputs.
- Regimes: benign, jump, tail. Position size accordingly, default to 30% notional in tail regime.
- Cross-asset macro overlay: flattening yield curve + rising VRP often precedes downside skew expansion.

## Actionable Strategies

### Strategy A: VRP Variance Carry
1. Forecast RV with HAR-RV using 1-year history.
2. Compute VRP z-score over 60 days.
3. Enter when z-score > 1.5 and term structure is in contango.
4. Size risk Vol equivalent to 1.5 sigma of RV; stop if RV forecast > implied variance.

### Strategy B: Skew-Directed Strangle
1. Long 15-delta put, short 30-delta put; short symmetrical 15/25-delta calls.
2. Only execute when VRP z-score > 1.2 and skew positive.
3. Roll monthly or when realized skew steepens more than 0.5 vol pts.

### Strategy C: VRP Macro Overlay
- Use VRP percentile as downside-kurtosis indicator.
- Reduce trend/CTA exposure when VRP percentile > 80 and curve flattening > 20 bps.

## Verification Criteria

- Carry strategy: annualized Sharpe ≥ 1.0 over 4 years.
- Strangle: win rate ≥ 55%, profit factor ≥ 1.6, max drawdown ≤ 12%.
- Accuracy of RV forecast vs realized 7-day squared returns: RMSE ≤ 0.0005 squared daily units.

## Data Sources
- Equity index options: CBOE, OPRA, tradier, Interactive Brokers.
- Volatility data: vixcentral, CBOE term structure, Bloomberg volatility indices.
- Macro/policy data: FRED yield curve, Fed funds, CPI announcements for regime filters.

## Practical Implementation Checklist
- [ ] Pipeline: fetch options chain, compute ATM IV term structure, quote synthetic variance swap.
- [ ] Backtest fill assumptions: 10 bps per leg, 5 bps roll cost.
- [ ] Run monthly coverage scan with options liquidity cutoff and delta recalibration.
- [ ] Document roll dates and holding period to support carry attribution.
