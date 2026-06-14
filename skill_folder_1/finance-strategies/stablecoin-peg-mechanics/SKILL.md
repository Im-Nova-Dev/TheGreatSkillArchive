---
title: Stablecoin Peg Mechanics & De-Peg Arbitrage
name: stablecoin-peg-mechanics
description: >
  Teach stablecoin peg restoration dynamics using Mean-Field Game framework.
  Covers primary vs secondary market roles, non-linear breakdown thresholds,
  historical event calibration (USDC/USDT), and actionable execution rules.
triggers:
  - stablecoin peg
  - de-peg arbitrage
  - peg restoration
  - primary market arbitrage
  - secondary market liquidity
  - stablecoin mechanics
  - USDC USDT depeg
---

# Stablecoin Peg Mechanics & De-Peg Arbitrage

## 1. Core Insight

Peg restoration is driven by **primary-market arbitrageurs** when redemption rails function. Secondary-market liquidity alone cannot recover the peg once primary friction exceeds κₚ ≈ 15–18 threshold. Three distinct regimes observed in historical events.

> **Key Finding (Mohanty & Krishnamachari, 2026):** "When primary redemption rails remain open, recovery is dominated by direct redemptions. When primary capacity is impaired but not broken, recovery reflects a joint contribution from primary arbitrage and secondary buying. When venue-level infrastructure failures both obstruct redemptions and fragment liquidity, both channels contribute little, and recovery is slow."

---

## 2. Mathematical Framework: Dynamic Mean-Field Game

### 2.1 Market Structure

```
Primary Market: Treasury ↔ Arbitrageurs (1:1 mint/redeem at $1 peg)
Secondary Market: Exchanges (CEX/DEX) ↔ All agents (free trading)
```

### 2.2 Agent Populations

| Agent Type | Population Share | Market Access | Key Frictions |
|------------|-----------------|---------------|---------------|
| **Retail Traders** | πᵣ = 0.85 | Secondary only | High slippage (κᵣ), inventory aversion (ηᵣ) |
| **Arbitrageurs** | πₐ = 0.15 | Primary + Secondary | Lower frictions (κₐ), primary execution cost (κₚ) |

### 2.3 Mean-Field State

μₜ = (mₜ, Lₜ, ϕₜ, ψₜ) where:
- **mₜ**: Stablecoin mispricing relative to $1 peg
- **Lₜ**: Primary backlog vector across chains
- **ϕₜ**: Aggregate secondary flows across venues
- **ψₜ**: Aggregate primary flows

### 2.4 Price Dynamics (Eq. 3)

```
mₜ₊₁ = mₜ + Σₛ λₛ(πᵣaᵣ,ₛ,ₜ + πₐaₐ,ₛ,ₜ) + Σ꜀ γ꜀(πₐr꜀,ₜ) + εₜ
```

### 2.5 Primary Backlog (Eq. 4)

```
L꜀,ₜ₊₁ = (1-δ꜀)L꜀,ₜ + πₐr꜀,ₜ
```

### 2.6 Stochastic Volatility (GARCH)

```
σₜ² = ω + αεₜ₋₁² + βσₜ₋₁²
κᵢ,ₛ,ₜ = κᵢ,ₛ,₀(1 + cᵢσₜ)
λₛ,ₜ = λₛ,₀(1 + aₛσₜ)
```

---

## 3. Three Historical De-Peg Events Calibrated

| Event | Period | Data Source | Key Characteristic | Primary Rail |
|-------|--------|-------------|-------------------|---------------|
| **USDC Mar 2023** | Mar 11-15, 2023 | Binance 1-min USDC/USD | SVB receivership, weekend pause | **Impaired** |
| **USDT May 2022** | May 12-16, 2022 | Binance 1-min USDT/USD | TerraUSD collapse | **Functional** |
| **USDT Jul 2023** | Jul 15-31, 2023 | Binance USDT/USD | Binance venue outage | **Both impaired** |

### Recovery Half-Lives

| Event | Empirical Half-Life | Model Half-Life | Mechanism |
|-------|---------------------|-----------------|-----------|
| USDT May 2022 | ~2.5 hours | ~2.5 hours | Primary only |
| USDC Mar 2023 | ~12 hours | ~12 hours | Joint primary + secondary |
| USDT Jul 2023 | 30.7 hours | 45.9 hours | Severely delayed |

**Model outperforms baselines:** Avg RMSE 0.0128 vs AR(1) 0.0158, ARMA-GARCH 0.0162

---

## 4. Critical Non-Linear Breakdown Threshold

**Primary friction κₚ ≈ 15–18 is the breakdown point.** Beyond this threshold:
- Half-life explodes non-linearly
- Primary arbitrage channel effectively closes
- Secondary liquidity alone cannot compensate
- Recovery time scales from hours to days

This threshold corresponds to operational failures like:
- Weekend/holiday banking hours (SVB weekend)
- Venue-level infrastructure outages (Binance Jul 2023)
- KYC/gating delays for institutional redemption

---

## 5. Primary vs Secondary Market Access Asymmetry (Fed FEDS Notes, Feb 2024)

| Token | Primary Access | Min Mint | Notes |
|-------|----------------|----------|-------|
| **USDC** | Institutional (application) | ~$1M+ | Direct customers only |
| **USDT** | Institutional (restrictive) | $100K | More gated, Tron-heavy |
| **BUSD** | Halted by NYDFS Feb 2023 | N/A | Only burns possible |
| **DAI** | **Permissionless** (Maker PSM) | Any | 1:1 USDC→DAI via PSM |

> **Critical insight:** If you're not a direct customer with $1M+ minimum, you **cannot** access primary arbitrage for USDC/USDT. Size secondary positions accordingly.

### March 2023 Crisis Timeline
- **Mar 10**: Circle announces $3.3B USDC reserves at SVB
- **Mar 11**: Primary market **paused** (banking hours constraint)
- **Mar 13**: Primary reopens; USDC recovers over ~3 days
- **DEX volumes spiked to >$20B** (historic high) on Mar 11 — **preceded** CEX spike
- **No significant pricing gap** between CEX/DEX despite volume divergence

---

## 6. Actionable Execution Rules

### 6.1 Monitor Primary Backlog (Lₜ)
On-chain mint/burn queues are leading indicators:
- Rising backlog = impaired primary rail → secondary liquidity will dry
- Track Circle/Tether mint/burn events, PSM flows

### 6.2 Track Redemption Eligibility
- If not a direct customer ($1M+ min), no primary access
- DAI via PSM is permissionless → retail-accessible primary arb
- Size secondary positions inversely to primary access

### 6.3 DEX Volume Spike + Stable Price = Warning
- Price stability amid surging DEX volume signals hidden stress
- Order book thinning, not equilibrium
- Monitor Curve 3pool, Uniswap V3 pool imbalances

### 6.4 USDC/USDT Premium Basis Signal
- When USDT > $1 > USDC: primary arb pressure on USDT side
- Expect USDT cap growth, USDC cap decline
- Track funding rate basis (USDC/USDT perp pairs)

### 6.5 Half-Life Based Position Sizing
| Primary Status | Expected Half-Life | Position Scaling |
|----------------|-------------------|------------------|
| Functional | ~2-3 hours | Full size |
| Impaired (weekend/holiday) | ~12 hours | 50% size |
| Both impaired | 24-48+ hours | 25% size or avoid |

---

## 7. Data Sources & Signals

| Source | Signals | Frequency |
|--------|---------|-----------|
| **On-chain** | Mint/burn (Circle, Tether, Maker), PSM flows, DEX pool imbalances | Block-level |
| **CEX** | Funding rate basis, order book depth, VPIN toxicity | Millisecond |
| **Macro** | Banking hours, Fedwire/Settlement windows, event monitoring | Daily |

---

## 8. Related Intel & Skills

### Intel Documents
- `/home/nova/.hermes/intel/finance/2026-06-06_stablecoin-depeg-peg-restoration.md` — Full detailed analysis
- `finance-strategies/cross-asset-macro-liquidity-signals` — Regime-aware risk scaling

### Related Skills
- `finance-strategies/stablecoin-depeg-arbitrage` — (future) specific arb execution
- `finance-strategies/cross-exchange-funding-rate-arbitrage`
- `finance-strategies/orderbook-resilience-discrete-events`
- `finance-strategies/finance-market-microstructure`

---

## 9. Pitfalls

- **Assuming secondary liquidity equals primary access** — it doesn't
- **Ignoring primary rail hours** — weekends/holidays create predictable impairment windows
- **Not monitoring on-chain backlog** — Lₜ is a leading indicator, not lagging
- **Equal sizing across token types** — USDC/USDT gated vs DAI permissionless changes everything
- **Annualizing short-term recovery patterns** — half-life is regime-dependent, not stationary

---

## 10. References

- Mohanty & Krishnamachari (2026): "Who Restores the Peg? A Mean-Field Game Approach to Model Stablecoin Market Dynamics" — arXiv:2601.18991v2 [q-fin.TR]
- Federal Reserve FEDS Notes (Feb 2024): "Primary and Secondary Markets for Stablecoins: Evidence from the March 2023 Crypto Market Stress"
- Code: https://github.com/ANRGUSC/stablecoin-peg-mfg