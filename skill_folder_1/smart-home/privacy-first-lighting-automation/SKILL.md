---
name: privacy-first-lighting-automation
description: Teach designing privacy-first smart lighting automations that function without cloud, with minimal telemetry, and with user-defined data retention rules. Covers local-only voice, local schedule storage, and anti-tracking rules.
---

# Privacy-First Lighting Automation

## Default posture
All timers, sensors, and scenes should work without WAN.

## Cloud containment rules
- Disable vendor cloud toggles in apps.
- Use DNS sinkhole for vendor analytics domains.
- Use MAC randomization on IoT Wi-Fi SSID.

## Voice without cloud
- Siri with HomeKit: more processing on-device than Alexa/Google.
- Home Assistant with voice pipeline: fully local STT/TTS optional.
- Mycroft/OpenVoice: open voice stack but community-support fragile.

## Data retention
- Zigbee2MQTT logs: purge after 48h unless debugging.
- Home Assistant history: prune to 7 days for lighting events.
- No camera data sent off-site.

## Teaching checklist
- [ ] Internet unplugged; scenes still fire.
- [ ] No vendor app telemetry outbound on IoT network segment.
- [ ] User understands local vs cloud tradeoffs.
