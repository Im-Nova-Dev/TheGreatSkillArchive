# Attribution SQL Patterns

Hourly rollup queries for ClickHouse and TimescaleDB.

## ClickHouse: Hourly Attribution Rollup

```sql
-- Direct cost per (model, tenant, workflow) per hour
CREATE MATERIALIZED VIEW IF NOT EXISTS attribution_hourly_direct
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, model_id, tenant_id, workflow_id)
AS SELECT
    toStartOfHour(timestamp) AS hour,
    model_id,
    tenant_id,
    workflow_id,
    sum(prompt_tokens) AS prompt_tokens,
    sum(completion_tokens) AS completion_tokens,
    sum(cached_tokens) AS cached_tokens,
    sum(gpu_ms) AS gpu_ms,
    count() AS request_count,
    sum(egress_bytes) AS egress_bytes
FROM inference_events
GROUP BY hour, model_id, tenant_id, workflow_id;
```

## ClickHouse: Shared Cost Allocation

```sql
-- Total shared infra cost per hour (GPU fleet, networking, storage)
CREATE TABLE IF NOT EXISTS infra_hourly_cost (
    hour DateTime,
    gpu_fleet_cost_usd Float64,
    networking_cost_usd Float64,
    storage_cost_usd Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY hour;

-- Proportional allocation key: each (model,tenant,workflow)'s share of total gpu_ms
WITH
    total_gpu_ms AS (
        SELECT hour, sum(gpu_ms) AS total_ms
        FROM attribution_hourly_direct
        GROUP BY hour
    ),
    allocation AS (
        SELECT
            d.hour,
            d.model_id,
            d.tenant_id,
            d.workflow_id,
            d.gpu_ms / t.total_ms AS alloc_share
        FROM attribution_hourly_direct d
        JOIN total_gpu_ms t ON d.hour = t.hour
    )
SELECT
    a.hour,
    a.model_id,
    a.tenant_id,
    a.workflow_id,
    -- Direct token costs
    a.prompt_tokens / 1e6 * 2.50 AS input_cost_usd,
    a.completion_tokens / 1e6 * 10.00 AS output_cost_usd,
    a.cached_tokens / 1e6 * 0.50 AS cached_cost_usd,
    -- Shared GPU allocation
    c.gpu_fleet_cost_usd * a.alloc_share AS gpu_shared_cost_usd,
    c.networking_cost_usd * a.alloc_share AS net_shared_cost_usd,
    c.storage_cost_usd * a.alloc_share AS storage_shared_cost_usd
FROM allocation a
JOIN infra_hourly_cost c ON a.hour = c.hour;
```

## TimescaleDB: Continuous Aggregate

```sql
-- Hypertable for raw events
CREATE TABLE inference_events (
    time        TIMESTAMPTZ       NOT NULL,
    model_id    TEXT              NOT NULL,
    tenant_id   TEXT              NOT NULL,
    workflow_id TEXT              NOT NULL,
    prompt_tokens     BIGINT      DEFAULT 0,
    completion_tokens BIGINT      DEFAULT 0,
    cached_tokens     BIGINT      DEFAULT 0,
    gpu_ms      BIGINT            DEFAULT 0,
    egress_bytes BIGINT           DEFAULT 0
);
SELECT create_hypertable('inference_events', 'time', chunk_time_interval => INTERVAL '1 day');

-- Continuous aggregate for hourly direct costs
CREATE MATERIALIZED VIEW attribution_hourly_direct
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS hour,
    model_id,
    tenant_id,
    workflow_id,
    SUM(prompt_tokens) AS prompt_tokens,
    SUM(completion_tokens) AS completion_tokens,
    SUM(cached_tokens) AS cached_tokens,
    SUM(gpu_ms) AS gpu_ms,
    COUNT(*) AS request_count,
    SUM(egress_bytes) AS egress_bytes
FROM inference_events
GROUP BY hour, model_id, tenant_id, workflow_id;

-- Add real-time view for recent data
CREATE MATERIALIZED VIEW attribution_hourly_direct_realtime
WITH (timescaledb.continuous, timescaledb.materialized_only = false) AS
SELECT * FROM attribution_hourly_direct;
```