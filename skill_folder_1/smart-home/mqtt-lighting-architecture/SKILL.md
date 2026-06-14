---
name: mqtt-lighting-architecture
description: Teach MQTT broker setup and topic design for smart lighting including broker choice (Mosquitto vs EMQX), topic naming conventions, retain flags, QoS, authentication, and segmentation by user trust level.
---

# MQTT Architecture for Lighting

## Core concept
MQTT is the local bus for open-source lighting. Every light becomes an MQTT topic. Good naming prevents chaos.

## Topic schema
```
home/
  {location}/
    {device_type}/
      {instance}/
        set    -> write here to control
        state  -> read here for current state
        attr/  -> metadata
```

Example:
```
home/living_room/light/sofa_left/set
home/living_room/light/sofa_left/state
```

## Broker options
- Mosquitto: small footprint, easy config, good for beginner.
- EMQX: faster at scale; better for many Zigbee2MQTT/Z2M + WLED + ESPHome devices.

## QoS guidance
- Commands: QoS 1 at minimum. QoS 0 is okay for color previews.
- State: QoS 1 or 0 depending on reliability need.
- Retain: ON for state so dashboards show true state after restart.

## Security baseline
- Disable anonymous access.
- Require username/password for every client.
- Segment: `home/` vs `guest/` topics; restrict write access to admin apps.
