---
name: tuya-convert-esphome-migration
description: Teach converting Tuya-based smart bulbs and plugs to ESPHome/Tasmota via tuya-convert and newer methods. Covers hardware requirements, flash flow, preserving warranty implications, and restoring stock firmware.
---

# Tuya Convert + ESPHome Migration — Teaching

## Why this matters
Tuya devices are cheap but cloud-dependent. Converting them to open firmware lets users regain local control.

## Method options (2026)
- Tuya Convert: legacy OTA flash via Wi-Fi provisioning. Many newer devices now flash-protected; success rate dropping.
- Serial flash: opening device and connecting USB-UART to ESP module. Reliable but invasive.
- Kauf/similar pre-flashed bulbs: buy ESPHome-ready; skip flashing entirely.

## Tuya Convert flow
1. Ensure device is still on cloud firmware <5.x and supports OTA on unencrypted broadcast.
2. Boot Linux laptop/SBC with airgapped AP.
3. Start tuya-convert; detect device MAC.
4. Upload Tasmota or ESPHome firmware.

## Risks
- Brick risk if wrong firmware.
- Warranty void on most devices.

## Teaching cues
This is advanced; save for users explicitly seeking privacy. Do not perform on employer equipment.
