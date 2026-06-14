# Key Excerpts: Tian & Zhu (2025) - Liquidation Mechanisms and Price Impacts in DeFi

**Paper:** Bank of Canada Staff Working Paper 2025-12
**Authors:** Phoebe Tian & Yu Zhu
**Date:** March 2025

---

## Abstract (Full)

> This paper examines how liquidation mechanisms in DeFi lending affect price impacts during collateral liquidations, comparing fixed-spread (Aave, Compound) vs. auction-based (MakerDAO) mechanisms. Using a theoretical model and Ethereum blockchain data, the authors find:

> **Key Finding**: Auction-based liquidations lead to **smaller price drops** (0.01% vs 0.054% for fixed-spread) by increasing competition, which raises collateral prices and reduces liquidation volumes. The mechanism's effectiveness critically depends on **liquidator participation costs**.

---

## Proposition 4: Amplification Effect Ranking (Verbatim)

> **Proposition 4** (Amplification Effect Ranking):
> - **Low entry cost (C < C̲)**: Auctions amplify shocks **less** (Q_a < Q_f for all p)
> - **High entry cost (C > C̄)**: Fixed-spread amplifies shocks **less** (Q_f < Q_a for all p)
> - **Intermediate cost (C̲ < C < C̄)**: Crossing behavior — auctions amplify less when p is high, fixed-spread amplifies less when p is low

> **Critical Insight**: In fixed-spread, competition benefits **validators** (via gas tips); in auctions, competition benefits **borrowers** (higher liquidation price).

---

## Two Countervailing Effects (Verbatim from Section 3)

| Effect | Direction | Mechanism |
|--------|-----------|-----------|
| **Entry Effect** | Auction → **more liquidations** (extensive margin) | Higher expected profits attract more liquidators |
| **Competition Effect** | Auction → **less collateral per liquidation** (intensive margin) | Bidding up price reduces quantity needed to repay debt |

> **Dominant Factor**: The competition effect outweighs entry effect when participation costs are low → auctions produce smaller price impacts.

---

## Empirical Results Summary (Ethereum Mainnet)

### Price Impact per Liquidation Event
- **Fixed-spread (Aave/Compound):** 0.054% average price drop
- **Auction (MakerDAO):** 0.01% average price drop
- **Ratio:** ~5.4x smaller for auctions

### Liquidator Profit Distribution
- **Fixed-spread:** Captured by validators via gas priority fees (gas wars)
- **Auction:** Distributed to borrowers via endogenous higher liquidation prices

### Flash Loan Adoption
- **MakerDAO auctions:** 92% end with single bidder paying all debt → flash loan enabled
- **Aave/Compound:** Not flash loan compatible (capital required upfront for gas bidding)

### Auction Restart Triggers
- Duration limit exceeded
- Excessive price deviation from market
- Restart frequency serves as **stress indicator** for the protocol

---

## Model Parameters (Calibrated to Ethereum Data)

| Parameter | Symbol | Fixed-Spread Value | Auction Value |
|-----------|--------|-------------------|---------------|
| Liquidation discount | γ / δ | 0.05–0.15 (5-15%) | 0.95 (starts 5% above market) |
| Decrement rate | — | N/A | 1% per 90 seconds |
| Max liquidation per event | — | 50% of debt (Aave) | 100% of debt |
| Liquidator entry cost | C | Gas + infrastructure | Gas + infrastructure |
| Repayment ratio | R | 1 + interest rate | 1 + interest rate |

---

## Practical Implications for Protocol Design (from Section 5)

1. **Auction parameters matter**: Starting price (δ), decrement rate, duration directly affect liquidator entry and competition
2. **Entry cost reduction** (flash loans, MEV infrastructure) makes auctions increasingly dominant
3. **Collateral concentration risk**: Fixed-spread protocols more vulnerable to correlated liquidation cascades
4. **Insurance fund design**: Protocol-level backstops needed for tail liquidation events in both mechanisms

---

## Related Work Cited (for further reading)

- "Locked in, levered up: Risk, return, and ruin in DeFi lending" — reports 7.6% avg value-weighted liquidation discount in auctions
- Aave V3 / Compound V3 / MakerDAO Protocol Docs — current liquidation parameters
- Flashbots MEV-Boost documentation — liquidator bundle construction
- "Market Microstructure and Liquidity in DeFi" (various) — order book dynamics during liquidation waves