---
name: euler-pentagonal-number-theorem
description: >
  Teach Euler's pentagonal number theorem and its proofs: the classical Franklin
  bijective/involution argument, the generating-function derivation for partitions,
  and the recent probabilistic proof via a shuffling model (Shane Chern 2025).
  Includes compact exercises and connections to partition recurrences.
tags:
  - combinatorics
  - number-theory
  - partitions
  - generating-functions
  - probability
---

# Euler's Pentagonal Number Theorem

## Identity

For \(|q|<1\):
\[
\prod_{n=1}^{\infty}(1-q^{n})=\sum_{k=-\infty}^{\infty}(-1)^{k} q^{k(3k-1)/2}.
\]

The exponents \(g_k = k(3k-1)/2\) for \(k\in\mathbb{Z}\setminus\{0\}\) are the **generalized pentagonal numbers**:
\[
\ldots, 1, 2, 5, 7, 12, 15, 22, 26, 35, 40, \ldots
\]

## 1. Classical Franklin Bijective Proof

Consider partitions into distinct parts. Their generating function is the LHS product, thought of as
\[
\sum_{n}(E(n)-O(n))q^{n},
\]
where \(E(n)\) / \(O(n)\) count even/odd partitions into distinct parts.

### Involution
Let \(\pi\) be a Ferrers diagram with distinct parts.
- Let \(m\) = length of the smallest row.
- Let \(s\) = length of the rightmost \(45^{\circ}\) diagonal.

**Rule:**
- If \(m > s\): move the rightmost diagonal into a new bottom row. This flips the parity of the number of rows and produces another distinct-part partition (no duplicates because the new row is longer than all existing rows).
- If \(m \le s\): move the bottom row back onto the first \(m\) rows, adding one dot to each, restoring a distinct-part diagram.

This operation is an involution (\(\varphi(\varphi(\pi))=\pi\)). It pairs partitions with opposite parity contributions, so they cancel in the generating function.

### Non-cancelling fixed cases
Cancellation fails exactly when the move is not possible:
1. **Case \(m = s\)** (\(k=m>0\)): diagonal and bottom row meet.
   Resulting shape has \(n=m+(m+1)+\dots+(2m-1)=m(3m-1)/2=g_m\) dots.
   Sign \((-1)^m\) remains: contribution \((-1)^m q^{g_m}\).
2. **Case \(m = s+1\)** (\(k=1-m<0\)): using the new row would duplicate an existing row.
   Dots: \(n=(m-1)+(m)+\dots+(2m-2)=(m-1)(3(m-1)+1)/2=g_{1-m}\).
   Sign \((-1)^{m-1}=(-1)^{1-m}\): contribution \((-1)^k q^{g_k}\).

No other cases survive; all others cancel. This exactly reconstructs the RHS.

## 2. Franklin-to-Partition Recurrence

The ordinary generating function for integer partitions is
\[
\sum_{n\ge0}p(n)q^{n}=\prod_{n\ge1}(1-q^{n})^{-1}.
\]
Multiplying by the theorem gives
\[
\Bigl(\sum_{n\ge0}p(n)q^{n}\Bigr)\Bigl(\sum_{n\ge0}a_n q^{n}\Bigr)=1,
\]
where
\[
a_n=\begin{cases}
(-1)^k & n=g_k,\\[4pt]
0 & \text{otherwise}.
\end{cases}
\]
Equating coefficients yields the classic Euler recurrence:
\[
p(n)=\sum_{k\neq0}(-1)^{k-1}\,p(n-g_k),
\]
with \(p(0)=1\) and \(p(n)=0\) for \(n<0\). Because \(g_k\) grows quadratically, only finitely many terms are non-zero.

## 3. Probabilistic Proof Idea (Shane Chern 2025)

Chern's short proof (published, *Seminaire Lotharingien de Combinatoire* 92, 2025) reinterprets the identity through a **shuffling model** rather than an explicit bijection.
- The product \(\prod_{n\ge1}(1-q^n)\) arises as a probability-generating function over certain combinatorial configurations—essentially signed states of a shuffling process.
- The RHS emerges from conditioning on a distinguished event (generalized pentagonal number) in that model.
- The cancellation becomes a probabilistic symmetry rather than a combinatorial involution.

This proof is noteworthy because it replaces a delicate geometric argument with probabilistic reasoning, providing a new template for identities involving infinite alternating products.

## Exercises

1. Compute the coefficient of \(x^{10}\) in \(\prod_{n\ge1}(1-x^{n})\) using the pentagonal theorem directly.
2. Write the recurrence for \(p(0),\dots,p(20)\).
3. Verify Franklin's involution on the Ferrers diagram of \(4+3+2+1\) vs \(5+2+1\) and show they cancel.
4. (Probabilistic) Explain why a shuffling model naturally produces alternating signs.
