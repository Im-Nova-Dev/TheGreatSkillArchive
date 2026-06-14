---
title: Volatility Smile / Surface Modeling with SVI
name: volatility-surface-smile
description: >
  Teach volatility smile/surface modeling with SVI (and SSVI extension): calibration,
  arbitrage constraints, term structure, surface construction, and applications
  to options trading, variance swaps, and crypto/DeFi volatility products.
  Covers actionable interpolation, skew decomposition, and Greeks extraction.
triggers:
  - volatility smile
  - surface interpolation
  - SVI
  - SSVI
  - implied volatility surface
  - variance swap replication
  - skew term structure
  - options Greeks
---

# Volatility Smile / Surface Modeling: SVI & Extensions

Use this skill when designing or teaching volatility surfaces, provisioning structured
products, pricing non-listed strikes, managing quant vol books, or arbitrage-checking
options market microstructure.

## 1. Why Smile/Surface Modeling Matters
The Black–Scholes constant-volatility assumption is violated in practice:
- Market-implied volatility varies with strike and maturity.
- The skew/surface contains consensus views on tail risk, dealer hedging flows,
  and event premia.
- Trading strategies extract value from inconsistencies between fitted surface
  and realized outcomes.

## 2. SVI: Parametric Implied Variance

### 2.1 Formula
Total implied variance w(k) as a function of log-moneyness k:
```
w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))
```
Parameters:
- a: baseline variance at-the-money
- b: slope/steepness of smile
- rho: rotation/skew correlation parameter (-1 to 1)
- m: smile center/at-the-money shift
- sigma: curvature/spread of smile wings

Implied volatility:
```
implied_vol(k) = sqrt(w(k))
```

### 2.2 Arbitrage Constraints (Gatheral)
To avoid butterfly arbitrage (negative density):
- `|rho| < 1`
- `b * rho + sigma > 0`
- `w(k) >= 0` for all k
- Second derivative `w''(k) >= 0` everywhere

Verify numerically: sample dense grid in k and compute density via Breeden-Litzenberger
or Corran-Sheriff. Fail if negative density detected.

## 3. Calibration Workflow
1. **Input Data**: end-of-day or intraday option chain for target symbol/maturity
   with mid prices, bid/ask, volumes, and open interest.
2. **Clean Quotes**: remove quotes with zero bid, abnormally wide spreads, or
   stale timestamps. Prefer liquid strikes around ATM.
3. **Invert IV**: for each strike, solve Black–Scholes implied vol from mid price.
4. **Fit SVI**: minimize sum of squared errors between market IV and SVI IV:
   ```
   loss = sum_over_i (iv_market(i) - iv_svi(k_i))^2 * weight_i
   ```
   Use higher weight near ATM to stabilize fit.
5. **Enforce Constraints**: clamp parameters after each iteration or add penalty
   terms for constraint violations.
6. **Maturity Interpolation**: fit parameters separately for each expiry, then
   fit smooth curves for a, b, rho, m, sigma as a function of time to expiry
   (linear, quadratic, or spline basis).

## 4. Term Structure and Surface Construction
### 4.1 Parameter Surface
For smoothness, represent each SVI parameter as a function of maturity:
```
a(T) = a0 + a1*T
b(T) = b0 + b1*T + b2*T^2
rho(T) = rho0 + rho1*T
...
```
Then surface IV at strike, maturity is `sigma_iv(k, T) = sqrt(w(k; params(T)))`.

### 4.2 Event Drift
During earnings, macro events, or exchange upgrades, allow separate parameter
sets before/after event. Blend with a forward-dated event smile to avoid
discontinuities.

## 5. Greeks Extraction from SVI
- **Delta**: differentiate SVI with respect to spot under the surface.
- **Gamma**: second derivative of surface wrt spot.
- **Vega**: sensitivity of surface to shift in a, b, rho, sigma.
- **Vanna**: cross-derivative of vol wrt spot and vol; useful for
  cross-gamma hedging.
- Implementation: compute numerically from surface or via analytic SVI
  derivative formulas.

## 6. Applications

### 6.1 Variance Swap Replication
- Replicate forward-starting variance by integrating SVI across strikes:
  ```
  E[variance] ~ integrate(w(k) dk) over strike range
  ```
- Calibrate replication weights for each strike to match realized variance.

### 6.2 Non-Listed Strike Pricing
- Use fitted SVI to interpolate IV for mid-strikes or exotic payoff boundaries.

### 6.3 Crypto / DeFi Applications
- Fit SVI to perpetual options or dated options from Deribit, OKX, Bybit.
- Compare SVI-implied variance to on-chain realized variance (e.g., Deribit RV)
  to identify overpriced variance for premium-selling strategies.
- When analyzing non-std expiries (e.g., Friday expirations), enforce
  term-structure continuity to avoid spikes.

### 6.4 Structured Products
- For vol-targeting or variance-selling products, pre-fit SVI and set contract
  terms (strikes, barriers) such that the product's expected payoffs align with
  fitted surface minus execution cost.
- Use skew term structure to estimate barrier вероятность.

## 7. SSVI Extensions
Surface SVI (SSVI) introduces time-dependent correlation:
```
w(k, T) = (a(T) + b(T) * (rho(T) * (k - m(T)) + sqrt((k - m(T))^2 + sigma(T)^2))) * g(T)
```
where `g(T)` ensures correct total variance scaling. Use when front/back
skew shapes differ sharply (e.g., event-heavy assets, crypto near upgrades).

## 8. Risk Controls
- Regime filters: do not fit extreme tails separately; cap weight for OTM/ITM
  strikes with sparse liquidity.
- Model risk: stress test by perturbing rho, sigma, and b by ±1 standard deviation
  and reprice portfolio.
- Execution: keep fitted surface ahead of market by at most 1 tick in IV space.

## 9. Practical Tips
- Use Python (scipy.optimize) or MATLAB for calibration. Libraries: `pyfolio`,
  `volsurface`, `svi` community packages.
- For high-frequency teaching: calibrate to 15-minute bars for liquidity
  demonstration.
- Keep a rolling 30-day calibration log to detect drift in parameters and
  liquidity-quality degradation.

## 10. Exercises
1. Calibrate SVI to 1 week of BTC options data. Plot fitted vs market IV and
   verify butterfly arbitrage constraints.
2. Compute variance swap replication weights from SVI and compare to market figures.
3. Introduce an event (e.g., ETF announcement) and compare pre-event vs post-event
   parameter shifts, especially b, rho, sigma.
4. Evaluate profitability of selling OTM variance when SVI-implied variance exceeds
   a rolling 30-day realized variance forecast by at least 5 vol points.

## 11. Related Skills / Concepts
- `finance-strategies/variance-risk-premium-execution-workshop`
- `finance-strategies/risk-reversal-volatility-skew`
- `finance-strategies/orderbook-microstructure-trading`
