---
name: local-presence-detection
description: Teach offline presence detection using ESP32 BLE, Zigbee=device occupancy, mmWave, Wi-Fi associated-device lists, and GPS fence via local MQTT — avoiding cloud geofencing.
---

# Local Presence Detection

## Problem
Cloud geofencing and phone tracking leak location history.

## Local methods ranked
1. Zigbee PIR + mmWave for room presence.
2. BLE advertisement sniffing from ESP32 fixed sensors.
3. Wi-Fi AP client list (MAC addresses tied to device owners).
4. Door/contact sensors infer room transitions.

## Privacy notes
- Do not fingerprint phones by MAC randomization.
- Prefer per-room occupancy over per-person tracking unless explicitly desired.

## Example wiring
```
Bedroom PIR --> Z2M --> topic: zigbee2mqtt/bedroom_pir --> HA binary_sensor
ESP32 BLE beacon -> mqtt json -> homeassistant sensor
mmWave radar -> GPIO ESP32 -> ADC -> mqtt -> HA distance sensor
```

## Teaching exercise
Apprentice designs bedroom + bathroom presence trigger to avoid lights staying on when empty.
