---
name: execution-notification-workflows
description: >
  Teach designing execution notification and alert workflows for trading strategies and broker interactions.
  Covers event taxonomy, authorization policies, handler logic, template patterns, broker API constraints,
  and compliance-aware notification controls.
hero: false
---

# Execution Notification Workflows

Use this skill to design robust, compliant alert and notification systems
for trading strategy lifecycle events and broker interactions.

## 1. Authority and Compliance Guardrails

Before implementing any notification system, confirm authorization:

- Verify that notifications are internal or within explicitly authorized channels.
- Broker rules may restrict certain automated communications; check API terms of service.
- Some markets require pre-approval for strategy-level alerts to investors.
- Maintain audit logs of alert triggers and recipients.

If a notification workflow is prohibited or restricted, document that as a
negative constraint and provide alternatives (summary reports, delayed digests).

## 2. Event Taxonomy

Classify notification events by severity and actionability.

| Tier            | Examples                                        |
|-----------------|-------------------------------------------------|
| Informational   | Daily PnL summary, model health checks          |
| Attention       | Spread widening, latency spike, queue depth     |
| Action Required | Margin call, fill rejection, circuit breaker    |
| Urgent          | Execution failure, broker connectivity loss     |

## 3. Event Attachment Principles

Attach evidence, not emotions or unverified claims.

- Use structured payloads: timestamp, symbol, event type, context.
- Include quantifiable fields: price, size, slippage, latency bps.
- Route only inferred risks, not speculative predictions.

## 4. Handler Design

### Idempotency
- Deduplicate by event ID or composite key (strategy + symbol + slot).
- Record processed IDs for replay protection.

### Throttling
- Limit repeat alerts for persistent conditions (e.g., margin > threshold).
- Use state machines: WARN -> ALERT -> ESCALATE.

### Acknowledgment and Escalation
- Require acknowledgment for Tier 3+ events.
- Escalate after no-acknowledgment timeout to designated channels.

## 5. Template Patterns

### Strategy Health Report
```
[HEALTH] strategy=vix-scalp status=OK return=0.12% max_dd=0.45% 
execution_score=0.83 latency_avg_ms=12
```

### Execution Alert
```
[EXEC] order_id=abc123 symbol=SPY action=FILLED qty=500 
price=$502.14 slippage_bps=1.2 venue=ARCA ts=2026-06-05T14:31:22Z
```

### Broker Issue Warning
```
[BROKER] alert=BACKOFF_ORDER_REJECTED strategy=tsla-momos 
reason=COOLOFF_PERIOD <= Retry after 00:05:00 UTC
```

## 6. Broker-Centric Interaction Rules

### Rate Limits and Backoff
- Respect 429 responses; apply jittered exponential backoff.
- Centralize retry state to avoid duplicate order submissions.
- Detect order_stale or duplicate_id errors and halt replay.

### Order State Management
- Track order status transitions: pending -> accepted -> filled/rejected.
- Verify acknowledgments before updating position state.

### Connection and Heartbeat
- Implement heartbeats per session.
- On reconnect, reconcile open orders and pending alerts.

## 7. Design Patterns

### Fan-Out with Correlation
```
strategy_event
  -> execution_monitor (slippage, fill rate)
  -> risk_monitor (drawdown, margin)
  -> notification_hub (route by tier)
```

### Event Sourcing
- Store raw events and recompute alerts from log for backtests.

### Dead Letter Queue
- Capture failed notifications for manual review or replay.

## 8. Compliance and Audit

- Retain logs per regulatory requirements (varies by jurisdiction).
- Hash or redact PII where required.
- Define retention policy: 7 years typical for financial records.

## 9. Practical Implementation Checklist

- [ ] Documented authorization per channel and jurisdiction.
- [ ] Event taxonomy and tiering defined.
- [ ] Deduplication and idempotency guaranteed.
- [ ] Broker terms of service reviewed for automation restrictions.
- [ ] Rate limit and backoff configured.
- [ ] Order state reconciliation on reconnect.
- [ ] Audit log retention configured.

## 10. Teaching Exercises

### Exercise 1: Event Taxonomy
Design an event taxonomy for an intraday stat-arb strategy.

### Exercise 2: Retry Workflow
Implement an acknowledgment handler with exponential backoff.

### Exercise 3: Compliance Audit
Review a sample notification log for regulatory gaps.

### Exercise 4: Failure Drill
Simulate broker API failure and verify reconciliation workflow.

## 11. Common Pitfalls

- Over-notifying: alert fatigue masks real issues.
- Under-attaching: missing context increases MTTR.
- Blind replay: triggering duplicate orders on reconnect.
- Ignoring jurisdiction rules: broker may impose message limits.
- Soft vs hard authority: not documenting what is prohibited vs discouraged.
