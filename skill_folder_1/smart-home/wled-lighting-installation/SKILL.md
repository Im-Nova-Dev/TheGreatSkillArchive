---
name: wled-lighting-installation
description: Teach installing WLED, the open-source LED controller firmware, on ESP32 boards for local control of strips, panels, and matrices. Covers compile vs pre-built binaries, LED types, power injection, and Home Assistant integration without cloud.
---

# WLED — Open Lighting Firmware for Strips and More

## Core concept
WLED runs on ESP32 to control addressable LEDs (WS2812B, SK6812, etc.) entirely locally. It is the open-source rival to proprietary controllers like those bundled with Govee strips.

## Hardware
  - ESP32 dev board with 5V output or external power supply.
  - Logic-level MOSFET if using non-addressable strips.
  - 5V 10A PSU for 5m RGBIC at full brightness.
  - Level shifter if LED data line needs 3.3V -> 5V logic (recommended).

## Install paths
1. Pre-built binary: flash via esptool from WLED releases.
2. Compile: PlatformIO build for custom pinout.
3. USB install: WLED Installer finds ESP32 and flashes.
4. OTA update: enable in WLED Settings; supersedes USB.

## Power considerations
- Max per output: ESP32 GPIO ~40mA; use only as signal line.
- Shared ground: PSU ground to ESP32 ground is mandatory.
- Power injection: every 5m for 5V strips.

## Local control surfaces
- WLED UI on http://wled.local
- Home Assistant integration: native WLED integration or MQTT.
- MQTT topics: `wled/+/api`, `wled/+/lp` for live preview.

## Why this beats cloud strips
- No app required.
- Effect design runs locally.
- MQTT API fully documented.
