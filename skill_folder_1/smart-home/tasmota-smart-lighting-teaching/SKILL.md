---
name: tasmota-smart-lighting-teaching
description: Teach Tasmota as an open-source firmware alternative for Wi-Fi bulbs, plugs, and relays. Covers flashing flow, console commands for lights, MQTT topics, and comparison to ESPHome.
---

# Tasmota Smart Lighting Teaching

## Core concept
Tasmota is an open-source firmware for ESP8266/ESP32 that replaces cloud Tuya firmware with local MQTT/HTTP control.

##灯具/flash methods
- Tuya Convert OTA exploit: legacy, less reliable.
- Serial flash: USB-UART; most trusted.
- Pre-flashed KAUF-type bulbs: buy already running Tasmota.

## Console commands for lights
- `Power1 ON`
- `Dimmer 50`
- `Color 40FF9A` (HSB)
- `White 255`

## Local integration
- MQTT topics: `tele/<topic>/STATE`, `cmnd/<topic>/POWER`.
- Home Assistant MQTT Light platform.

## ESPHome vs Tasmota
- Tasmota: simpler for off-the-shelf bulbs, faster initial setup.
- ESPHome: easier YAML, Home-Assistant-centric OTA, more GPIO freedom.

## Teaching
Teach both. Many users want "just local" and Tasmota delivers that with less compile friction.
