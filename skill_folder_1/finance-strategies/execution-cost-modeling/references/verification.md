# Execution Cost Modeling Reference

**Source:** `/home/nova/.hermes/skills/finance-strategies/execution-cost-modeling/SKILL.md`  
**Date:** 2026-06-05  
**Focus:** Execution cost modeling and implementation shortfall

Refer to the primary skill for full formulas, exercises, and checklists.

## Key Formulas

| Metric | Formula |
|--------|---------|
| Total cost | 0.5 * Spread + Impact + TimingRisk + Fees + Latency |
| Impact (sqrt) | c * sigma * sqrt(Q / ADV) |
| Implementation shortfall | (DecisionPrice - ExecutionPrice) / DecisionPrice - Bench |

## Almgren-Chriss Parameters

- gamma: temporary impact coefficient
- eta: permanent impact coefficient
- T: horizon in days
- sigma: daily volatility
- participation: fraction of ADV

## External Models to Verify From

- [ ] Almgren, T., & Chriss, N. (2001). *Optimal execution of portfolio transactions*.
- [ ] Gatheral, J. (2010). *No-dynamic-arbitrage and market impact*.
- [ ] Kissell, R. (2013). *The Science of Algorithmic Trading and Portfolio Management*.
- [ ] Bouchaud, J. P., et al. (2018). *Trades, quotes and prices: The financial ecology of a stock market*.
- [ ] Kyle, A. S. (1985). *Continuous auctions and insider trading*.
