# Theorems and Proof Details

## Main Theorem (Theorem 1.2)
Let pp(n) be the number of partitions of n into primes. Then:
```
log pp(n) ~ 2π √(n / 3 log n)
```
More precisely, for any ε > 0 and sufficiently large n:
```
exp((1-ε) * 2π/√3 * √(n/log n)) ≤ pp(n) ≤ exp((1+ε) * 2π/√3 * √(n/log n))
```

## The Three-Step Recipe (R1–R3)

### R1: Recursive Formula (Lemma 3.1)
For any non-decreasing σ: ℕ₊ → ℕ₊:
```
n · p_σ(n) = Σ_{s∈ℕ} σ(s) · Σ_{k=1}^{n/σ(s)} p_σ(n - σ(s)·k)
```
*Proof:* Double counting. LHS counts pairs (π, *) where π is a σ-partition of n and * is a marked part-position. RHS groups by the marked part's value s (σ(s) possibilities) and multiplicity k.

For primes (σ(s) = p_s, the s-th prime): `pp(n) = p_ℙ(n)`
```
n · pp(n) = Σ_{p≤n} p · Σ_{k=1}^{n/p} pp(n - p·k)
```

### R2: Exponential Sum Bound (Lemma 5.1)
```
Σ_{p∈ℙ} p · e^{-δp} ∼ δ^{-2} / log(1/δ)  as δ → 0
```
*Proof:* Compare to integral using PNT: ∫ x·log x · e^{-ηx·log x} dx.

### R3: Elementary Evaluation
Split sum at k = log²(n):
- **A (small k)**: Use R2 to show A ≤ (1-ε)n
- **B (large k)**: Bound by geometric series to show B ≤ εn

## Upper Bound Proof Sketch (Theorem 1.2)

Set c = 2π/√3, f(x) = √(x/log(10x)), f'(x) = (1 - 1/log(10x)) / (2√(x log(10x)))

**Inductive hypothesis:** pp(m) ≤ K · exp((1+ε)cf(m)) for m < n

**Recursion:** n·pp(n) = Σ_p p · Σ_k pp(n-pk)

**Bound:** ≤ K·exp((1+ε)cf(n)) · Σ_{k=1}^n Σ_p p·exp(-(1+ε)ck·p·f'(n))

Split k at log²(n):
- A = Σ_{k≤log²(n)} ... → Use Lemma 5.1: A ≤ (1-ε)n
- B = Σ_{k>log²(n)} ... → Bound by Σ_a a·exp(-k·a·f'(n)): B ≤ εn

Thus n·pp(n) ≤ K·exp((1+ε)cf(n))·n, giving pp(n) ≤ K·exp((1+ε)cf(n))

## Lower Bound Proof Sketch

**Inductive hypothesis:** pp(m) ≥ K^{-1}·exp((1-ε)cf(m)) for m < n

Restrict to p ≤ n^{3/4} and k ≤ log(n) (so pk ≤ n/10)

Use **second-order Taylor**: f(m-x) ≥ f(m) - x·f'(m) + x²·f''(m)

Sum decomposes: Σ = A - B + C → show Σ ≥ (1-ε)n

## Related Results (Theorems 1.1, 1.3)

### d-Power Partitions (d > 0)
p_d(n) = partitions into ⌊m^d⌋ (m ∈ ℕ)
```
log p_d(n) ~ c_d · n^{1/(d+1)}
c_d = (d+1) · (1/d · Γ(1+1/d) · ζ(1+1/d))^{d/(d+1)}
```

### Plane Partitions
PL(n) = 2D arrays with non-increasing rows/columns
```
log PL(n) ~ (27·ζ(3)/4)^{1/3} · n^{2/3}
```
*Proof uses MacMahon's recursion: n·PL(n) = Σ_t Σ_k t²·PL(n-tk)*

## Key Inequalities (Appendix)

**Lemma A.1:** Σ_{m=1}^∞ m²·e^{-δm} ≤ 2/δ³

**Lemma A.2:** For f(x) = x^d·e^{-δx^d}, a = δ^{-1/d}:
```
Σ_{m=1}^∞ f(m) ≤ ∫₀^∞ f(x)dx + 2·f(a) = Γ(1+1/d)/(d·δ^{1+1/d}) + 2/(e·δ)
```