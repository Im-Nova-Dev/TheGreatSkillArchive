---
name: multi-protocol-local-bridging
description: Teach bridging Zigbee, Z-Wave, Thread/Matter, and Wi-Fi devices into a unified offline control plane using MQTT translation, Z-Wave JS UI, Zigbee2MQTT, and Matter controller bridges without vendor clouds.
---

# Multi-Protocol Local Bridging

## Goal
One authoritative control surface across protocols.

## Map
```
Zigbee --> Zigbee2MQTT --> MQTT --> HA
Z-Wave --> Z-Wave JS UI --> MQTT --> HA
Thread --> Matter controller (HA/chip) --> HA
Wi-Fi --> ESPHome/Tasmota --> MQTT or HA native --> HA
```

## Rules
- Single source of truth per device; avoid duplicate entities.
- Use MQTT as common bus; HA consumes only from MQTT or native bindings.
- Prefer native HA Matter if Thread devices dominate.

## Teaching exercise
Add one Z-Wave dimmer + one Zigbee bulb to same room scene.
