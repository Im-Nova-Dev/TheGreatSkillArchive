# Teaching Exercises

## Exercise 1: Recursion Derivation
**Problem:** Derive the recursion `n · p_A(n) = Σ_{a∈A} a · Σ_{k=1}^{n/a} p_A(n - a·k)` by double counting.
*Hint:* Count pairs (π, i) where π is an A-partition of n and i ∈ {1, ..., n} marks a unit in the partition.

**Solution:** Each A-partition of n has exactly n units. Marking one gives n·p_A(n) pairs. Alternatively, group by the part a containing the marked unit (a choices for position within part a) and the multiplicity k of part a. This yields the RHS.

---

## Exercise 2: Exponential Sum — Integer Powers
**Problem:** For d ∈ ℕ, prove the bound:
```
Σ_{m=1}^∞ m^d · e^{-δ·m^d} ≤ Γ(1+1/d)/(d·δ^{1+1/d}) + 2/(e·δ)
```
*Hint:* Use integral comparison on f(x) = x^d·e^{-δx^d} and the fact that max_x f(x) = 1/(e·δ) at x = δ^{-1/d}.

---

## Exercise 3: Prime Sum Asymptotic
**Problem:** Using the Prime Number Theorem (π(x) ~ x/log x), show:
```
Σ_{p} p·e^{-δp} ~ δ^{-2}/log(1/δ)  as δ → 0
```
*Hint:* Approximate by ∫₂^∞ x·log x · e^{-x·log x·δ} dx, then substitute u = x·log x.

---

## Exercise 4: Upper Bound Induction Setup
**Problem:** For prime partitions, set up the inductive proof of the upper bound:
- Define f(x) = √(x/log(10x))
- Assume pp(m) ≤ K·exp((1+ε)cf(m)) for all m < n
- Show the recursion gives: `n·pp(n) ≤ K·exp((1+ε)cf(n)) · Σ_{k≤n} Σ_p p·exp(-(1+ε)ck·p·f'(n))`
- Explain why splitting at k = log²(n) works

---

## Exercise 5: Lower Bound — Second-Order Taylor
**Problem:** Why does the lower bound require the second-order Taylor expansion while the upper bound only needs first order?
*Answer Sketch:* For lower bound we need f(n-pk) ≥ f(n) - pk·f'(n) + pk²·f''(n). The convexity of f (f'' > 0 for large x) provides a positive quadratic correction that compensates for dropping terms in the sum. Upper bound uses concavity-like inequality f(n-x) ≤ f(n) - x·f'(n) which holds for f(x) = √(x/log x).

---

## Exercise 6: Connection to Classical Partition Function
**Problem:** Compare the prime partition asymptotic to the Hardy-Ramanujan formula:
```
log p(n) ~ π √(2n/3)           (all natural numbers)
log pp(n) ~ 2π √(n/3 log n)     (primes only)
```
Explain heuristically why the prime version has:
- Extra factor √2
- The log n in denominator

*Hint:* Prime density ~ 1/log n means "effective number of parts" scales differently.

---

## Exercise 7: d-Power Partitions — General d
**Problem:** For general d > 0 (not necessarily integer), the parts are ⌊m^d⌋ and ⌈m^d⌉. Explain why the proof needs the parameter η = η(d) such that m^d - 1 ≥ η·m^d for m ≥ 2.

---

## Exercise 8: Plane Partitions and MacMahon
**Problem:** Derive MacMahon's recursion for plane partitions:
```
n·PL(n) = Σ_{t=1}^n Σ_{k=1}^{n/t} t²·PL(n-tk)
```
*Hint:* Think of a plane partition as a 3D Young diagram. The "t" parameter corresponds to ... (complete as teaching exercise).

---

## Discussion Questions

1. **Why "elementary"?** What complex-analytic tools does this avoid? (Circle method, modular forms, generating function singularity analysis)

2. **Adaptability:** The paper claims the three-step recipe works for several partition functions. What property must the part set A have for this to work?

3. **Sharpness:** The bounds have (1±ε) factors. What would be needed to get exact constants like Hardy-Ramanujan?

4. **Computational:** For n = 10^6, estimate log pp(n) using the asymptotic formula. Compare to actual computed values if available.

5. **History:** This paper (2026) gives an elementary proof. What year was the first asymptotic for pp(n)? (Vaughan 1977, using circle method).