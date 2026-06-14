---
name: open-source-lighting-migration-runbook
description: Teach migrating a closed vendor smart lighting system (Hue cloud, LIFX cloud, Govee app) to fully local open stack. Covers pre-migration audit, staging by room, rollback plan, and provider disengagement.
---

# Closed-to-Open Lighting Migration Runbook

## Phase 0: Audit
List every device, current hub, and whether it supports local protocol. Accept that a few vendor-only devices may need eventual replacement.

## Phase 1: New hub in parallel
Deploy Home Assistant + Zigbee coordinator. Do not retire old hub yet.

## Phase 2: Room-by-room
Pick one room. Pair all bulbs to Z2M or ZHA. Recreate scenes. Validate for 7 days.

## Phase 3: Cutover
- Reassign dashboards.
- Disable vendor app cloud sync.
- Set old hub to factory default and store for 30 days.

## Rollback
Keep old hub box on shelf with power adapter; if Z2M behaves oddly, user can re-pair individual bulbs to old hub within minutes.

## Anti-anchor rule
Do not migrate everything simultaneously. Single-room validation reduces chaos.
