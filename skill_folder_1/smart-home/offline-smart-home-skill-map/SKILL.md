---
name: offline-smart-home-skill-map
description: One-page decision map of all offline/local-first smart-home skills. Use this to quickly select the right teaching skill by goal, device type, or system layer. Acts as a curated index rather than adding new technical content.
---

# Offline Smart Home Skill Map

## How to use
Start with your goal, then follow the branch to the right skill.

## Goal: Build from scratch
- full-offline-home-system-setup — master 4-day install guide.

## Layer: Core platform
- open-source-light-hubs-teaching — hub software comparison.
- full-offline-home-system-setup — server + OS + containers.
- offline-backup-strategy — snapshot and restore cadence.

## Layer: Protocols
- zigbee2mqtt-lighting-installation — Zigbee to MQTT.
- zwave-local-lighting-control — Z-Wave dimmers and switches.
- matter-thread-lighting-local-control — Thread border router + Matter.
- mqtt-lighting-architecture — broker design and topics.
- multi-protocol-local-bridging — unify Zigbee, Z-Wave, Wi-Fi, Thread.

## Layer: Firmware and hardware
- esphome-smart-lighting-teaching — ESPHome config patterns.
- tasmota-smart-lighting-teaching — Tasmota migration and config.
- wled-lighting-installation — LED strips and matrices.
- shelly-relay-lighting-installation — stock local REST/MQTT relays.
- diy-smart-bulb-hardware-teaching — custom open-hardware builds.
- ikea-tradfri-dirigera-open-path-teaching — IKEA local path.
- tuya-convert-esphome-migration — closed Wi-Fi to open firmware.
- offline-firmware-management-lighting — pinned OTA and rollback.

## Layer: Hub integrations
- home-assistant-zha-lighting-local — HA Zigbee Home Automation path.
- openhab-lighting-installation — openHAB bindings overview.
- deconz-phoscon-lighting-installation — DeCONZ coordinator path.
- knx-lighting-local-installation — KNX wired local.
- node-red-local-lighting-automation — visual flow automation.
- privacy-first-camera-lighting — Frigate camera to light triggers.

## Layer: Networks and security
- cloud-audit-for-lighting-freedom — discover cloud calling home.
- iot-vlan-isolation-lighting — router and firewall structure.
- zigbee-mqtt-network-resilience — mesh stability and fallback.
- privacy-first-lighting-automation — data minimization rules.

## Layer: Inputs and sensors
- local-presence-detection — PIR, mmWave, BLE, Wi-Fi clients.
- airtag-free-local-presence — phone tracking without AirTags.
- local-energy-management — CT sensors and load shedding.
- local-traffic-and-environment-lighting — CO2, VOC, lux, noise.
- local-doorbell-and-entry-lighting — button and contact sensors.
- local-access-control-lighting — RFID/NFC/keypad triggers.
- offline-time-lighting-rituals — NTP/RTC time triggers.

## Layer: Outputs and notifications
- local-voice-lighting-commands — Piper/Vosk/Whisper offline pipeline.
- local-notification-system — TTS, MQTT alerts, e-ink panels.
- lan-only-lighting-dashboards — HA dashboard and tablet UI.
- local-media-sync-lighting — Jellyfin/Kodi/Snapcast to lights.
- audio-reactive-local-lighting — mic FFT to LED strips.

## Layer: Advanced and life events
- local-climate-integration — HVAC + lighting scenes.
- local-security-and-alarm-lighting — arm states and breach lights.
- local-calendar-event-lighting — ICS/CalDAV scenes.
- local-weather-lighting-scenes — station and cached forecast.
- local-seasonal-lighting-transitions — solstice and temp driven.
- local-accessibility-lighting — high contrast and audio cues.
- multi-user-role-based-lighting — roles, priorities, overrides.
- local-pet-and-plant-lighting — animal comfort and grow lights.

## Layer: Resilience
- home-assistant-backup-light-stack — HA snapshot strategy.
- offline-disaster-recovery-drills — kill and restore drills.
- local-smart-bulb-purchasing-guide — buy local-capable hardware.

---

## Quick picking rules
- New install start here: full-offline-home-system-setup
- Cloud audit first: cloud-audit-for-lighting-freedom
- Voice: local-voice-lighting-commands
- Zigbee first: zigbee2mqtt-lighting-installation
- Z-Wave first: zwave-local-lighting-control
- Security layer: iot-vlan-isolation-lighting
