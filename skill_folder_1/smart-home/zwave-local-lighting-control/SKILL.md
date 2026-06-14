---
name: zwave-local-lighting-control
description: Teach controlling Z-Wave lights and relays fully offline with Z-Wave JS UI, pairing strategies, and interoperability with Zigbee2MQTT and Home Assistant without cloud bridges.
---

# Z-Wave Local Lighting Control

## Why Z-Wave still matters
- Mature dimmer support, especially in-wall switches.
- Less Wi-Fi congestion than Zigbee in dense environments.
- Good for retrofit where Zigbee adoption is lower.

## Hardware
- Z-Wave dongle: Zooz 800 S2 or Nortek HUSBZB-1.
- Preferred devices: Inovelli, Zooz, Aeotec dimmers.

## Stack
```
Z-Wave device <--Z-Wave--> Dongle <--USB--> Z-Wave JS UI
  -> MQTT (optional binding)
  -> Home Assistant native Z-Wave JS integration
```

## Pairing
- Include device within arm’s reach of dongle.
- For wall switches, use "inclusion mode" at hub; then press device 3x.

## Teaching point
- Z-Wave range is ~30m line-of-sight; mesh repeats through powered devices.
- Repeater list viewable in Z-Wave JS UI; plan mesh before install.
