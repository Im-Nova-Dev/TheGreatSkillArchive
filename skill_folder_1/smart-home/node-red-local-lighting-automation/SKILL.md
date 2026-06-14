---
name: node-red-local-lighting-automation
description: Teach Node-RED flow design for local lighting control using MQTT, Zigbee2MQTT, ESPHome, and Home Assistant events. Covers drag-and-drop teaching, debugging flows, and migrating cloud automations to local.
---

# Node-RED Local Lighting Automation

## Core concept
Node-RED is a visual flow editor on Node.js that connects events to actions. All logic runs locally in Docker or on the host.

## Core nodes
  - `mqtt in` / `mqtt out`: talk to broker.
  - `events: state` (Home Assistant): sensor/light state changes.
  - `trigger`: schedules, delays, rate limit.
  - `change`: transform and route.
  - `call service`: trigger scenes or set light attributes.

## Example flow
  Zigbee2MQTT motion -> delay 60s -> expect no motion -> set light off unless lux > 30
  All runs on hub; no internet.

## Teaching
Use 3 flows:
  1. Motion -> porch light.
  2. Sunset -> ambient strip.
  3. Manual button -> goodnight scene.

## Resilience
- Node-RED failures do not stop Zigbee devices; they fall back to direct apps.
- Flows exportable as JSON; treat as config backup.
