---
name: smart-tube-lights-installation
description: Teach installation of smart LED tube lights including T8/T5 form-factor replacements, ballast bypass vs plug-and-play wiring, driver considerations, and fixture compatibility.
---

# Smart LED Tube Installation Mastery

## Core concept
Smart tube lights replace linear fluorescent tubes in troffers, shop lights, and under-cabinet fixtures. They shift from magnetic ballast-dependent to line-voltage direct wire or intelligent driver setups.

## Terminology
  - T5/T8/T12: tube diameter in eighths of an inch (T5 = 5/8in, etc.). T8 is dominant in US commercial.
  - Ballast-compatible (Type A): tube works with existing electronic ballast — simpler swap but adds failure point.
  - Ballast-bypass (Type B): direct-wire to line; removes ballast from equation. Most reliable long-term; safer for smart driver integration.
  - Hybrid: works either way.

## Pre-installation
- Identify existing setup: single-ballast (1 lamp) or tandem (2 lamps). Unsure? take picture of wiring before touching.
- Disposal: old fluorescent tubes + ballasts often contain mercury; bag and take to recycling center.
- Wire nuts rated for stranded solid hybrid wire; label old wires for 5 minutes.

## Installation path: plug-and-play swap
1. Turn off circuit; verify dead.
2. Remove diffuser; twist old tube out.
3. Insert new tube oriented with G13/G10q base straight — do not force.
4. Restore power; light should turn on within seconds.
5. If using smart-app integration: tube may have embedded Zigbee/Thread radio; ensure hub is nearby.

## Installation path: ballast bypass (preferred for smart)
1. Kill power; open fixture.
2. Cut ballast input and output wires. Cap/seal removed wires individually with wire nuts + shrink.
3. Wire line (black) and neutral (white) to lampholders per tube wiring diagram:
   - Usually one side gets both hot wires, other side both neutrals (or split).
4. Add grounding wire to metal fixture if grounding exists.
5. Reassemble; turn on.
6. In app: pair each tube as independent device.

## Hazards
  Hazard                                | Mitigation
  --------------------------------------|-----------------------------------------------
  T12 magnetic ballast running on Type B tube without bypass | Rewire or replace ballast
  T5 retrofitted into T8 socket         | Physical mismatch; use proper retrofit base
  Shared neutral across multiple tubes  | Keep neutrals separate or use 2-pole breaker

## Teaching drills
- Drill 1: apprentice identifies ballast type from drawings (instant start vs programmed start).
- Drill 2: wire diagram sandbox. Give 3 fixture types; apprentice writes pairing instructions.
- Drill 3: live demo with training fixture; apprentice completes take-down and rewire in <20 min.

## Post-install
- [ ] Old ballast physically removed or isolated so no future tech wires back in.
- [ ] Each tube paired in app and named by location.
- [ ] Brightness and color temperature set.
- [ ] Status light hidden behind diffuser if visible.
