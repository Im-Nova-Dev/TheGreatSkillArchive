---
name: empty-convex-k-holes-extremal
description: Teach the 2026 Suk–Zhou bounds (arXiv:2606.05721) on the maximum number of k-holes (empty convex k-gons) in planar point sets that avoid (k+1)-holes. Covers the Hardy–Littlewood circle method context, the empty hexagon theorem (Gerken/Nicolás), Horton sets, and the new polynomial bounds with exponent gap ~k/6. Use when studying combinatorial geometry, Erdős problems, extremal combinatorics, or point set analysis.
category: quantitative-theory
---

# Empty Convex $k$-Holes: Extremal Bounds

## Core Result (Suk–Zhou 2026)

For each fixed $k \ge 6$, let $h_k(n)$ be the maximum number of $k$-holes (empty convex $k$-gons) determined by an $n$-point set in general position with **no $(k+1)$-hole**. Then there exist absolute constants $c_1, c_2 > 0$ such that:

$$\left(\frac{c_1}{k}\right)^{\lfloor k/3 \rfloor} n^{\lfloor k/3 \rfloor} \;\le\; h_k(n) \;\le\; \left(\frac{c_2}{k}\right)^{\lceil k/2 \rceil} n^{\lceil k/2 \rceil}$$

**Exponent gap:** $\lceil k/2 \rceil - \lfloor k/3 \rfloor \approx k/6$. Exact growth remains open.

---

## Background: The Erdős Empty Polygon Problem

| Year | Result | Authors |
|------|--------|---------|
| 1978 | Every large set has a 5-hole | Harborth |
| 2007 | Every large set has a 6-hole | Gerken; Nicolás (independently) |
| 1983 | Arbitrarily large sets with **no 7-hole** | Horton |

**Key insight:** 6-holes are **unavoidable**, but 7-holes can be avoided. This paper studies the *maximum* number of $k$-holes you can pack while avoiding $(k+1)$-holes.

---

## Key Definitions

- **$k$-hole:** Empty convex $k$-gon (no other points in its interior)
- **General position:** No three points collinear
- **$h_k(n)$:** Maximum number of $k$-holes in an $n$-point set with **no $(k+1)$-hole**

---

## Asymptotic Bounds Table

| $k$ | $\lfloor k/3 \rfloor$ | $\lceil k/2 \rceil$ | Lower Bound | Upper Bound |
|-----|----------------------|---------------------|-------------|-------------|
| 6   | 2                    | 3                   | $\Omega(n^2/k^2)$ | $O(n^3/k^3)$ |
| 7   | 2                    | 4                   | $\Omega(n^2/k^2)$ | $O(n^4/k^4)$ |
| 8   | 2                    | 4                   | $\Omega(n^2/k^2)$ | $O(n^4/k^4)$ |
| 9   | 3                    | 5                   | $\Omega(n^3/k^3)$ | $O(n^5/k^5)$ |
| 10  | 3                    | 5                   | $\Omega(n^3/k^3)$ | $O(n^5/k^5)$ |
| 11  | 3                    | 6                   | $\Omega(n^3/k^3)$ | $O(n^6/k^6)$ |
| 12  | 4                    | 6                   | $\Omega(n^4/k^4)$ | $O(n^6/k^6)$ |

---

## Proof Ideas (9-page paper — highly compact)

### Lower Bound Construction
1. **Start with Horton set:** $n$-point set with *no 7-hole* (hence no $(k+1)$-hole for any $k \ge 6$)
2. **Perturb iteratively** to create many $k$-holes while preserving the no-$(k+1)$-hole property
3. **Technique:** "Stretching" along carefully chosen directions; each stretch creates $\Theta(n^{\lfloor k/3 \rfloor})$ new $k$-holes
4. **Key combinatorial tool:** Analysis of *order types* and *allowable sequences*

### Upper Bound
1. **Double counting** of "chains" of nested holes
2. **Crossing number** arguments on the arrangement of convex hulls of holes
3. **Induction** on $k$ using the fact that a $k$-hole contains many $(k-1)$-holes
4. **Bootstrap:** The $\lceil k/2 \rceil$ exponent comes from iterating the $(k-1)$-hole bound

---

## Teaching Exercises

1. **Show:** For $k=6$, the bounds give $\Omega(n^2) \le h_6(n) \le O(n^3)$. Can you construct a set with $\Theta(n^2)$ 6-holes but no 7-hole? (Hint: Perturbed Horton set.)

2. **Explain:** Why does the exponent jump from $\lfloor k/3 \rfloor$ to $\lceil k/2 \rceil$? What geometric obstruction prevents improving either side?

3. **Research:** Can the gap be closed? What structural property of point sets determines whether $h_k(n) = \Theta(n^{\lfloor k/3 \rfloor})$ or $\Theta(n^{\lceil k/2 \rceil})$?

4. **Code:** Implement the Horton set construction and count 6-holes experimentally for small $n$. Verify the $\Omega(n^2)$ growth.

---

## Connections

| Area | Link |
|------|------|
| **Erdős problems** | Classic minimum empty polygon problem |
| **Combinatorial geometry** | Order types, allowable sequences, crossing numbers |
| **Ramsey theory** | $h_k(n)$ relates to induced subgraph Ramsey numbers for convex geometric graphs |
| **Extremal combinatorics** | New extremal function on point sets |

---

## References

- Suk, A., & Zhou, S. (2026). *On the maximum number of $k$-holes in point sets with no $(k+1)$-hole*. arXiv:2606.05721.
- Gerken, T. (2008). *Empty hexagon theorem*. Discrete Comput. Geom.
- Nicolás, C. M. (2007). *The empty hexagon theorem*. Discrete Comput. Geom.
- Horton, J. D. (1983). *Sets with no empty convex 7-gons*. Canad. Math. Bull.