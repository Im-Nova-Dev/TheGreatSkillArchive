---
name: smart-lighting-schedule-design
description: Teach building honest light schedules including sunset/sunrise offsets, presence simulation when away, vacation mode, seasonal shifts, and seasonal holiday schedule templates.
---

# Smart Lighting Schedule Design Teaching

## Schedule categories
  - Daily: wake-up, dinner, bedtime.
  - Weekly: weekday vs weekend wake times.
  - Seasonal: summer vs winter sunset offsets.
  - Away: presence simulation for security.
  - Holiday: date-ranged seasonal decor.

## Best practices
- Use local sun events, not fixed times where possible.
- Create "Goodnight" scene tied to time + motion off + phone charging.
- Vacation mode randomizes on/off ±15 min from normal windows.

## Template to reuse
```
Weekdays:
  6:45am - Bedroom fade-in 2700K 1% to 80% over 15 min.
  7:00am - Kitchen counter 4000K 100%.
  Sunset+10min - Porch 2700K 40%.
  11:00pm - Hallway night light 2700K 5% if motion + lux low.

Weekends:
  8:00am - Wake scene delayed.
```