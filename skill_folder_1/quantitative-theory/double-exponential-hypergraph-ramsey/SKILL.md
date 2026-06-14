---
name: double-exponential-hypergraph-ramsey
description: >
  Teach the 2026 complete resolution (Du, Hu, Liu, Wang, arXiv:2604.23986) of the 54-year-old
  Erdős-Hajnal conjecture on tower growth rates for off-diagonal hypergraph Ramsey numbers.
  Covers the double-exponential lower bound r₄(5,n) ≥ 2^(2^(c n^(1/7))), the stepping-up construction
  with δ-sequence classification, case analysis via local extrema, and the resulting corollary
  rₖ(k+1,n) ≥ twrₖ₋₁(c n^(1/7)) for all k ≥ 4. Use when teaching extremal combinatorics,
  Ramsey theory, hypergraphs, the probabilistic method, or stepping-up techniques.
---

# Double-Exponential Lower Bound for Hypergraph Ramsey Numbers

## 1. Problem Statement

**Definition:** For k ≥ 2, a **k-graph** is a k-uniform hypergraph (edges are k-element subsets).  
Let Kₛ⁽ᵏ⁾ be the complete k-graph on s vertices.  
The **off-diagonal hypergraph Ramsey number** rₖ(s,n) is the smallest N such that every N-vertex k-graph contains either Kₛ⁽ᵏ⁾ or an independent set of size n.

**Tower function:** twr₁(x) = x; twrᵢ₊₁(x) = 2^(twrᵢ(x)).

**Erdős–Hajnal Conjecture (1972):** For 4 ≤ k < s, rₖ(s,n) ≥ twrₖ₋₁(Ω(n)).

## 2. Historical Timeline

| Year | Authors | Result |
|------|---------|--------|
| 1972 | Erdős & Hajnal | Conjectured tower growth; proved r₄(7,n) ≥ 2^(2^Ω(n)) |
| 2013 | Conlon, Fox, Sudakov | Modified stepping-up; holds for s ≥ ⌈5k/2⌉ - 3 |
| 2017/18 | Mubayi & Suk; Conlon, Fox, Sudakov | Verified for k ≥ 4, s ≥ k+3 |
| 2018 | Mubayi & Suk | rₖ(k+1,n) ≥ twrₖ₋₂(n^Ω(log n)); rₖ(k+2,n) ≥ twrₖ₋₁(Ω(n^(1/5))) |
| **2026** | **Du, Hu, Liu, Wang** | **r₄(5,n) ≥ 2^(2^(c n^(1/7))) — final case resolved** |

The entire problem reduced to proving a double-exponential lower bound for r₄(5,n).

## 3. Main Theorem

**Theorem 1.2 (Du–Hu–Liu–Wang 2026):**  
For all n ≥ 5, ∃ absolute c > 0 such that  
**r₄(5,n) ≥ 2^(2^(c n^(1/7)))**.

**Corollary:** For n > k ≥ 5, rₖ(k+1,n) ≥ twrₖ₋₁(c n^(1/7)).

## 4. Stepping-Up Construction (Core Technique)

### 4.1 δ-Notation

Fix D > 0, V = {0, 1, ..., 2ᴰ - 1}.  
For v ∈ V: v = Σᵢ v(i)2ⁱ, v(i) ∈ {0,1}.  
**δ(u,v)** = largest i where u(i) ≠ v(i).  
For ordered r-tuple S = (v₁,...,vᵣ): δ(S) = (δ(v₁,v₂), ..., δ(vᵣ₋₁,vᵣ)).

**Key properties:**
- **Property I:** δ(u,v) ≠ δ(v,w) for u < v < w
- **Property II:** δ(v₁,vᵣ) = maxⱼ δ(vⱼ,vⱼ₊₁)
- **Property III:** For v₁ < v₂ < v₃ < v₄, if δ₁ > δ₂ then δ₁ ≠ δ₃ (if δ₁ < δ₂, δ₁ = δ₃ possible)
- **Fact 2.1:** Any non-monotone sequence with no equal consecutive elements contains a local extremum

### 4.2 Base Coloring (Lemma 3.1)

For every n ≥ 5, ∃ c₀ > 0 and a red/blue coloring φ of pairs of {0,1,...,⌊2^(c₀n)⌋-1} such that **every n-set A contains a 3-tuple aᵢ < aⱼ < aₖ with φ(aᵢ,aⱼ) = φ(aⱼ,aₖ) ≠ φ(aᵢ,aₖ)**.

*Proof idea:* Random 2-coloring; use a partial Steiner (n,3,2)-system with c'n² edges; probability a bad 3-tuple occurs is (3/4)^(c'n²); union bound over (D choose n) subsets < 1/2 for small c₀.

### 4.3 The 4-Graph H

Let U = {0,1,...,⌊2^(c₀n)⌋-1} with coloring φ from Lemma 3.1.  
Let N = 2^⌊2^(c₀n)⌋, V(H) = {0,1,...,N-1}.

For 4-tuple e = (v₁,v₂,v₃,v₄) with v₁ < v₂ < v₃ < v₄, let δᵢ = δ(vᵢ,vᵢ₊₁).

**e ∈ E(H) iff one of:**

| Case | δ-sequence type | φ-condition |
|------|-----------------|-------------|
| (i) | (δ₁,δ₂,δ₃) strictly monotone | φ(δ₁,δ₂) = φ(δ₂,δ₃) ≠ φ(δ₁,δ₃) |
| (ii) | δ₁ > δ₂ < δ₃, and δ₁ > δ₃ | φ(δ₁,δ₂) = φ(δ₁,δ₃) ≠ φ(δ₂,δ₃) |
| (iii) | δ₁ > δ₂ < δ₃, and δ₁ < δ₃ | φ(δ₁,δ₂) = φ(δ₁,δ₃) = φ(δ₂,δ₃) |

## 5. Proof That H is K₅⁽⁴⁾-Free

**Claim 3.2:** For any 5-tuple P = (v₁,...,v₅), δ(P) is **not** a monotone sequence.

*Proof:* If δ(P) increasing, case (i) forces:
- φ(δ₁,δ₂) = φ(δ₂,δ₃) ≠ φ(δ₁,δ₃)
- φ(δ₂,δ₃) = φ(δ₃,δ₄) ≠ φ(δ₂,δ₄)

Then (v₁,v₂,v₄,v₅) has δ = (δ₁ < δ₃ < δ₄) but φ(δ₃,δ₄) ≠ φ(δ₁,δ₃) → not an edge → contradiction.

By Fact 2.1 and Claim 3.2, ∃ i ∈ {2,3} where δᵢ is a **local extremum**.

- **Local maximum** → immediate contradiction in all subcases
- **Local minimum** (δᵢ₋₁ > δᵢ < δᵢ₊₁) → three-case analysis using the edge conditions and Property III (δ₁ < δ₂ < δ₃ ⇒ δ₁ = δ₃ possible) to derive contradictions.

## 6. Independence Number Bound

Any independent set of size n in H gives an n-set in U. By Lemma 3.1, this n-set must contain a bad 3-tuple, violating the edge conditions. So **α(H) < n**.

Since N = 2^⌊2^(c₀n)⌋, we get r₄(5,n) > N ≥ 2^(2^(c n^(1/7))) for some c > 0.

## 7. Teaching Exercises

1. **Verify Property III:** For v₁ < v₂ < v₃ < v₄, prove that if δ₁ > δ₂ then δ₁ ≠ δ₃. Give an example where δ₁ < δ₂ and δ₁ = δ₃.

2. **Steiner system in Lemma 3.1:** Explain why a partial Steiner (n,3,2)-system is the right structure. What happens if we use a different design?

3. **Monotone contradiction:** Walk through the Claim 3.2 proof step by step for the increasing sequence. Why does (v₁,v₂,v₄,v₅) give a contradiction?

4. **Local minimum case (i=2):** Given δ = (δ₁ > δ₂ < δ₃ < δ₄), derive the contradiction using edge cases (ii) and (iii). What role does Property III play?

5. **Tower growth:** Explain why iterated stepping-up from r₄(5,n) gives rₖ(k+1,n) ≥ twrₖ₋₁(Ω(n^(1/7))). Where does the n^(1/7) come from?

6. **Generalization attempt:** The construction uses 4-graphs and 3-tuples in the base coloring. What breaks if we try to adapt this for r₅(6,n) directly?

## 8. Key Takeaways

- **Complete resolution** of a 54-year conjecture is rare; this is a landmark result
- **Stepping-up** remains the fundamental tool for hypergraph Ramsey lower bounds
- **δ-sequence classification** into monotone / local min / local max is the clean organizing principle
- **Base graph coloring** via Steiner systems + probabilistic method is a reusable technique
- The n^(1/7) exponent comes from careful constant tracking through the union bound in Lemma 3.1