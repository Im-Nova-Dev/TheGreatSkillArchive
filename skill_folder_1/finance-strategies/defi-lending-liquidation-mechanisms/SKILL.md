---
name: defi-lending-liquidation-mechanisms
category: finance-strategies
description: |
  Teach the mechanics, comparison, and practical implications of fixed-spread vs auction-based liquidation mechanisms in DeFi lending protocols (Aave, Compound, MakerDAO). Covers price impact formulas, liquidator game theory, cascade risk assessment, and actionable execution rules for traders and liquidators.
tags:
  - defi
  - lending-protocols
  - liquidation
  - market-microstructure
  - aave
  - compound
  - makerdao
  - auction-design
  - cascade-risk
  - flash-loans
---

# DeFi Lending Liquidation Mechanisms: Teaching Skill

**Source:** Bank of Canada Staff Working Paper 2025-12 (Tian & Zhu, March 2025)
**Intel File:** `/home/nova/.hermes/intel/finance/2026-06-06_defi-lending-liquidation-mechanisms-fixed-spread-vs-auction.md`

---

## When to Use This Skill

- Designing leveraged strategies on DeFi lending protocols
- Evaluating protocol risk for capital allocation
- Building liquidator bots or MEV searchers for liquidations
- Risk management for lending protocol exposure
- Teaching DeFi lending mechanics to quant teams

---

## Core Concepts (30-Minute teachable unit)

### 1. Two Mechanism Classes (5 min)

| Mechanism | Protocols | Key Feature |
|-----------|-----------|-------------|
| **Fixed-Spread** | Aave, Compound, dYdX | Collateral sold at fixed discount γ from oracle price |
| **Auction-Based** | MakerDAO | Dutch descending auction starting above market, bids executed immediately |

### 2. The Critical Difference: Where Competition Benefits Go (5 min)

- **Fixed-spread:** Competition → gas tips to **validators**
- **Auction:** Competition → higher collateral price to **borrowers**

### 3. Two Countervailing Effects (5 min)

| Effect | Auction Outcome | Mechanism |
|--------|-----------------|-----------|
| Entry Effect | **More liquidations** (extensive margin) | Higher expected profit → more liquidators enter |
| Competition Effect | **Less collateral per liquidation** (intensive margin) | Bidding up price → less collateral needed to repay debt |

**Dominant when C < C̲:** Competition effect wins → Auctions amplify shocks LESS

### 4. Key Formula: Liquidator Entry Condition (5 min)

```
Fixed-Spread:  e^{-η_f^*} · π_f(γp,l) = C
Auction:       e^{-η_a^*} · π_a(δp,l) = C
```

Where:
- η* = liquidator ratio (active liquidators / potential)
- C = fixed entry cost (gas, infrastructure, opportunity cost)
- π = expected profit per liquidation

### 5. Price Impact Comparison (5 min)

| Metric | Fixed-Spread | Auction |
|--------|--------------|---------|
| Price drop/liquidation | **0.054%** | **0.01%** |
| Liquidation discount | Fixed (5-15%) | Endogenous |
| Flash loan usage | No | **92% of auctions** |

### 6. Actionable Rules (5 min)

**For leveraged position sizing:**
```
If protocol = fixed-spread:  max_leverage = 1 / (LTV_max + liquidation_discount)
If protocol = auction:       max_leverage = 1 / LTV_max  (discount is endogenous, typically <5%)
```

**For cascade probability monitoring:**
```
P(cascade_fixed) ∝ (1 - η_f^*) · (max_LTV - current_LTV)^(-1)
P(cascade_auction) ∝ (1 - η_a^*) · (1 - restart_rate)
```

---

## Lecture/Demo Outline (90 min session)

### Part 1: Theoretical Framework (30 min)
1. Model setup: crypto supply, exchange equilibrium, loan heterogeneity
2. Two-stage liquidator game: entry + competition
3. Derive expected liquidation quantities q_f(p,l) and q_a(p,l)
4. Proposition 4: Amplification effect ranking by entry cost threshold

### Part 2: Empirical Evidence (20 min)
1. Ethereum mainnet data methodology
2. Price impact measurements: 0.054% vs 0.01%
3. Liquidator profit distribution analysis
4. Flash loan dominance in Maker auctions (92%)

### Part 3: Practical Applications (25 min)
1. Protocol selection decision tree
2. Liquidator bot architecture for each mechanism
3. Risk dashboard: η*, gas/C ratio, restart rate, concentration
4. Cross-protocol arb: liquidate on Aave, repay on Maker

### Part 4: Workshop Exercise (15 min)
- Given: gas price = 50 gwei, ETH = $2500, position = 100 ETH at 75% LTV
- Calculate: Is fixed-spread or auction liquidation profitable?
- Compute: Expected price impact for each mechanism
- Decide: Which protocol to use for this position size?

---

## Reference Implementation Snippets

### Liquidator Profitability Check (Fixed-Spread)
```python
def fixed_spread_profitable(gamma, p, l, R, C):
    """
    gamma: liquidation discount (e.g., 0.15 for 15%)
    p: oracle price
    l: loan size
    R: repayment ratio (1 + interest)
    C: entry cost (gas + infrastructure)
    """
    profit_per_unit = (1 - gamma) * p
    max_recoverable = l / (gamma * p)
    required = max_recoverable * profit_per_unit > C
    return required, profit_per_unit * max_recoverable - C
```

### Liquidator Profitability Check (Auction)
```python
def auction_profitable(delta, p, l, R, C):
    """
    delta: auction floor price as fraction of market (e.g., 0.95)
    """
    min_collateral = max(l / (delta * p), 1)
    profit = min(l / (delta * p), 1) * (p - delta * p * R)
    return profit > C, profit - C
```

### Cascade Risk Indicator
```python
def cascade_risk_score(protocol, current_ltv, max_ltv, eta, gas_price, restart_rate=0):
    """
    Higher score = higher cascade probability
    """
    if protocol == "fixed-spread":
        return (1 - eta) * (max_ltv - current_ltv) ** -1 * (gas_price / 100)
    elif protocol == "auction":
        return (1 - eta) * (1 - restart_rate) * (gas_price / 100)
```

---

## Assessment Questions

1. **Conceptual:** Why does the auction mechanism benefit borrowers while fixed-spread benefits validators?
2. **Quantitative:** Given C = $500, γ = 0.10, p = $2000, l = 50 ETH, R = 1.02, is a fixed-spread liquidation profitable?
3. **Design:** How would you modify the MakerDAO auction parameters (δ, decrement rate, duration) to reduce restart rate during high volatility?
4. **Strategy:** When would you prefer Aave over Maker for a 3x leveraged ETH position? When would you prefer Maker?

---

## Related Skills

- `finance-strategies/basis-trade-clawback-management` — defensive exit for basis trades
- `finance-strategies/mev-and-decentralized-ordering` — MEV context for liquidation competition
- `finance-strategies/finance-market-microstructure` — order book dynamics during liquidation waves
- `finance-strategies/orderbook-resilience-discrete-events` — liquidation cascade as discrete event

---

## Support Files

- `references/key-formulas-and-implementations.md` — Key mathematical formulas, Python snippets, and assessment answers extracted for quick reference during implementation
- `references/tian-zhu-2025-key-excerpts.md` — Verbatim key propositions, empirical results, and model parameters from the source paper (Bank of Canada SWP 2025-12)

---

## Further Reading

1. Tian & Zhu (2025). *Liquidation Mechanisms and Price Impacts in DeFi*. Bank of Canada SWP 2025-12.
2. "Locked in, levered up: Risk, return, and ruin in DeFi lending" (ScienceDirect, 2025) — 7.6% avg VW discount in auctions
3. Aave V3 / Compound V3 / MakerDAO Protocol Docs — current liquidation parameters
4. Flashbots MEV-Boost docs — liquidator bundle construction