---
name: van-der-waerden-theorem
description: |
  Teach Van der Waerden's theorem and a new 2026 ultrafilter proof.
  Covers: statement, classical proof strategy, Gallai colorings,
  connections to Hindman's theorem, the compact space βℕ,
  the new short proof that avoids minimal and idempotent ultrafilters,
  exercises, and references.
---

# Van der Waerden's theorem — and a new ultrafilter proof

Use this skill when the topic is Ramsey theory, topological dynamics,
algebra in βℕ, or short/advanced proofs of classical combinatorial theorems.

## 1. Statement

For all positive integers \(r\) (colors) and \(k\) (length), there exists a least integer
\(W(r,k)\) such that every \(r\)-coloring of \(\{1,\dots, W(r,k)\}\)
contains a monochromatic arithmetic progression of length \(k\).

This is the foundational uniform finite-splitting result of Ramsey theory.

## 2. Classical proof strategy

- Reduce to a statement about piecewise syndetic sets.
- Use van der Waerden's original combinatorial covering + induction on \(k\).
- The bound \(W(r,k)\) grows enormously; known bounds are tower-exponential in \(k\).

## 3. Connection to Hindman and to βℕ

- Gallai coloring lemma gives monochromatic pairs \((x,y)\) sharing the same color-class pattern.
- Ultrafilter proofs work in \(\beta\mathbb{N}\), the Stone–Čech compactification.
- Classical Hindman-style arguments typically need **minimal** or **idempotent**
  ultrafilters to extract long monochromatic structures.

## 4. The new 2026 ultrafilter proof (Di Nasso, arXiv:2603.04043)

**Theorem (new simplified proof).** Van der Waerden's theorem holds.
Moreover, the result admits a short proof using only algebra in \(\beta\mathbb{N}\)
**without** invoking minimal or idempotent ultrafilters.

### 4.1 What this changes

Prior ultrafilter proofs required:
- existence of minimal idempotents,
- Ellis–Numakura lemma compactness machinery,
- delicate fixed-point extraction.

The new proof replaces that with:
- direct algebraic closure properties in \(\beta\mathbb{N}\),
- compactness + finite-color Ramsey reduction,
- cleaner infinite-to-finite compactness transfer.

### 4.2 Proof sketch

1. Consider \(\beta\mathbb{N}\) with the usual semiring structure:
   addition and multiplication extended from \(\mathbb{N}\).
2. For an \(r\)-coloring \(c: \mathbb{N} \to \{1,\dots,r}\), each color class
   lifts to the closure of a set in \(\beta\mathbb{N}\).
3. Use compactness/closure to show repeated algebraic structure
   yields a monochromatic IP-like configuration.
4. Transfer the infinite configuration back to a long monochromatic
   arithmetic progression in \(\mathbb{N}\) via ordinary compactness,
   **without** requiring idempotence.

### 4.3 Key insight

The paper shows that a "standard" algebraic argument in \(\beta\mathbb{N}\)
is already strong enough for Van der Waerden's theorem when the goal is
only finite monochromatic progressions, not infinite sets.
This decouples Van der Waerden from the heavier dynamical machinery
usually associated with ultrafilter proofs.

## 5. Why this matters

- Pedagogically: provides a simpler entry point into \(\beta\mathbb{N}\)
  for students.
- Methodologically: shows ultrafilter proofs can be streamlined when
  infinite combinatorial objects are not required.
- Historically: separates Van der Waerden's uniform Ramsey bound
  from Hindman's infinite combinatorial structure theory.

## 6. Compact teaching exercises

1. **Finite reduction.** Show that if \(W(r,k)\) exists, then every coloring of
   \(\{1,\dots,n\}\) with \(n \ge W(r,k)\) contains a monochromatic AP of length \(k\).

2. **Gallai coloring.** Prove that if \((a_n)\) is an injective sequence of natural
   numbers and each pair is colored from \(\{1,\dots,r\}\), then there exists a
   monochromatic subset of the form \(\{a_i, a_j, a_k\}\) with \(i<j<k\) and
   \(a_j-a_i = a_k-a_j\).

3. **βℕ algebra.** Show that for ultrafilters \(p,q \in \beta\mathbb{N}\),
   the definition \(A \in p+q\) iff
   \(\{ n \in \mathbb{N} : \{ m : n+m \in A \} \in q \} \in p\)
   makes \((\beta\mathbb{N}, +)\) a compact right topological semigroup.

4. **Compare to Hindman.**
   Explain why Hindman's theorem (every finite coloring of \(\mathbb{N}\) contains
   an infinite set whose finite sums are monochromatic) strictly requires
   idempotent ultrafilters, while Van der Waerden's theorem does not.

5. **Tower bounds.**
   Show by induction the classical tower-of-twos lower bound on \(W(2,k)\).

## 7. References and sources

- Di Nasso, M. *A new ultrafilter proof of Van der Waerden's theorem*,
  arXiv:2603.04043 [math.LO, math.CO], March 2026.
- van der Waerden, B. L. *Beweis einer Baudetschen Vermutung*,
  Nieuw Arch. Wisk. 15 (1927), 212–216.
- Hindman, N. & Strauss, D. *Algebra in the Stone–Čech compactification*,
  de Gruyter, 2012.
- Furstenberg, H. & Katznelson, Y. *An ergodic Szemerédi theorem*,
  Combinatorica 5 (1985), 215–228.
