# Variance Risk Premium (VRP) Harvesting
**Date Captured**: 2026-06-06
**Category**: Quant Strategy / Derivatives / Portfolio Theory
**Actionability**: High

---

## Concept Summary
The variance risk premium is the systematic spread between implied variance (from options) and realized variance. Selling this premium — via variance swaps, short straddles/strangles, or delta-hedged option selling — is a core quant strategy with positive expected return over long horizons.

### Core Formula
VRP = Implied Variance (IV²) - Realized Variance (RV)

Or in volatility terms:
VRP_vol = Implied Vol - Realized Vol

### Why It Exists
- Insurance demand: Institutions hedge tail risk by buying OTM puts, pushing up implied variance.
- Dealer gamma hedging: Market makers delta-hedge short gamma positions, buying high/selling low, which compresses realized variance.
- Leverage constraints: Regulatory and risk limits prevent full arbitrage.

---

## Actionable Implementation

### 1. Signal Construction
- Compute rolling 30-day realized variance from 5-minute returns (or close-to-close).
- Obtain 30-day ATM implied variance from options chain (or VIX-style index for equities, Deribit DVOL for crypto).
- VRP signal = IV² - RV. Normalize by IV² to get VRP premium ratio.

### 2. Entry Rules
- Go short variance when VRP ratio > threshold (e.g., > 15% or > 1.5σ above rolling mean).
- Preferred instruments:
  - Equity: S&P 500 variance swaps, SPX short straddles (delta-hedged).
  - Crypto: Deribit BTC/ETH variance swaps, or short gamma via ATM straddles with dynamic delta hedging.
  - DeFi: Option vaults selling vol (e.g., Dopex, Lyra, Premia) — filter by VRP spread.

### 3. Sizing and Risk
- Position size = base_notional * (VRP_ratio / median_VRP_ratio) capped at max_allocation.
- Stop loss: Realized variance exceeds implied variance by > 2× for 5 consecutive days (regime shift).
- Gamma risk limit: max short gamma exposure per unit portfolio vol.

### 4. Rolling / Rebalancing
- Roll variance swap positions monthly or quarterly.
- For option-based replication: rebalance daily delta hedges; roll straddles 7-14 days before expiry.

---

## Crypto/DeFi Specifics
- Perpetual funding rate acts as a partial VRP proxy: high funding correlates with elevated IV.
- Realized variance calc must account for 24/7 trading — use 1-hour or 4-hour bars, not daily close.
- DeFi option liquidity is thin; prefer CEX variance swaps (Deribit) or structured products with explicit VRP targets.
- Watch for liquidation cascades: they spike RV temporarily but IV may not keep pace — conflict for VRP harvesters.

---

## Quant Research Extensions
- Conditional VRP: regress VRP on term structure slope, skew, macro regime (VIX term structure, credit spreads).
- Cross-asset VRP: long equity VRP, short crypto VRP when correlation regime diverges.
- VRP term structure: front-month vs back-month VRP spread as carry signal.

---

## Key References
- Carr & Wu (2009) "Variance Risk Premium"
- Bollerslev, Tauchen, Zhou (2009) "Expected Stock Returns and Variance Risk Premium"
- Bali & Zhou (2016) "Risk, Uncertainty, and Expected Returns"
- Deribit DVOL documentation and methodology notes

---

## Quick Exercise
Take 1 week of BTC end-of-day options data for 3 strikes (ITM, ATM, OTM) across 3 maturities. Fit SVI to each maturity. Check butterfly arbitrage. Interpolate to price a mid-strike ATM 2-week option and compare with market quote.

---

## Related Skills
- `finance-strategies/variance-risk-premium-execution-workshop`
- `finance-strategies/volatility-surface-smile`
- `finance-strategies/optimal-hedging-frequency`
- `finance-strategies/delta-hedging-band`
- `finance-strategies/funding-rate-arbitrage`

---

## Search Queries for Refresh
["variance risk premium harvesting 2025 2026", "VRP trading strategy implied realized variance spread", "crypto variance swap Deribit DVOL", "DeFi option vault variance risk premium", "short gamma trading delta hedging VRP"]