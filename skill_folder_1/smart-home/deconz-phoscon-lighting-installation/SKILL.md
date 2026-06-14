---
name: deconz-phoscon-lighting-installation
description: Teach using DeCONZ + Phoscon as an open-source Zigbee gateway stack, independent of Hue Bridge. Covers ConBee/ RaspBee hardware, Phoscon UI, REST API, local scene design, and migrating away from Hue cloud.
---

# DeCONZ / Phoscon — Open Zigbee Gateway Teaching

## Core concept
DeCONZ turns a ConBee or RaspBee dongle into a standalone Zigbee gateway. Phoscon is its web/phone UI. Both speak local REST/WebSocket and avoid Hue cloud.

## Hardware
  - ConBee II / ConBee 3 USB dongle.
  - RaspBee II (Pi HAT) on Raspberry Pi.
  - Raspberry Pi 4/5 running Debian.

## Install path
1. Install OS; add dongle with USB extension.
2. Install deconz package or use Home Assistant OS add-on if present.
3. Phoscon UI launches on http://host:8080.
4. Lights and sensors paired through Permit Join.

## Local API
- REST pushes: `PUT /api/<apikey>/lights/<id>/state`.
- WebSocket for push events.
- Phoscon scenes map to local presets; no internet required.

## Migration path from Hue
1. Pair existing Hue bulbs in DeCONZ.
2. Create identical scenes.
3. Point dashboards/bridges to Phoscon API.
4. Disable Hue Bridge.

## Teaching emphasis
Treat Phoscon as a local replacement for Hue app. Show REST endpoint in browser before introducing apps.
