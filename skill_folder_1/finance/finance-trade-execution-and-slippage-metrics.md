---
title: Trade Execution & Slippage Metrics
description: Teach finance trade execution and slippage metrics including effective spread, implementation shortfall, venue routing score, and reproducible benchmarking archetypes. Use for execution quality review, order routing, and quantifying trading costs.
tags: [finance, execution, slippage, liquidity, routing]
metadata:
  author: hermes scheduled
  version: 1.0
---

# Finance: Trade Execution & Slippage Metrics

## Core Concepts

### 1. Effective Spread
```python
mid_t = (best_bid_t + best_ask_t) / 2
filled_t = execution_price_at_t
effective_spread_t = abs(filled_t - mid_t) / mid_t
```
- Prefer over quoted spread because it captures routing and queue departure cost.

### 2. Implementation Shortfall
```python
decision_mid = mid_price_at_decision_time
net_shortfall = (decision_mid - avg_execution_price) / decision_mid
```
- Decompose net_shortfall into delay, impact, and spread components.
- Use per-slice gates to limit any single cost driver above threshold.

## Reproducible Archetype: Execution Quality Logger

```python
import pandas as pd
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExecutionRecord:
    ts: pd.Timestamp
    symbol: str
    venue: str
    decision_mid: float
    best_bid: float
    best_ask: float
    avg_exec_price: float
    qty: float
    fee: float = 0.0

    def effective_spread(self):
        mid = (self.best_bid + self.best_ask) / 2
        return abs(self.avg_exec_price - mid) / mid

    def is_signed(self):
        mid = (self.best_bid + self.best_ask) / 2
        signed = (self.avg_exec_price - mid) / mid
        return -signed if self.qty > 0 else signed

# Append rows to rolling parquet
records = []
records.append(ExecutionRecord(...).__dict__)
pd.DataFrame(records).to_parquet("execution_records.parquet", append=True)
```

## Reproducible Archetype: Venue Routing Score

```python
def venue_score(venue_stats: pd.DataFrame,
                w_spread=0.4, w_is=0.4, w_risk=0.2) -> pd.Series:
    """
    Higher score = better routing target.
    venue_stats must include: effective_spread, implementation_shortfall, spread_jitter, hidden_share.
    """
    spread_score = 1 / (1 + w_spread * venue_stats["effective_spread"])
    is_score = 1 / (1 + w_is * venue_stats["implementation_shortfall"].clip(lower=0))
    risk_score = 1 / (1 + w_risk * venue_stats["spread_jitter"])
    return spread_score + is_score + risk_score - 0.5 * venue_stats["hidden_share"]
```

## Repro Steps
1. Capture execution fills with venue and order metadata.
2. Derive effective spread and implementation shortfall per fill.
3. Compute venue routing score hourly.
4. Replay fills against prior routing score to estimate missed opportunity.

## Verification
- Correlation between routing score and realized slippage ≥ 0.45 after 4 weeks.
- Effective spread reduction ≥ 8% versus first-come-first-served routing.
- Fill rate change relative to market order baseline tracked separately.
