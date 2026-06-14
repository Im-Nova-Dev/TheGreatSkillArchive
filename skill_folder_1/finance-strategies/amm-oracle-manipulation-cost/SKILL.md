# AMM Oracle Manipulation Cost

**Category:** DeFi / Market Microstructure / Oracle Design
**Difficulty:** Advanced
**Prerequisites:** Constant product AMMs (Uniswap v2), on-chain oracles, basic game theory

---

## Learning Objectives

By the end of this skill, you will be able to:
1. **Define** cost of manipulation for AMM-based oracles in economic terms
2. **Calculate** single-pool and multi-pool manipulation costs using closed-form formulas
3. **Choose** optimal aggregation method (weighted median vs weighted mean) with liquidity weights
4. **Size** oracle parameters (dwell time, rate limits) against explicit attack costs
5. **Audit** existing oracle designs for manipulation vulnerability

---

## Core Concept: Cost of Manipulation

### Framework
- **Attacker** trades against CPMM pools to distort on-chain price oracle
- **Arbitrageurs** restore cross-pool/cross-venue price consistency
- **Oracle Designer** chooses aggregation: weighted mean, weighted median, etc.
- **EMH Assumption:** Off-chain "true" price follows efficient market hypothesis

### Definition
> **Cost of Manipulation (CoM)** = Minimal mark-to-market loss attacker must incur to move the oracle by multiplicative factor α

This is the **economic security** of the oracle — if CoM > potential profit from manipulation, rational attackers won't attack.

---

## Single-Pool Closed-Form Formula

For a constant product AMM (Uniswap v2 style) with TVL = total value locked at true price:

```
Cost(α) = 2 × √TVL × (√α - 1/√α)
```

Where:
- α = target price distortion factor (α > 1 for upward, α < 1 for downward)
- TVL = x + y·p (reserves valued at true price p)

### Example
- Pool: 10,000 ETH / 20,000,000 USDC (price = 2,000 USDC/ETH)
- TVL = 10,000 × 2,000 + 20,000,000 = $40M
- Cost to move price by 10% (α = 1.10):
  - Cost = 2 × √40,000,000 × (√1.10 - 1/√1.10)
  - ≈ 2 × 6,324 × (1.0488 - 0.9535) ≈ **$1,206,000**

---

## Multi-Pool Aggregation: The Attacker-Designer Game

### Aggregation Methods Compared

| Method | Formula | Optimality |
|--------|---------|------------|
| **Weighted Median (liquidity weights)** | median_{w∝depth}(p_i) | **Maximizes min CoM for ANY α** ✅ |
| **Weighted Mean (liquidity weights)** | Σ w_i p_i, w_i ∝ depth_i | Optimal only as α→1; **fragile for large α** ⚠️ |
| Uniform weights | Σ p_i / N | Suboptimal; ignores liquidity |

### Key Theoretical Results

1. **Weighted median with liquidity weights is uniformly optimal** — no matter the target distortion, it maximizes the minimum manipulation cost
2. **Weighted mean with liquidity weights is locally optimal** — only for tiny distortions (α≈1). For large α, optimal weights depend on α; no single choice works for all
3. **With frictionless cross-pool arbitrage**: CoM depends ONLY on total quote depth across pools, and ALL symmetric aggregators coincide

---

## Practical Oracle Design Rules

### 1. Default Choice: Weighted Median + Liquidity Weights
```python
def weighted_median_with_liquidity_weights(prices: list, depths: list) -> float:
    """Robust oracle aggregation — maximizes manipulation cost at all distortion levels."""
    total_depth = sum(depths)
    weights = [d / total_depth for d in depths]
    # Sort by price
    sorted_pairs = sorted(zip(prices, weights))
    cumsum = 0
    for price, weight in sorted_pairs:
        cumsum += weight
        if cumsum >= 0.5:
            return price
```

### 2. Avoid Weighted Mean for Critical Oracles
- Use only for low-stakes oracles with small expected distortions
- Example: Lending protocol liquidation oracle → **must use weighted median**

### 3. Size Oracle Parameters Using Framework
Given target manipulation cost C_min and max acceptable distortion α_max:
```
Required TVL ≥ (C_min / [2 × (√α_max - 1/√α_max)])²
```

Add safety margins:
- **Dwell time**: Minimum blocks oracle value must persist before use (e.g., 10-30 blocks)
- **Rate limit**: Max price change per block (e.g., 1-3% per block)

---

## Audit Checklist for Existing Oracles

| Check | Pass Criteria | Action if Fail |
|-------|---------------|----------------|
| Aggregation method | Weighted median with liquidity weights | Migrate to weighted median |
| Total quote depth | Sufficient for target CoM at α=1.25 | Add liquidity / more pools |
| Cross-pool arbitrage | Active, sub-block latency | Verify arbitrage bots running |
| Dwell time | ≥ 10 blocks (Ethereum) / ≥ 30 blocks (L2) | Increase dwell time |
| Rate limit | ≤ 3% per block | Tighten limit |
| Pool composition | Multiple venues, chains, DEXes | Diversify pool sources |

---

## Extension: Multi-Asset Star Architectures

For oracles pricing asset A via pools A/ETH, A/USDC, ETH/USDC (star topology):
- **Liquidity weights remain optimal** in the same sense
- Manipulation cost determined by minimum over paths to base asset
- Design implication: Ensure sufficient liquidity on ALL legs of the star

---

## References

- **Primary:** Müller, Moumeni, Messaoudi (2026) "Cost of Manipulation in AMM-Based Oracles" — arXiv:2606.03548, FC'26 DeFi Workshop
- **Related:** Feys (2026) "Fairness and Strategy-Proofness in Automated Market Makers" — arXiv:2606.04959
- **Foundational:** Adams et al. (2020) "Uniswap v2 Core" — constant product AMM

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Fix |
|---------|----------------|-----|
| Using TWAP from single pool | Single-pool manipulation cost is low | Aggregate across pools with weighted median |
| Weighted mean with uniform weights | Ignores liquidity; easy to manipulate small pools | Use liquidity-proportional weights |
| No dwell time / rate limit | Attacker can manipulate in single block | Add temporal constraints |
| Ignoring cross-venue arbitrage | Off-chain price can be restored without on-chain cost | Monitor cross-venue basis |

---

## Verification Exercises

1. **Calculate CoM:** Given pool with $50M TVL, what's cost to manipulate by 25%?
2. **Compare aggregations:** Simulate 3 pools with depths [10M, 5M, 2M] and prices [100, 101, 99]. Compute weighted mean vs weighted median. Which is more robust?
3. **Parameter sizing:** Design oracle for lending protocol requiring $10M CoM at 20% distortion. What TVL needed? What dwell time + rate limit?
4. **Audit:** Review Chainlink/Uniswap v3 TWAP oracle — does it use weighted median? What are its manipulation costs?

---

## Related Skills

- `finance-strategies/fairness-strategy-proof-amm` — AMM mechanism design
- `finance-strategies/oracle-design-defi` — Broader oracle design patterns
- `finance-strategies/orderbook-microstructure-fundamentals` — Traditional market microstructure
- `finance-strategies/mev-and-decentralized-ordering` — MEV and oracle manipulation