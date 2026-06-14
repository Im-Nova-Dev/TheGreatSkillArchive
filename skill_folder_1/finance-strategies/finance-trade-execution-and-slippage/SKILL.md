---
name: finance-trade-execution-and-slippage
description: Finance trade execution, slippage tolerance, adverse selection, fill rates, and order routing. Use when planning trade execution, reviewing strategy robustness, understanding spread and execution cost, or teaching execution micro-skills.
---

# Trade Execution, Slippage, and Order Routing

Teach execution-side trading concepts with actionable practice: slippage tolerance as a risk parameter, fill-rate vs tolerance trade-offs, adverse selection, and liquidity diagnostics.

## Core Concept
Slippage tolerance is not only UI tolerance: it is a structural decision that gates order acceptance on expected execution quality.

## Lessons
1. Slippage as a risk parameter, not a convenience slider.
2. Fill rate and expected cost as coupled metrics.
3. Adverse selection detection from execution quality.
4. Measuring execution: effective spread vs quoted spread.
5. Order routing implications for fragmentation.

## Before the run
- Define one execution hypothesis to test.
- Identify venue or instrument with observable fills.

## During the run
- Record expected price, executed price, time to fill, and tolerance used.
- Tag by liquidity regime if available.

## After the run
- Calculate realized slippage, rejection rate, and effective spread.
- If rejections increase with no fill improvement, tolerance is likely too tight for conditions.
- If costs rise with fill rate improvements, admission of adverse selection into strategy edge.

## Pitfalls
- Measuring success by fill rate alone ignores realized cost.
- Treating tolerance as constant ignores volatility and depth changes.

## Output
- One execution insight in `/home/nova/.hermes/intel/finance/`.
- One updated teaching note or new example.
