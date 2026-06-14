---
name: smart-light-sensors-installation
description: Teach placement, pairing, and automation use of standalone daylight/lux sensors and combined motion-lux sensors. Covers calibration, ceiling vs wall mounting, and using lux data as input for lighting scenes.
---

# Smart Light Sensors Installation Mastery

## Core concept
Lux (illuminance) sensors read ambient brightness in lux units. They let automations respond to real light levels instead of (or in addition to) timers.

## Dedicated vs combined sensors
  - Dedicated lux sensor: rare standalone; usually embedded (Hue Motion, Eve Motion, Aqara FP2).
  - PIR + lux combined: most common product form.
  - mmWave + lux: Aqara FP2 style.

## Installation
- Mount away from direct view of bulbs to avoid saturation.
- Indoor: ceiling mount reads room average; wall/table reads task area.
- Outdoor: install under eaves; avoid facing sky at night for accurate dusk/dawn threshold.

## Automation patterns
  - “If lux < 50 and motion, turn on porch light to 30%” — conserves energy vs motion-only.
  - “If lux > 300, lower blinds” — daylight harvesting.
  - “If lux stable at 0 for 8h AND no motion, switch to away mode.”

## Calibration
- Take baseline at noon with lights off; record lux.
- Set automation threshold relative to baseline.
- Re-calibrate seasonally (summer vs winter lux profiles differ).

## Teaching drills
- Drill 1: apprentice reads lux in 4 home spots and compares to table standards (kitchen task = 300-500lux).
- Drill 2: write 2-lux automation in HomeKit/Hue app from raw requirement.
- Drill 3: diagnose overtriggered sensor and reduce false positives.

## Post-install
- [ ] Sensor paired and reading lux in app.
- [ ] Baseline lux values documented per room.
- [ ] Automation validated over 24-hour cycle including sunrise/sunset.
