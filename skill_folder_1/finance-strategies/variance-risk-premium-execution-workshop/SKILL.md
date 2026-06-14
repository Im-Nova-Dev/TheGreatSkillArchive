---
name: variance-risk-premium-execution-workshop
description: Teach how to design and operate a variance risk premium strategy: measurement, tradeable structures, risk controls, and outcome verification.
---

# Variance Risk Premium Execution Workshop

Use this skill to teach or implement a tradeable variance risk premium workflow. Focus on execution, not commentary.

## 1. Intuition
Implied variance prices an insurance-like volatility contract. Realized variance is what actually happens. The persistent gap between them is tradeable when measured and executed correctly.

## 2. Build measurement
1. Choose one proxy for implied variance: index VIX, 3-month VIX3M, ATM option implied variance.
2. Compute realized variance from high-frequency returns:
   - log returns
   - annualize by multiplying by sqrt(seconds-in-year / observation-interval).
3. Build VRP_t = IV_t - RV_{t-1..t}
4. Plot rolling 3-year z-score of mean and term-structure steepness for entry filters.

## 3. Tradeable structures
- Variance swaps/futures
- Dispersion: index variance - single-name variance basket
- Calendar variance spread: near vs next expiry

## 4. Entry rules
Long VRP: IV z-score > 1.0 and VRP z-score > 1.2.
Short VRP: RV z-score > 1.1 and VRP z-score < -0.8.
Exit on VRP z-score reverting to 0.

## 5. Risk controls
- Cap vega and gamma by portfolio limits before entry.
- Prefer variance contracts; if unavailable, hedge delta and rebalance no slower than intraday 3× per day.
- Avoid back-week expiries.

## 6. Verification
- Required: walk-forward 12-month out-of-sample Sharpe >= 1.0.
- Required: 99th percentile daily loss no worse than 3% of strategy notional.
- Required: t-stat of mean excess return > 2.5 after transaction costs.

## 7. Pitfalls
- Treating VIX as volatility without considering its beta to SPX.
- Forgetting that RV depends on sampling frequency and microstructure noise.
- Ignoring jumps: RV overestimates continuous variance; adjust if needed.
- Funding and margin costs on leveraged proxies can wipe premium.
