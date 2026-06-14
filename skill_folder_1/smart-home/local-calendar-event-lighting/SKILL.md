---
name: local-calendar-event-lighting
description: Teach controlling lights from an offline shared calendar using local ICS feeds or Home Assistant calendar integration, with routines for wake, away, and guest modes tied to local events.
---

# Local Calendar Event Lighting

## Options
1. HA calendar + automation.
2. Radicale or baikal for local CalDAV.
3. ICS over local HTTP from Nextcloud.

## Routine examples
- Wake: bed light ramp 07:00 on weekdays.
- Away: all lights off + simulated presence after 18:00.
- Guest mode on "Guests" label: lobby light on at sunset 30 min.

## Teaching exercise
Map 3 calendar labels to 3 distinct lighting scenes triggered by event start.
