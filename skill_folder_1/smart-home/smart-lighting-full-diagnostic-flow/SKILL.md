---
name: smart-lighting-full-diagnostic-flow
description: Teach a single unified troubleshooting tree that routes smart lighting failures from the most general symptom ("lights don't work") into the right sub-skill pathway.
---

# Unified Smart Lighting Diagnostic Flow

## Top-level triage
Symptom first → category decision → skill lookup.

## 1. Power issue (all variants)
Check: switch, fuse, breaker, plug.
Skill: smart-switches-installation, smart-plugs-installation

## 2. Single bulb won't light
Check: socket seated, socket type/voltage, dumb dimmer present.
Skill: smart-bulb-installation

## 3. Many bulbs won't light
Check: hub offline, Zigbee channel, bridge power.
Skill: smart-bridges-installation

## 4. Strip partial failure
Check: power injection, data connector, model ID.
Skill: smart-strip-lights-installation

## 5. Panel dropout
Check: USB power, daisy chain seating, Rhythm module fit.
Skill: smart-light-panels-installation

## 6. Outdoor light dead
Check: GFCI, transformer, cable burial, IP connector.
Skill: smart-outdoor-lighting-installation

## 7. Motion/automation misfire
Check: lux threshold, timeout value, heat source interference.
Skill: smart-motion-sensors-installation

## 8. App can't reach device
Check: Wi-Fi, Matter Thread border, firmware.
Skill: smart-bridges-installation, smart-apps-installation

## 9. Voice no-op
Check: device name collision, assistant cloud, skill linking.
Skill: smart-voice-assistants-installation
