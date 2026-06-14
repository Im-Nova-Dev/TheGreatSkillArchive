---
name: offline-disaster-recovery-drills
description: Teach periodic full offline recovery drills for local home systems, covering power loss, disk corruption, coordinator swap, hub restore, and proof that lighting automation survives zero WAN.
---

# Offline Disaster Recovery Drills

## Drills
1. Power kill + UPS reboot: restart ordering, auto-start containers.
2. Disk failure: recreate SSD, restore HA + MQTT + configs.
3. Coordinator replacement: new dongle, restore Zigbee2MQTT db, permit-join.
4. Full wipe test from scratch and restore snapshots.

## Pass criteria
- Every automation from checklist online within timeout.
- No factory resets of end devices.
- Documentation and configs recover from local repo.

## Teaching exercise
Run coordinator swap drill and measure downtime in minutes.
