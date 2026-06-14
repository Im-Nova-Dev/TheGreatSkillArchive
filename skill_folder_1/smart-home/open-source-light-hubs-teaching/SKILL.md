---
name: open-source-light-hubs-teaching
description: Teach Home Assistant, openHAB, Zigbee2MQTT, and Mosquitto as local-first lighting controllers. Covers install paths, hardware requirements, privacy tradeoffs, and how to explain local vs cloud control to beginners.
---

# Open-Source Lighting Hubs — Onboarding Teaching

## Core message
The hub does not need to be Phililps Hue, Lutron, or a cloud subscription. Open-source hubs run on any Linux box and bring your lights home.

## Hub options at a glance
  - Home Assistant: highest community support; built-in Zigbee/Thread add-ons; easiest local UI.
  - openHAB: older, mature, steeper curve; stronger enterprise/commercial rules.
  - Zigbee2MQTT + Mosquitto MQTT broker: dedicated Zigbee gateway; pairs with Home Assistant, openHAB, or Node-RED.
  - OwnTracks / custom: advanced; not recommended for lighting beginners.

## Hardware paths
  - Raspberry Pi 4/5: Home Assistant OS; runs Zigbee2MQTT add-on with Sonoff dongle.
  - Intel NUC / mini PC: Home Assistant Container (Docker) or Full install; quieter, faster.
  - Existing NAS: Synology, Unraid; run VM or Docker.
  - ESP32 standalone: minimal Zigbee gateway; great as secondary.

## Why users care about local
  - Privacy: raw telemetry stays on LAN.
  - Uptime: automations run during ISP outage.
  - Speed: Zigbee to device in <50ms vs cloud round-trip 200-1200ms.
  - Cost: after hardware purchase, no subscription.

## First-install teaching sequence
1. Flash coordinator firmware if needed (Sonoff dongle with Z-Stack fw).
2. Install HA OS on Pi; connect to router by Ethernet.
3. Add Zigbee2MQTT add-on; pair first device (bulb or sensor).
4. Create simple automation; verify it runs during active WAN disconnect test.

## Post-install
- [ ] Hub reachable on LAN only if desired.
- [ ] Backup snapshot on local NAS or USB.
- [ ] User knows how to rollback to previous snapshot if update breaks Zigbee.
