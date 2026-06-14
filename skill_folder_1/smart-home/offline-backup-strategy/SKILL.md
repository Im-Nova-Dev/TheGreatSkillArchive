---
name: offline-backup-strategy
description: Teach designing a fully offline backup strategy for a local smart home including Home Assistant snapshots, Mosquitto persistence, ESPHome configs, MQTT retained state, coordinator recovery, and periodic restore drills.
---

# Offline Backup Strategy

## Layers
1. HA snapshots to local SMB/NFS share nightly.
2. Mosquitto persistence directory snapshot after broker stop.
3. ESPHome configs in local git repo, mirrored to second disk.
4. Zigbee2MQTT permit-join and database backups.

## Drill cadence
- Full cold restore quarterly.
- Knob test: swap coordinator, restore db, permit-join without factory reset.

## Teaching point
Cloud backup is optional insurance, not the source of truth.
