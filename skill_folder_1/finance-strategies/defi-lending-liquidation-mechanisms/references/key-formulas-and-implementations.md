# Key Formulas & Implementations: DeFi Lending Liquidation Mechanisms

**Source:** Bank of Canada SWP 2025-12 (Tian & Zhu, March 2025)
**Extracted from:** Main SKILL.md for quick reference during implementation

---

## 1. Liquidator Entry Conditions

### Fixed-Spread (Aave, Compound, dYdX)
```
e^{-η_f^*} · π_f(γp, l) = C

π_f(γp, l) = min(l/(γp), 1) · (p - γpR)

η_f^*(p,l) = log π_f(γp,l) - log C    (if π_f > C)
```

### Auction-Based (MakerDAO Descending Multi-Unit)
```
e^{-η_a^*} · π_a(δp, l) = C

π_a(b, l) = min(l/b, 1) · (p - bR),  b ≥ δp

η_a^*(p,l) = log π_a(δp,l) - log C    (if π_a > C)
```

**Where:**
- η* = liquidator ratio (active / potential)
- C = fixed entry cost (gas + infrastructure + opportunity cost)
- γ = liquidation discount (e.g., 0.15 = 15%)
- δ = auction floor price fraction (e.g., 0.95 = 95% of market)
- p = oracle/market price
- l = loan size
- R = repayment ratio (1 + interest rate)

---

## 2. Expected Liquidation Quantities

### Fixed-Spread
```
q_f(p,l) = 
  0                                         if (1-γR)l/γ ≤ C
  l/(γp) - C/((1-γR)p)                      if C < (1-γR)l/γ < (1-γR)p
  1 - C/((1-γR)p)                           if γp ≤ l
```

### Auction
```
q_a(p,l) = piecewise (see paper Proposition 3)
```

---

## 3. Price Impact Comparison (Empirical)

| Metric | Fixed-Spread | Auction |
|--------|--------------|---------|
| Price drop/liquidation | **0.054%** | **0.01%** |
| Avg liquidation discount | Fixed (5-15%) | Endogenous (~7.6% VW) |
| Flash loan usage | No | **92%** |

---

## 4. Cascade Risk Indicators

### Fixed-Spread Protocol
```
P(cascade) ∝ (1 - η_f^*) · (max_LTV - current_LTV)^(-1) · (gas_price / 100)
```

### Auction Protocol
```
P(cascade) ∝ (1 - η_a^*) · (1 - restart_rate) · (gas_price / 100)
```

---

## 5. Protocol Selection for Leveraged Positions

```
Fixed-spread max leverage = 1 / (LTV_max + liquidation_discount)
Auction max leverage      = 1 / LTV_max  (discount endogenous, typically <5%)
```

---

## 6. Python Implementation Snippets

### Liquidator Profitability Check
```python
def fixed_spread_profitable(gamma, p, l, R, C):
    """Returns (is_profitable, net_profit)"""
    max_recoverable = l / (gamma * p)
    profit_per_unit = (1 - gamma) * p
    total_profit = max_recoverable * profit_per_unit
    return total_profit > C, total_profit - C

def auction_profitable(delta, p, l, R, C):
    """Returns (is_profitable, net_profit) at floor price"""
    collateral_needed = max(l / (delta * p), 1)
    profit = min(l / (delta * p), 1) * (p - delta * p * R)
    return profit > C, profit - C
```

### Cascade Risk Scoring
```python
def cascade_risk_score(protocol, current_ltv, max_ltv, eta, gas_price, restart_rate=0):
    if protocol == "fixed-spread":
        return (1 - eta) * (max_ltv - current_ltv) ** -1 * (gas_price / 100)
    elif protocol == "auction":
        return (1 - eta) * (1 - restart_rate) * (gas_price / 100)
    return 0
```

### Mechanism Choice Decision
```python
def choose_protocol(entry_cost_C, gamma, delta, p, l, R):
    """Returns 'fixed-spread', 'auction', or 'neither'"""
    fs_profit = min(l/(gamma*p), 1) * (p - gamma*p*R)
    auc_profit = min(l/(delta*p), 1) * (p - delta*p*R)
    
    fs_viable = fs_profit > entry_cost_C
    auc_viable = auc_profit > entry_cost_C
    
    if fs_viable and auc_viable:
        return "auction" if auc_profit > fs_profit else "fixed-spread"
    elif fs_viable:
        return "fixed-spread"
    elif auc_viable:
        return "auction"
    return "neither"
```

---

## 7. Key Thresholds (from paper)

- **C̲ (lower entry cost threshold):** Below this, auction competition effect dominates → auctions amplify shocks LESS
- **C̄ (upper entry cost threshold):** Above this, fixed-spread may have fewer liquidations
- **Dominant region:** Low C (modern flash-loan enabled markets) → prefer auction-based protocols

---

## 8. Assessment Reference

**Q1:** Why auction benefits borrowers, fixed-spread benefits validators?
> A: Fixed-spread competition = gas tip bidding → validators capture surplus. Auction competition = price bidding → borrowers get higher collateral price.

**Q2:** Profitable fixed-spread liquidation? C=$500, γ=0.10, p=$2000, l=50 ETH, R=1.02
> A: max_recoverable = 50/(0.10*2000) = 25 ETH. profit_per_unit = 0.90*2000 = $1800. total = 25*1800 = $45,000 > $500. **Yes, highly profitable.**

**Q3:** MakerDAO auction parameter tuning for high volatility?
> A: Increase δ (higher floor), slower decrement rate, longer duration → reduce restart rate, give bidders more time.

**Q4:** When prefer Aave over Maker for 3x ETH long?
> A: When LTV allows (Aave may offer higher max LTV), and you accept 5-15% fixed discount slippage. Prefer Maker when cascade risk is primary concern.