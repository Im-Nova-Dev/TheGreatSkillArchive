---
name: isoperimetric-inequalities
description: >
  Teach discrete isoperimetric inequalities on the hypercube, the edge-boundary / threshold method,
  the edge-isoperimetric theorem for Hamming and symmetric graphs, and connections to Boolean
  function analysis, sharp thresholds, and noise sensitivity. Includes theorem statements, proof
  sketches, and compact teaching exercises. Use when studying combinatorics, analysis of Boolean
  functions, theoretical CS, or high-dimensional geometry.
---

# Discrete Isoperimetric Inequalities

## Scope
Covers the classical discrete isoperimetric problem on the hypercube, the Harper / edge-boundary theorem,
Kahn–Kalai–Linial (KKL), and the Margulis–Rohde–Schiffmann connection to Gaussian noise sensitivity.

## 1. The discrete isoperimetric problem
Given a finite graph `G = (V, E)` and a set `S ⊆ V`, the **edge boundary** is

```
∂_E(S) = { {u,v} ∈ E : u ∈ S, v ∉ S }.
```

The isoperimetric problem asks: for fixed `|S| = s`, how small can `|∂_E(S)|` be?

Why it matters: this is the geometry of discrete spaces, and it underlies inequalities for Boolean functions,
random graph thresholds, social-choice impossibilities (e.g., the EK-evenness theorem), and concentration.

## 2. Hypercube edge-isoperimetric theorem (Harper / Bernstein–Lindström)

Setting: `G = Q_n`, the `n`-dimensional hypercube, where vertices are `{0,1}^n` and edges join Hamming distance 1.

**Theorem (Harper).** Among all subsets of fixed size `s`, initial segments of binary order minimize edge boundary.

Equivalently, for `S` of size `s`,
```
|∂_E(S)| ≥ |∂_E({x : x ≤_{bin} t})|
```
where `t` is chosen so that the initial segment has size `s`.

**Idea of proof sketch**:
- Use a compression / shifting argument: repeatedly replace any pair violating order with the lexicographically earlier pair.
- Each compression weakly decreases the boundary and never changes `|S|`.
- After finitely many compressions, `S` becomes an initial segment, so the minimum occurs there.

**Quantitative form**: if `S` has size `2^k`, the minimum boundary is `k·2^k`. More generally the boundary rate is governed by the binary weight.

## 3. Total influence and the KKL theorem

For a Boolean function `f: {0,1}^n → {−1,0,1}` define

```
In_i(f) = Pr_μ[f(x) ≠ f(x ⊕ e_i)]    (influence of coordinate i)
I(f) = Σ_i In_i(f)                    (total influence)
```

**KKL (Kahn–Kalai–Linial, 1988).** For symmetric log-concave product measure (including uniform on the cube),
```
max_i In_i(f) ≥ c · I(f) · log n / n
```
for an absolute constant `c > 0`.

**Why it matters**: this is an isoperimetric inequality in probability space. It constrained conjectures in
social choice (e.g., the EK-evenness theorem) and inspired the “hypercontractivity + log-Sobolev” machinery.

## 4. Noise sensitivity via the “majority is stablest” theorem

Noise operator: `T_ρ f(x) = E_y∼N_ρ(x)[f(y)]`.

**Theorem (Majority is stablest, O'Donnell–Kahn–Kalai–Ole já).** Among all balanced Boolean functions with given `I(f)`,
majority maximizes noise stability at every level `ρ < 1`.

Interpretation: this is a Gaussian-space analogue of discrete isoperimetry via spectral analysis on the hypercube.
It connects:
- Harper-type edge bounds,
- hypercontractivity of the noise operator,
- Gaussian surface-area bounds ( Borell’s inequality ).

## 5. The edge-isoperimetric inequality on symmetric graphs

More generally, for vertex-transitive / Cayley graphs `Γ(G,S)` with symmetric generating set `S`:

```
|∂_E(S)| ≥ |S| · h(G) · min(|S|, |V\ S|)
```

where `h(G)` is the Cheeger constant / expansion constant. Equality is often controlled by sublevel sets of
eigenvectors of the Laplacian (Cheeger’s inequality), linking discrete isoperimetry to spectral graph theory.

## 6. Exercises

### Warm-Up
1. Show that a single vertex in `Q_n` has boundary `n`, and an initial segment of size `2^k` has boundary `k·2^k`.
2. For the cube `Q_n`, compute the exact boundary of the “middle layer” `{x : |x| = n/2}` and compare with Harper’s bound.

### Intermediate
3. Prove the shifting/compression step for Harper’s theorem: show that replacing a pair out of order never increases `|∂_E(S)|`.
4. Use KKL to show that for a monotone Boolean function, if `I(f)` is constant then some coordinate has influence at least `Ω(log n / n)`.
5. For `f` = majority on `{0,1}^n`, compute `In_i(f)` explicitly and verify the `≥ c log n / n` lower bound up to constants.

### Advanced
6. Show that for the noisy cube model with parameter `ρ`, the operator `T_ρ` satisfies hypercontractivity on `L^2` with appropriate `q(p,ρ)`.
7. Prove that any monotone Boolean function on `{0,1}^n` with `Pr[f=1] = 1/2` satisfies `Pr[f(x) ≠ f(y)] ≥ c / √n` for a random edge `{x,y}` of the cube, and relate this to total influence.
8. Derive Cheeger’s inequality in the form `h(G)²/2 ≤ λ₂ ≤ 2h(G)` for a `d`-regular graph where `λ₂` is the smallest nontrivial eigenvalue of `L = I − (1/d)A`.

## 7. References / Further Reading
- Harper, L. H. (1966). *Optimal numberings and isoperimetric problems on graphs*. J. Combinatorial Theory.
- Kahn, J., Kalai, G., & Linial, N. (1988). *The influence of variables on Boolean functions*. FOCS.
- O'Donnell, R. (2014). *Analysis of Boolean Functions*. Cambridge.
- Bobkov, Merker, & Phillips. *Sharp inequalities via rearrangement*.
- Connections to spectral graph theory: Cheeger inequality, higher-order Cheeger / Sipser–Lynch.
- Margulis, Rohde, Schiffmann (1980s–90s) on Gaussian isoperimetry and noise sensitivity.
