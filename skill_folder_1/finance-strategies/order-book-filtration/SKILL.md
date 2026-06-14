# Order Book Filtration & Directional Signal Extraction

## Overview
Teaching skill for structural filtration of limit order book (LOB) events to improve directional signal quality. Based on arXiv 2507.22712v1 (2025).

## When to Use
- Building high-frequency directional signals from LOB data
- Filtering transient/noisy orders that degrade alpha
- Validating signal causality vs mere correlation
- Designing market-making or execution alphas

## Core Concepts

### Order Book Imbalance (OBI)
```
OBI(τ,h) = (ΔN^s - ΔN^b) / (ΔN^s + ΔN^b)
```
- ΔN^s = sell-side events in lookback window (τ-h, τ]
- ΔN^b = buy-side events in same window
- Standard window: h = 10s, forecast horizon ξ = 1s

### Three Filtration Schemes (Real-Time Observable)

| Filter | Logic | Formula | Thresholds |
|--------|-------|---------|------------|
| **Lifetime (LF)** | Remove orders surviving < T̄ | T_j = t_exit - t_entry | 100, 500, 1000 ms |
| **Mod Count (MF)** | Remove orders modified > M̄ times | M_j = modification count | 1, 3, 5 |
| **Mod Time (MTF)** | Remove orders with clustered final mods | M_j = time(last_mod - prev_mod) | 50, 100, 200 ms |

All filters applied independently; no lookahead bias.

## Three-Layer Diagnostic Framework

### Layer 1: Contemporaneous Correlation (𝒮^ρ)
- Pearson ρ between filtered OBI and realized returns
- **Use**: Baseline linear association check
- **Limitation**: Symmetric, univariate, noise-sensitive
- **Result**: Filtration enhances correlation

### Layer 2: Discretized Regime Scores
- OBI → 9 bins, Returns → 4 bins (uniform [-1, +1])
- **𝒮^{ρ,Λ}**: Diagonality-weighted cross-correlation
- **𝒮^R**: Regression R² (return regimes ~ OBI regime counts)
- **AR Control**: Fit AR to regime sequences, regress on residuals
- **Result**: Filtration enhances explanatory power

### Layer 3: Hawkes Excitation Norm — *Causal* (𝒮^φ)
```
𝒮^φ = ||Φ_{OBI→Ret} ∘ M||₁
```
- Multivariate Hawkes with sum-of-exponentials kernel
- Extract 4×9 submatrix: OBI regimes → Return regimes
- Mask M: diagonality-weighted (emphasize directionally aligned)
- **Exclude**: Self-excitation (OBI→OBI, Ret→Ret)
- **Result**: Filtration gives **limited causal improvement**

## Critical Finding
> **Trade-based OBI has stronger causal alignment with future price movements than LOB-based OBI.**

Execution flow > Quote flow for directional alpha.

## Implementation Workflow

```python
# 1. Collect tick data
events = collect_lob_events(symbol, venue)  # new, trade, mod, cancel

# 2. Compute raw OBI
obi_raw = compute_obi(events, window=10.0)

# 3. Apply filters
obi_lf = filter_lifetime(events, T_bar=500)      # ms
obi_mf = filter_mod_count(events, M_bar=3)
obi_mtf = filter_mod_time(events, M_bar=100)     # ms
obi_trade = compute_obi(trade_events_only, window=10.0)

# 4. Run diagnostics
for obi_stream in [obi_raw, obi_lf, obi_mf, obi_mtf, obi_trade]:
    s_rho = correlation_score(obi_stream, returns)
    s_regime = regime_scores(obi_stream, returns)
    s_hawkes = hawkes_excitation_norm(obi_stream, returns)
    
    report = {s_rho, s_regime, s_hawkes}

# 5. Select best filter + event type by causal score (𝒮^φ)
```

## Key Pitfalls

1. **Don't optimize only correlation/R²** — They measure association, not causality
2. **Don't ignore trade events** — LOB event OBI is noisier causally
3. **Don't use future-dependent filters** — All three schemes are real-time observable
4. **Don't skip Hawkes diagnostics** — Only way to validate causal signal
5. **Don't over-filter** — Aggressive thresholds remove signal with noise

## Validation Checklist
- [ ] Raw OBI correlation baseline established
- [ ] All three filters tested across threshold grids
- [ ] Three-layer diagnostics computed for each
- [ ] Trade-based OBI benchmark included
- [ ] Causal score (𝒮^φ) used as primary selection criterion
- [ ] Out-of-sample validation on held-out period

## Advanced Extensions

### Diagonality Mask Design
```python
M_ij = 1 / (1 + |i - j|)  # Weight aligned regimes higher
```
Or use learned mask from validation data.

### Hawkes Kernel Selection
- Sum-of-exponentials: Flexible, captures multiple timescales
- Power-law: Heavy-tailed excitation, better for long memory
- Validation: Likelihood + out-of-sample excitation norm

### Regime Binning Sensitivity
- Test OBI bins: 5, 7, 9, 11
- Test Return bins: 3, 4, 5
- Uniform vs quantile binning

## References
- arXiv 2507.22712v1: "Order Book Filtration and Directional Signal Extraction at High Frequency" (2025)
- hftbacktest.readthedocs.io: Market Making with Alpha - Order Book Imbalance tutorial
- Hawkes process literature: Bacry et al. (2015), Bormetti et al. (2015)

## Related Skills
- `finance-strategies/obi-market-making` — OBI for quote skew
- `finance-strategies/vpin-orderflow-toxicity` — Adverse selection measurement
- `finance-strategies/orderbook-microstructure-trading` — Short-horizon signals