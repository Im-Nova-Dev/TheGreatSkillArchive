---
name: zigbee2mqtt-lighting-installation
description: Teach installing Zigbee2MQTT on Home Assistant, openHAB, or standalone as an open coordinator layer. Covers Sonoff ConBee II adapter, firmware flashing, device permitting, joining mode, network key rotation, and monitoring with MQTT Explorer.
---

# Zigbee2MQTT for Lighting — Installation Mastery

## Core concept
Zigbee2MQTT translates Zigbee radio traffic into MQTT messages. This removes proprietary hub lock-in (Hue, SmartThings) and exposes raw light control to any MQTT client.

## Supported coordinators
  - Sonoff Zigbee 3.0 USB Dongle Plus (P or E or 3.0): the budget leader.
  - ConBee II / ConBee 3: reliable, Linux-native, good range.
  - Nordic nRF52840 dongle: DIY path.
  - Always use a 10-15cm USB extension cable; Pi USB3 radio interferes with 2.4GHz Zigbee.

## Install path: Home Assistant add-on
1. SSH into HA or use Add-on Store.
2. Install Zigbee2MQTT add-on; configure serial port path (match dongle).
3. Start; check log for "Zigbee2MQTT started successfully" and coordinator firmware version.
4. Frontend: install Zigbee2MQTT Web UI add-on for permit join workflow.

## Pairing a bulb
1. Enable "Permit Join" in Zigbee2MQTT frontend.
2. Flip bulb power off/on 3-4 times if bulb has pairing mode.
3. Bulb appears in log; accept.
4. Rename in Zigbee2MQTT; map to Home Assistant light entity.

## Network key and security
- Zigbee2MQTT generates a random network key on first run. Back up this key for recovery.
- Rotate network key only if device is compromised.

## Troubleshooting
  Symptom                    | Cause                         | Fix
  ---------------------------|-------------------------------|------------------------------------
  Device not joining          | Invalid firmware on dongle     | Flash latest Z-Stack via flasher
  Lights lag                  | MQTT broker overload          | Move broker to same LAN segment
  Multi-bulb dropout          | Router DHCP conflict          | Use static IP for HA and dongle host

## Teaching drills
- Drill 1: apprentice identifies correct serial path on Linux host.
- Drill 2: bulb factory reset procedure timed; apprentice restores bulb to pairing mode.
- Drill 3: MQTT topic naming schema; apprentice maps `zigbee2mqtt/bulbid` to HA entity config.
