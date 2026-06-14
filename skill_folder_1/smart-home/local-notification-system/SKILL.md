---
name: local-notification-system
description: Teach building a fully local notification system using Home Assistant notifications, MQTT-triggered alerts, local TTS speakers, and Nokia/LCD panels -- with no vendor cloud.
---

# Local Notification System

## Why local notification is different
- Cloud push services can fail when WAN is down.
- Local ensures alert continuity during internet outages.

## Options
1. HA notify: mobile_app or Telegram bot routed only through LAN.
2. MQTT + client on ESP32 with e-ink display.
3. Piper TTS + Snapcast / pulseaudio group for spoken alerts.
4. Nuki / e-ink panels showing latest motion / door events.

## Privacy rule
No notification content emailed, SMSed, or pushed to any third-party API.

## Teaching exercise
Build a motion-triggered spoken alert for front door during quiet hours, served fully offline.
