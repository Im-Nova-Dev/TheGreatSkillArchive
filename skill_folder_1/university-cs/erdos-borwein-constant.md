---
title: Erdős–Borwein Constant and Reciprocal Odd-Part Sums
tags: [number-theory, rational-series, harmonic-density, 2-adic-valuation]
prerequisites: [basic-number-theory, series-convergence]
---

# Erdős–Borwein Constant and Reciprocal Odd-Part Sums

## 1. The Series

\[
E \;=\; \sum_{n\ge 1} \frac{1}{2^{\nu_2(n)}\,n} \;=\; \sum_{n\ge 1} \frac{1}{\operatorname{odd}(n)} \;=\; 1+\frac{1}{3}+\frac{1}{5}+\frac{1}{7}+\frac{1}{3}+\frac{1}{9}+\cdots
\]

where
- \(\nu_2(n)\) is the 2-adic valuation (exponent of the highest power of 2 dividing \(n\))
- \(\operatorname{odd}(n) = n / 2^{\nu_2(n)}\) strips powers of 2 from \(n\), i.e. the odd part of \(n\)

This constant is known as the **Erdős–Borwein constant**, approximately  
\(E \approx 1.60937\ldots\)

## 2. Why It Converges

Group integers by \(\nu_2(n) = k\). For a fixed \(k \ge 0\), the subset
\(\{n : \nu_2(n)=k\}\) contributes

\[
\frac{1}{2^k} \sum_{m \text{ odd}} \frac{1}{2^k m} \;=\; \frac{1}{4^k}\sum_{m \text{ odd}} \frac{1}{m}.
\]

Since \(\sum_{m\text{ odd}} 1/m\) diverges like \(\frac{1}{2}\log n\) (half of the harmonic series), summing the geometric weights \(1/4^k\) yields a finite limit. The full series

\[
E \;=\; \sum_{k\ge 0} \frac{1}{4^k} \sum_{m\text{ odd}} \frac{1}{m}
\]

converges because the outer geometric factor gives overall \(\sim C \log n\) → finite constant \(E\).

## 3. Key Theorem

**Theorem (Erdős–Borwein style).** The Erdős–Borwein constant \(E\) is **irrational**.

**Proof idea.** Write a generating function:

\[
E \;=\; \sum_{m\text{ odd}} \frac{1}{m} \sum_{j\ge 0} \frac{1}{2^j}
\;=\; \Bigl(\sum_{m\text{ odd}}\frac{1}{m}\Bigr)\cdot 2,
\]

and relate it to the binary-digital expansion of partial sums. The key "irrationality bottleneck" comes from the fact that bin
