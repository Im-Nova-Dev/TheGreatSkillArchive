---
name: local-access-control-lighting
description: Teach using local access control events - RFID, NFC, keypad, Z-Wave lock - to trigger entryway and ambient lighting flows without cloud auth.
---

# Local Access Control + Lighting

## Stack
- RFID/NFC reader: ESP32 RC522 over MQTT.
- Z-Wave lock: Yale / Schlage via Z-Wave JS UI.
- Wired keypad or standalone NFC tags on doors.

## Scene flow
```
Valid RFID -> unlock -> entry foyer warm + stair lights
Invalid RFID -> porch red alert + local notification
Locked -> entryway dim only
```

## Teaching exercise
Add two NFC tag scenes: sleep mode and guest mode at bedroom door.
