---
name: home-assistant-backup-light-stack
description: Teach Home Assistant snapshot and restore best practices for lighting stacks. Covers Samba/NAS target, what to back up vs ignore, validating restores, and protecting against hub/bridge migrations.
---

# Home Assistant Lighting Backup Strategy

## What to back up
- HA snapshots: full config + entities.
- Zigbee2MQTT database and config.
- Mosquitto broker config and secrets.

## What NOT to back up
- Zigbee2MQTT coordinator backup only if you intend to reuse *same* dongle; otherwise hard-pair new coordinator.
- Gigabytes of history/pruning logs.

## Snapshot cadence
- Pre-update snapshot.
- Weekly recurring.
- Post-migration snapshot.
- Keep last 3; prune older.

## Restore drill
1. Clean install HA OS.
2. Upload latest snapshot.
3. Re-add Zigbee coordinator (same dongle = same network key recoverable).
4. Reboot and validate 5 random light entities.

## Teaching metric
User completes restore in under 20 minutes without calling support.
