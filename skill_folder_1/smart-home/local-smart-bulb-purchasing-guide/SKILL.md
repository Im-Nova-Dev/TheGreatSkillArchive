---
name: local-smart-bulb-purchasing-guide
description: Teach how to buy smart bulbs that remain local and open. Covers open-protocol bulbs (Zigbee, Thread/Matter without cloud), pre-flashed ESP bulbs like KAUF, brands to avoid, and the litmus test for cloud lock-in.
---

# Buying Bulbs That Stay Local — User Guide

## The litmus test
If the bulb requires app login or phone location to work, it is cloud-dependent.

## Preferred choice categories
  1. Zigbee + open coordinator: Philips Hue (paired to Z2M), Gledopto, IKEA TRÅDFRI (paired to Z2M/ZHA).
  2. Thread/Matter via local controller: Nanoleaf Essentials, Eve, Aqara T2, Hue Thread-capable bulbs.
  3. Pre-flashed ESP bulbs: KAUF A21 with ESPHome (no cloud).
  4. Wi-Fi open firmware: pre-Tuya bulbs flashing Tasmota/ESPHome.

## Purchase guards
- Check Zigbee cluster library compatibility if not using Z2M.
- Avoid bulbs through "account needed" in manufacturer app first; pair via open coordinator and test.

## Vendors to approach carefully
- LIFX: great local API but cloud features activated first.
- WiZ: app-centric; some APIs undocumented.
- Wyze: Wi-Fi; community reverse-engineering required.

## Conversations with sales staff
Ask these exact questions:
1. "Does this work without internet?"
2. "Is there an open API?"
3. "Can I pair it to Zigbee2MQTT or Matter controller?"

## Teaching outcome
User leaves with 3 approved bulb SKUs and a reason why others were ruled out.
