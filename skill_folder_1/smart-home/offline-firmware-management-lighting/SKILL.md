---
name: offline-firmware-management-lighting
description: Teach managing local firmware updates for ESPHome/Tasmota/Shelly/WLED devices without cloud accounts using version pinning, local OTA via broker or HTTP, rollback, and staged deployment.
---

# Offline Firmware Management

## Principles
- No device should ever reach out for firmware updates.
- Maintain approved version manifest per device type.
- Rollback is mandatory before applying any production change.

## ESPHome/Tasmota
- Publish new binary to local web path.
- Trigger OTA via MQTT command pointing at LAN URL or use HA update entity.

## Shelly/WLED
- Use REST update endpoint with local file source.
- Stage then apply; allow health check before confirming.

## Teaching exercise
Push a config change, verify revert path, all offline.
