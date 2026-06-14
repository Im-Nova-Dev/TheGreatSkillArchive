---
name: shelly-relay-lighting-installation
description: Teach installing Shelly relays and dimmer modules for local Wi-Fi / MQTT lighting control. Covers behind-switch mounting, Shelly Plus 1 / Plus 2PM / Dimmer 2, Calibrating dimmer curve, and failover.
---

# Shelly Local Relay Installation

## Core positioning
Shelly exposes local HTTP, WebSocket, and MQTT APIs with no cloud required. It is the closest mainstream product to "open local" that ships ready-to-use.

## Models for lighting
  - Shelly Plus 1: single channel on/off.
  - Shelly Plus 2PM: dual channel with power metering.
  - Shelly Dimmer 2: trailing-edge dimmable LED with 0-100% smooth range.
  - Shelly Vintage: behind E27 socket; retrofit lamps.

## Installation
1. Turn off breaker; verify.
2. Mount behind switch; wire line, load, optional neutral.
3. Restore power; Wi-Fi AP mode starts.
4. Join `Shelly-xxxxxx` Wi-Fi; provide home SSID/password.
5. Shelly app optional; assign static IP via router DHCP.
6. Disable "Shelly Cloud" to remain fully local.

## Calibrating dimmer
- In Shelly web UI, run dimmer calibration to learn min/max for attached LED load.
- Store curve.

## Failure mode coverage
- Wi-Fi outage: local API drops, but relay holds last state or fails safely per switch config.
- Router restart: Shelly reconnects automatically.
