---
name: offline-time-lighting-rituals
description: Teach time-based offline lighting rituals using local time source (NTP fallback, RTC module), HA schedules, and timed scenes with graceful degradation if NTP fails.
---

# Offline Time-Based Lighting Rituals

## Time source
- NTP from LAN-only local host; fallback to DS3231 RTC on ESP32.
- Avoid phone system time where possible.

## Ritual patterns
- Sunrise: slow warm rise in bedroom.
- Sunset: porch warm, mains lights off.
- Quiet hours: red strip routes to bathroom only.

## Teaching exercise
Build sunrise curve with color temp and brightness using only local scheduler.
