# Order Book Microstructure Fundamentals

Teach order book microstructure concepts, order flow imbalance signals, and filtration techniques for high-frequency directional alpha.

## Learning Objectives

- Understand limit order book (LOB) structure and event dynamics
- Calculate and interpret Order Book Imbalance (OBI) and Order Flow Imbalance (OFI)
- Apply structural filtration to remove transient/strategic orders
- Evaluate signal quality using three-layer diagnostic framework
- Distinguish associative vs. causal signal diagnostics

## Core Concepts

### Limit Order Book (LOB) Structure

| Component | Description |
|-----------|-------------|
| Bid/Ask Levels | Price levels with aggregate volume |
| Order Events | Add, cancel, modify, execute, trade |
| Transient Orders | Short-lived, strategic, non-executed orders |

### Order Book Imbalance (OBI)

```
OBI(τ,h) = (ΔN^s - ΔN^b) / (ΔN^s + ΔN^b)
```
- ΔN^s = sell-side events in lookback window
- ΔN^b = buy-side events in lookback window
- Captures *latent* liquidity pressure from standing book volume

### Trade-Based OBI (OBI^T)

```
OBI^T(τ) = (ΔN^(b,T) - ΔN^(s,T)) / (ΔN^(b,T) + ΔN^(s,T))
```
- Captures *realized* directional pressure from actual executions
- Immune to flickering quotes and non-executed strategic placements
- Stronger causal alignment with future price movements

## Three Filtration Schemes (Real-Time Observable)

### 1. Lifetime-Based Filtration (ℱ^𝒯)
```
ℱ^𝒯(ε_t) = {ε_i ∈ ε_t : 𝒯_j ≥ 𝒯̄}
where 𝒯_j = t_j^(2) - t_j^(1)  (entry to exit time)
```
Thresholds: {100, 500, 1000} ms

### 2. Modification Count Filtration (ℱ^M)
```
ℱ^M(ε_t) = {ε_i ∈ ε_t : M_j ≤ M̄}
```
Thresholds: {1, 3, 5}

### 3. Modification Time Filtration (ℱ^ℳ)
```
ℱ^ℳ(ε_t) = {ε_i ∈ ε_t : ℳ_j ≥ ℳ̄}
where ℳ_j = time between last two modifications
```
Thresholds: {50, 100, 200} ms

## Three-Layer Diagnostic Framework

### Layer 1: Contemporaneous Correlation (𝒮^ρ)
- Pearson correlation between filtered OBI and realized returns
- Limitation: Symmetric, univariate, noise-sensitive

### Layer 2: Discretized Regime Scores
- OBI regimes: 9 bins over [-1, +1]
- Return regimes: 4 bins over [-1, +1]
- Metrics: Cross-correlation (𝒮^ρ,Λ), Regression R² (𝒮^ℛ)
- Autocorrelation control via AR model residuals

### Layer 3: Hawkes Excitation Norm (𝒮^φ)
- Multivariate Hawkes process with sum-of-exponentials kernel
- 13×13 kernel matrix (9 OBI + 4 return regimes)
- 𝒮^φ(ℱ) = ||Φ_OBI→Ret ∘ M||_1
- Extracts directional excitation, suppresses spurious self-excitation

## Key Findings (arXiv:2507.22712v1)

1. Filtration enhances directional signal clarity in correlation & regime metrics
2. Limited gains in causal excitation strength (Hawkes norm)
3. Trade-based OBI > any filtered quote-based OBI for causal alignment
4. Filter selection depends on objective (associative vs causal)

## Practical Exercises

1. Compute raw OBI from LOB event stream
2. Apply each filtration scheme with varying thresholds
3. Evaluate all three diagnostic layers
4. Compare against trade-based OBI benchmark
5. Design filter combination for specific trading objective

## Reference Implementation

See: `/home/nova/.hermes/intel/finance/order_book_filtration_directional_signals_2025.md`

## Further Reading

- arXiv:2507.22712v1 - Order Book Filtration and Directional Signal Extraction
- HFTBacktest tutorials on OBI-based market making
- Emergent Mind: Order Flow Imbalance in Market Microstructure