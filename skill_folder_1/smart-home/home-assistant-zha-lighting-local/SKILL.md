---
name: home-assistant-zha-lighting-local
description: Teach Home Assistant ZHA (Zigbee Home Automation) as an integrated local Zigbee stack for lighting. Covers installing the ZHA integration, pairing bulbs, device registry, quirks, and replacing Hue Bridge entirely.
---

# Home Assistant ZHA — Local Zigbee Lighting

## Core concept
ZHA is a Zigbee stack built into Home Assistant. It replaces Hue Bridge, SmartThings, or Z2M if you want fewer moving parts.

## Hardware
- Sonoff Zigbee 3.0 USB Dongle Plus, ConBee II, or any Zigbee coordinator supported by bellows/zigpy.

## Install
1. HA Settings > Devices & Services > Add Integration > ZHA.
2. Select serial port for dongle.
3. In ZHA dashboard: Enable Join.
4. Bulb on/off sequence; accept device.
5. Assign to area; set entity name.

## Quirks and compatibility
- ZHA uses quirks to support broken/special-cased devices.
- Confirm your bulb model appears in known-good lists before buying.
- Some Zigbee devices require signed firmware.

## Replacement of Hue Bridge
- Pair Hue bulbs to ZHA directly; works without Hue Bridge.
- Risk: Hue firmware updates won't apply.

## Teaching objective
Show that a single HA box + USB dongle replaces Hue Bridge + cloud contract.
