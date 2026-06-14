---
name: local-security-and-alarm-lighting
description: Teach integrating offline security sensors with lighting actions including door-open alerts, perimeter presence rules, partial-arm and full-arm scenes, and local siren/light strobes without cloud alarm services.
---

# Local Security and Alarm Lighting

## Sensors
- Door/contact sensors Zigbee or Z-Wave.
- PIR + glass break via ESP32.
- Siren/strobe on relay or Zigbee siren device.

## States
- Disarmed: normal scenes.
- Home partial: perimeter lights + front porch alert.
- Away: all interior lights off + exterior full on + siren on breach.

## Teaching exercise
Create arm-state-aware lighting states tied to HA alarm panel.
