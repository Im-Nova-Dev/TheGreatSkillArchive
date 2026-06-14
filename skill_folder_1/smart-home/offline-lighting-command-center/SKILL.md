---
name: offline-lighting-command-center
description: Teach setting up a truly offline-capable lighting command center inside Home Assistant or openHAB. Covers dashboard-only access, incident演练 when ISP fails, paper UI for guests, and local voice over SN.
---

# Offline Lighting Command Center Teaching

## Why "offline capable" is the correct expectation
Cloud-first devices become paperweights when ISP fails. Local stack does not.

## Local architecture
```
[Zigbee Coordinator] -- USB -- [HA/openHAB]
  |
  +-- Zigbee bulbs
  +-- Zigbee sensors
  +--ESP32 Arduino lights
```

## Command center types
1. Wall tablet: iPad/Mini PC mounted; dashboard loads on LAN.
2. Physical keypad: Lutron Caseta (local), Z-Wave scene controller.
3. Paper cheat sheet: 3 commands; keep for power failures.

## Outage test required
- Unplug WAN cable.
- Trigger motion, scene, voice.
- Expect 100% local functionality for Zigbee/Z-Wave devices.
- Wi-Fi-only devices (Tuya/Kasa) may fail; flag to user.

## Teaching drills
- Drill 1: simulate ISP outage; apprentice lists what breaks and what doesn't.
- Drill 2: rebuild Zigbee network after total wipe using backup network key.
- Drill 3: guest onboarding; apprentice runs through paper cheat sheet without technical terms.
