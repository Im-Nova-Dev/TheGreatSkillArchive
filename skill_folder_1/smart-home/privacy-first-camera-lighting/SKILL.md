---
name: privacy-first-camera-lighting
description: Teach using local camera feeds to trigger or adjust lighting policies, with motion regions, people detection via Frigate local model, and light activation without uploading frames to the cloud.
---

# Privacy-First Camera-Driven Lighting

## Stack
- Frigate or ZoneMinder on local server.
- Coral TPU optional for people detection.
- MQTT events for ONVIF/Persons sensor.

## Lighting wiring
```
Frigate detects person -> events: person_detected -> MQTT -> HA -> lights activate
```

## Privacy rules
- Motion clips stored on local disk or NFS only.
- No RTSP stream lease to cloud DVR.
- Mask private zones (windows into neighbor yards).

## Teaching exercise
Configure one porch camera to activate one outdoor light only during 22:00-05:00.
