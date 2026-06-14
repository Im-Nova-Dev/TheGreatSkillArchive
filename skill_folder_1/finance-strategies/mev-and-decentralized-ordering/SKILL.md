---
title: MEV and Decentralized Ordering
description: >
  Use when the user works with Ethereum, L2, DeFi, mempool data, or
  transaction-ordering risk: Maximal Extractable Value mechanics, sandwich attacks,
  Flashbots/MEV-Boost bundles, encrypted mempools, searcher-builder-validator
  dynamics, cross-chain MEV, arbitrage bundles, fair sequencing services,
  mitigation tactics, and protocol-level defenses against ordering exploitation.
  Covers both CEX/CLOB-order-flow and AMM contexts and is centered on actionable
  concepts rather than commentary.
triggers:
  - MEV
  - Maximal Extractable Value
  - sandwich attack
  - front-running
  - Flashbots
  - MEV-Boost
  - transaction ordering
  - bundle
  - encrypted mempool
  - sequencer
  - mempool
  - searcher
  - back-running
  - AMM arbitrage
  - liquidation MEV
  - time-bandit attack
  - fair sequencing
---

# MEV and Transaction Ordering Risk

## 1. Purpose
This skill captures the mechanics, tactics, and defensive design for Maximal Extractable Value (MEV) — the value extracted by reordering, inserting, or censoring transactions — and analogous ordering risks in DeFi and L2 environments.

## 2. Core Mechanics

### 2.1 Block Production Pipeline (Ethereum Post-Merge)
- **Searchers** identify profitable reorderings from public/proprietary flow.
- **Builders** assemble blocks by aggregating searcher bundles and user txs, optimizing for MEV.
- **Relays** validate and distribute blocks to validators.
- **Validators (proposers)** select blocks via MEV-Boost or local building.
- MEV leakage to validators grows as relay market consolidates.

### 2.2 Categories of MEV
- **Arbitrage** — exploit price differences across AMM pools or CEXes.
- **Sandwich (front-running)** — front-run + back-run around a victim trade.
- **Liquidations** — race to call a borrowing position.
- **Time-bandit reorg** — reorganize chain to steal prior MEV.
- **Censorship** — OFAC or regulator-driven tx exclusion.

### 2.3 AMM Mechanics and Slippage
- **Uniswap V2 constant product**: `x * y = k`. Price impact `Δp ≈ 1 - exp(-v / (2L))` for liquidity L and swap size v.
- **Uniswap V3 concentrated liquidity**: liquidity over price ticks; larger swaps sweep anythin