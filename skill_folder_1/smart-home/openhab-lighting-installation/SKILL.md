---
name: openhab-lighting-installation
description: Teach installing OpenHAB as an open-source local smart lighting controller. Covers install paths (Linux, Docker, Windows), Things/Channels/Items model, Zigbee/Z-Wave binding setup, Paper UI vs files-based config, and migration from cloud hubs.
---

# openHAB Lighting Installation Teaching

## Why openHAB
- Mature Java-based automation platform.
- Strong vendor-agnostic binding model for Zigbee, Z-Wave, KNX, Modbus, etc.
- Steeper learning curve than Home Assistant, but powerful rule engine.

## Installation paths
  - Linux: apt repository install or manual `.deb`.
  - Docker Compose: recommended for repeatability.
  - Windows: not recommended, but possible with WSL2.

## Lighting modeling
  - Thing = physical device.
  - Channel = capability (on/off, brightness, color).
  - Item = exposed property to UI/rules.
Map every light as:
- Switch Item (on/off)
- Dimmer Item (brightness)
- Color Item (hue/saturation)
- Separate white temperature channel if CCT.

## Zigbee binding
1. Install Zigbee binding from Add-ons/Marketplace.
2. Pair coordinator via serial thing.
3. Include bulb via permit join at thing level.

## Migrating from closed hub
- Export scenes from cloud app.
- Recreate scenes in openHAB rules DSL or Blockly.
- Test in parallel before retiring closed hub.

## Teaching emphasis
openHAB teaches models over clicks; users need conceptual grounding before UI tasks.
