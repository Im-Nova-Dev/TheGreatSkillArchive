---
name: local-doorbell-and-entry-lighting
description: Teach wiring doorbell and entry events into a local lighting stack using MQTT door sensors, ESP32 doorbell buttons, local notification chains, and occupancy-aware entry scenes without cloud services.
---

# Local Doorbell and Entry Lighting

## Hardware
- ESP32 or Shelly doorbell relay for wired chime.
- Zigbee + Z2M for separate door sensor.
- PoE or USB speaker for local doorbell tone.

## Flow
```
Door button press -> ESP32 -> MQTT bell event
  -> HA: front porch light + hallway warm
  -> local TTS: someone at the door
```

## Privacy
- No capture of doorbell video upload.
- If camera used, store only in local Frigate.

## Teaching exercise
Wire doorbell to light front porch for 90 seconds and play local wav.
