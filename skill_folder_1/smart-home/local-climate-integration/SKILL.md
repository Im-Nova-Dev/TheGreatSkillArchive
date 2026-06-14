---
name: local-climate-integration
description: Teach integrating local HVAC, heat pumps, fans, and heater control with lighting for presence-aware comfort scenes, setback automation, and energy-aware scheduling all offline with Home Assistant and MQTT.
---

# Local Climate Integration

## Stack
- Zigbee/Z-Wave thermostats or ESPHome temp + relay control.
- HA climate entity + fan + switch.

## Scene rules
- Away: heat setback + lights off + eco scene.
- Bedtime: bedroom warm + HVAC 2F lower.
- Sunny room: lower setpoint.

## Teaching exercise
Build one rule adjusting room brightness and target temp based on occupancy and lux.
