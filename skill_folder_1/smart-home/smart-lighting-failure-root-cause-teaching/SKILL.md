---
name: smart-lighting-failure-root-cause-teaching
description: Teach root-cause analysis for lighting failures using proven problem-solving patterns borrowed from non-software domains. Covers electrical tracing, Zigbee/Thread mesh debugging, and how non-technical users describe problems differently from technicians.
---

# Root Cause Analysis for Smart Lighting Failures

## Why traditional debugging mindset breaks down in lighting
Users say “it’s not working” and mean any of:
- bulb dark,
- bulb wrong color,
- app says offline,
- switch “does nothing,”
- automation fires at wrong time.

## Five-whys adapted for lighting
1. Symptom: Lights off
2. Why? Wall switch off
3. Why? User expects smart switch = smart bulb
4. Why? Instructions skipped
5. Why? Installer did not set household policy

## Signal vs noise in reports
“Slow” = Wi-Fi congestion, not hub weakness.
“Random off” = motion timeout without override.
“Color wrong” = model mismatch, not bulb defect.

## Diagnostic order of operations
1. Power state.
2. Hub health.
3. Network strength.
4. Device pairing.
5. Last resort: factory reset.

## Teaching objective
Translate non-technical complaints into technician-level hypotheses without jargon shaming the user.
