---
name: local-seasonal-lighting-transitions
description: Teach automated seasonal lighting transitions using local sunrise/sunset calculations, astronomy data from HA, temperature sensors, and holiday/solstice themes without cloud APIs.
---

# Local Seasonal Lighting Transitions

## Data
- HA sun.sun and weather integrations.
- Local temp/humidity sensors.
- Local calendar for solstice/holidays.

## Rules
- Winter: longer warm glow, earlier ramp.
- Summer: cooler temps, delayed porch off to match sunset.
- Holiday: seasonal palettes via HA scene.

## Teaching exercise
Build winter/summer scenes that activate by detected season with animated transitions.
