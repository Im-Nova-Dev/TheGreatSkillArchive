---
name: information-theory-entropy-and-coding-basics
description: Teach information theory basics including entropy, source coding, Huffman and Shannon-Fano coding, mutual information, channel capacity, and simple error detection/correction concepts with examples and exercises.
---

# Information Theory, Entropy, and Coding Basics

Use this skill to teach core information-theoretic ideas and intuitive coding results for CS/quant/theory students.

## Scope
- Uncertainty and entropy
- Optimal source coding concepts
- Channel capacity and simple bounds
- Minimum connections to compression and error control

## Teaching Order
1. Start with discrete entropy
2. Use practical coding examples before proving general bounds
3. Connect to probability, combinatorics, and complexity

## 1. Discrete Entropy
- Definition:
  - H(X) = E[-log p(X)] = -Σ p(x) log p(x)
- Units:
  - bits for base 2
  - nats for natural log
- Properties:
  - Maximum over fixed alphabet size when uniform
  - Concavity
  - Chain rule: H(X,Y) = H(X) + H(Y|X)

Intuition: entropy measures average surprise or information per symbol.

## 2. Source Coding and Optimal Compression
- Source coding theorem (discrete memoryless source):
  - expected code length ≳ entropy
- Prefix-free/Huffman coding
  - greedy shortest expected length
  - not always optimal under longer blocks but widely useful
- Kraft-McMillan inequality as feasibility condition
  - Σ 2^{-l_i} ≤ 1 for prefix-free codes

Teaching point: optimal compression is about assigning shorter codewords to more likely events.

## 3. Mutual Information
- I(X;Y) = H(X) - H(X|Y) = H(X) + H(Y) - H(X,Y)
- Nonnegative
- Channel capacity: C = max_{p(x)} I(X;Y)

Simple example: binary symmetric channel and noisy-channel intuition.

## 4. Error Detection/Correction Basics
- Hamming distance basics
- Minimum distance d_min bounds error detection and correction
- Intuitive use of redundancy without full coding-theory derivation

## Guided Examples
1. Compute entropy for Bernoulli(p)
2. Build a Huffman code for given probabilities
3. Show H(X,Y) ≤ H(X)+H(Y)
4. Compute mutual information for a small joint table

## Pitfalls
- Mixing base changes without clarification
- Claiming Huffman is optimal for all compression contexts
- Skipping nonnegativity and units when discussing bounds

## Exercises
1. Compute entropy for a fair die and for a biased die
2. For {A:1/2, B:1/4, C:1/8, D:1/8}, construct an optimal prefix code
3. Show H(X|Y) ≤ H(X)
4. Compute I(X;Y) for a given joint distribution