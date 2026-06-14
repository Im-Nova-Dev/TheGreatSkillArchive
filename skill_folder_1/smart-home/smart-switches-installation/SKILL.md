---
name: smart-switches-installation
description: Teach in-wall smart switch and dimmer installation including wiring identification (line/load/neutral/traveler), Lutron Caseta/Diva, Leviton Decora, TP-Link Kasa, Aqara H2, Inovelli, and Wemo. Covers 3/4-way wiring, neutral requirements, Dimmer curve, and avoiding the smart-bulb conflict.
---

# Smart Switch Installation Mastery

## Core insight
A smart switch replaces a dumb switch and should be left ON at all times; the smart control layer comes from app/automation/voice. Treating it like a regular on-off switch creates automation confusion.

## Neutral wire truth table
  Switch type             | Neutral required? | Why
  ------------------------|-------------------|-------------------------------------------
  Lutron Caseta/Diva      | Sometimes        | Some models no-neutral; others need it
  Leviton Decora Wi-Fi    | Yes              | Constant power for radio + relay
  TP-Link Kasa Matter     | Yes              | Same
  Aqara H2 (US)           | No-neutral option| Battery/zigbee-backed loads work without
  Inovelli Blue (Zigbee)  | Sometimes        | Depends on series/firmware
  Wemo                    | Yes              | Older Wi-Fi models need neutral

## Pre-flight electrical safety
- Always confirm wire identity with a non-contact tester after breaker off.
- Label wires before disconnecting.
- Do not assume black = hot; in 3/4-way, black may be traveler.
- Use wire strippers rated for 12-14AWG Romex. Exposed copper >1/8in is too long and increases short risk.

## Common wiring scenarios
  1. Single-pole (single switch, single light):
     - Usually 2 or 3 wires in box. Add neutral if white wire present.
  2. 3-way (two switches, one light):
     - 3-wire cable between boxes (common + 2 travelers). Smart switch replaces one side; other side may become a “remote” or need adapter (Lutron uses Pico remote; Aqara has D1-H2 variants).
  3. 4-way (three switches):
     - 2x 3-wire cables between middle and ends. Replace middle or use smart-remote-compatible kit.
  4. No-neutral:
     - Use smart-bulb instead, or select specific no-neutral switch (Aqara H2 US no-neutral mandates).

## Installation flow
1. Turn breaker off.
2. Remove old switch; separate hot (likely black), neutral (if present, bundle white), ground (bare/green).
3. Wire new smart switch:
   - Load = to light fixture.
   - Line = always-hot from supply.
   - Neutral = to white bundle (if required).
   - Ground = pigtail to box ground.
4. Fold wires into box; do not crowd. Wires touching back of switch cause shorts.
5. Mount switch; restore power.
6. App pairing:
   - Lutron: use Lutron app + Caseta Hub. Hub on network, press pairing.
   - Leviton/Kasa: app scans Wi-Fi network.
   - Aqara: uses Aqara Hub or HomeKit pairing.

## The smart-bulb trap
- Do NOT combine smart switch + smart bulb on the same fixture.
- Smart switch kills power; smart bulb loses connectivity.
- Options:
  - Use smart switch with dumb neutral bulb.
  - OR use smart switch left always-on + smart bulb (but keep physical switch taped).
  - OR use Lutron Aurora (bulb dimmer over socket) to avoid wall switch entirely.
  - OR rewire to switched-hot-to-bulb layout (requires electrician).

## Dimmer curves and compatibility
- Dimmable LEDs only. Do not use dimmers on ceiling fans or fluorescent ballasts.
- Trailing-edge (reverse-phase) dimmers are safest with LEDs; leading-edge causes buzzing.
- Lutron Diva is trailing-edge; CFL/LED compatible.

## Troubleshooting
  Symptom                  | Cause                       | Fix
  -------------------------|-----------------------------|----------------------------------------
  Switch broadcasts Wi-Fi  | Reset/firmware issue         | Power-cycle after 30s
  Light flickers at dim-low | Dimmer lowest-level cutoff   | Raise min-level in app
  Both switches on fight   | 3-way wiring mismatch        | Confirm common wire placed correctly
  Bulb reset when wall switch toggled | dumb-switch conflict | Tape switch, replace with Pico

## Teaching drills
- Drill 1: apprentice identifies 3 single-pole, 2 3-way mock boxes correctly in <5 min each.
- Drill 2: mock 3-way wiring failure; apprentice must find mislabeled traveler and correct without power.
- Drill 3: Dimmer minimum setting lab; apprentice sets physically lowest stable brightness, then captures app minimum.

## Post-install
- [ ] Breaker not tripping; no warm smell at switch.
- [ ] App command success within 1s latency.
- [ ] Voice control tested.
- [ ] Local control tested (Pico, app, physical if not left always-on).
- [ ] If dimmer: smoothly dims at 1%, 10%, 50%, 100%.
