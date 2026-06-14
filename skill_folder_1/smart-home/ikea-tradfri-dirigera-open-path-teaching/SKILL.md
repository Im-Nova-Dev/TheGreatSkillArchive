---
name: ikea-tradfri-dirigera-open-path-teaching
description: Teach IKEA Tradfri and Dirigera users how to leave IKEA's cloud and run smart lighting locally via Zigbee2MQTT or Home Assistant ZHA. Covers keeping bulbs, shedding cloud, and migrating scenes.
---

# IKEA Tradfri / Dirigera — Open-Path Teaching

## Why this path
Dirigera is more cloud-locked than Tradfri was. Many users already own IKEA bulbs and want local control without replacing them.

## Two paths
  1. Keep IKEA Gateway + bulbs: limited local, still requires IKEA app for setup.
  2. Pair bulbs to Zigbee2MQTT: true local; no IKEA app needed after pairing.

## Pairing IKEA TRÅDFRI bulb to Z2M
1. Turn bulb off and on rapidly to enter pairing mode.
2. Zigbee2MQTT Permit Join: ON.
3. Bulb joins; rename.
4. Remove from IKEA app if present.

## Caveats
- IKEA recycling mode firmware sometimes blocks re-pairing; factory reset via bulb on/off sequence.
- Blinds + remotes from IKEA often pair first to IKEA gateway; re-pair to Z2M when replacing gateway.

## Teaching script
"You already own the hardware. Let's free the software."

## Post-install
- [ ] All IKEA bulbs visible in Home Assistant.
- [ ] IKEA app removed or disabled.
- [ ] Scenes from Tradfri app rebuilt locally.
