---
name: zigbee-mqtt-network-resilience
description: Teach Zigbee + MQTT mesh resilience for reliable lighting networks. Covers routing vs end devices, adding router-capable plugs/bulbs, parent-change recovery, and interpreting Zigbee2MQTT network maps.
---

# Zigbee Network Resilience for Lighting

## Power law
A Zigbee network with only bulbs as routers will be flaky. One bad bulb takes down downstream nodes.

## Router vs end device
- Router: always powered, repeats traffic (wall plugs, mains bulbs).
- End device: battery (motion sensors) or sleepy (some bulbs broadcasting only when changed).
- Lighting rule: any ceiling or plug-in device should be router-capable whenever possible.

## Recovery behaviors
- Parent change: battery device re-pairs to nearest router automatically.
- Failed parent: device busy blinks or reports LQI 0.
- Z2M network map: inspect graph; orphan nodes need closer router.

## Shopping rule
When expanding Zigbee lighting, add one mains router per 8-10 end devices.
