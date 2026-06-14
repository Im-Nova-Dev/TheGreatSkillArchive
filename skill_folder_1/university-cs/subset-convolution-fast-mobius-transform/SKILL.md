---
title: "Fast Subset Convolution via Möbius and Zeta Transforms"
description: "Teach subset convolution, fast zeta transform, fast Möbius transform, and inclusion–exclusion style DP on the Boolean lattice. Includes algorithmic analysis, proof ideas, exercises, and connections to arithmetic-function transforms and FFT-like speedups."
category: "university-cs"
triggers:
  - subset convolution
  - Möbius transform
  - zeta transform
  - SOS DP
  - inclusion-exclusion algorithm
  - subset sum convolution
  - subset lattice
---

# Fast Subset Convolution via Möbius and Zeta Transforms

Use this skill when explaining how to convolve/combine functions over subsets of an n-element set in O(n^2 2^n), how Möbius inversion upgrades naive subset DP, and when students confuse inclusion–exclusion with zeta/Möbius transforms.

## 1) The Boolean lattice viewpoint
Treat the family P([n]) of subsets of {1,…,n} ordered by inclusion. Many DP/counting formulas ask for:
h(S) = Σ_{T⊆S} f(T)·g(S\\T) .
That is a *subset convolution* of f and g. Doing this for all S costs Θ(n·3^n) by the obvious recurrence. Fast subset convolution drops this to Θ(n^2 2^n).

## 2) Zeta and Möbius transforms on subsets
Define pointwise multiplication with shifted versions over subsets. For functions on subsets:
- Upward zeta (or downward depending on convention): \hat{f}(S) = Σ_{T⊆S} f(T).
- Möbius inversion is its inverse: f(S) = Σ_{T⊆S} (−1)^{|S\\T|} \hat{f}(T).
These are the set-theoretic analogs of Dirichlet convolution inversion, but here the underlying poset is the Boolean lattice. The transforms are invertible because the incidence matrix of subsets is triangular with ±1 on the diagonal.

## 3) Fast transforms: SOS DP
Compute the upward zeta for all S in O(n·2^n) by “sum-over-subsets” DP:
for i in 0..n-1:
  for S in 0..(1<<n)-1:
    if S has bit i set: dp[S] += dp[S ^ (1<<i)]
This iterates over supersets; the Möbius transform is the same loop with subtraction:
    if S has bit i set: dp[S] -= dp[S ^ (1<<i)]
These are exactly the subset-variant of the fast Walsh–Hadamard transform on the hypercube.

## 4) Fast subset convolution proof idea
Write f and g as arrays on subsets. For each subset S split by a distinguished element k = |S|, or equivalently by rank. Then
(f ∗ g)(S) = Σ_{T⊆S} f(T)·g(S\\T)
= Σ_{k=0}^{|S|} Σ_{T⊆S, |T|=k} f(T)·g(S\\T).
Precompute rank-partitioned transforms: for each k, let f_k(S) be f(S) if |S|=k, else 0. Then compute zeta transforms of all f_k and g_k. Convolution per rank uses pointwise products followed by inverse zeta. Combining ranks and summing over k yields the full convolution in O(n^2 2^n). The bookkeeping among {0,…,n} ranks is what raises the exponent from trivial O(n·2^n) up to O(n^2 2^n), matching the naive bound but with a much smaller constant and clean structure.

## 5) Intuition: why transforms help
The Boolean lattice is a graded poset. The zeta transform is convolution with the constant-1 function under the subset convolution monoid; the Möbius function μ(S,T)=(-1)^{|S|-|T|} is its inverse. Turning inclusion constraints into coefficient operations converts combinatorial sums into vector convolutions, exactly as generating functions do for ordinary integers, but in n dimensions corresponding to the n chain elements.

## 6) Algorithmic connections and applications
- Counting independent sets, vertex covers, or colorings via inclusion–exclusion DP.
- Covering DP: Σ_{T⊇S} instead of Σ_{T⊆S} by swapping roles.
- AND/OR/GCD convolutions use analogous transforms on divisor lattices.
- Parameterized complexity: inclusion–exclusion FPT algorithms for {p,q}-dominating sets, Steiner tree.
- Reductions: if you can compute subset convolution in O(2^n poly(n)), you can evaluate any inclusion–exclusion sum over subsets with the same cost.

## 7) Worked example
Let n=3, f(S)=1 if |S| odd else 0, g(S)=|S|.
Direct: h(S)=Σ_{T⊆S} f(T)g(S\\T).
For S={1,2,3}: subsets T split into odd-sized T giving g(S\\T) = |S|-|T|.
Compute by rank: k=1 term contributes C(3,1)·1·2, k=3 term contributes 1·1·0 => h=6+0=6.
Doing this for all 8 subsets illustrates rank summation and confirms the transform machinery.

## 8) Exercises
1. Write O(n·2^n) SOS DP for up/down transforms; test inversion by applying forward and backward passes.
2. Prove μ(S,T)=(-1)^{|S|-|T|} is the inverse of the zeta function on the Boolean lattice.
3. Implement fast subset convolution for n=20 and benchmark against the Θ(n·3^n) recurrence.
4. Derive the AND-convolution analog on subsets where T∩S appears instead of T⊆S.
5. Suppose f(S)=1. Compute \hat{f}(S)=2^{|S|} and verify by counting supersets.

## 9) Further Reading
- Björklund, Husfeldt, and Koivisto, “Fourier meets Möbius: fast subset convolution” (2009).
- Codeforces tutorial: “Tutorial on Zeta Transform, Mobius Transform and Subset Sum Convolution”.