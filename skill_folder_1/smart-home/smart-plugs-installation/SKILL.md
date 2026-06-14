---
name: smart-plugs-installation
description: Teach smart plug installation, safety limits, energy monitoring setup, outdoor variants, and integration with appliances including space heaters, chargers, lamps, and irrigation controllers.
---

# Smart Plug Installation Mastery

## Core rules
A smart plug converts a 120V socket into a remote-controlled switch with optional energy telemetry. Installation is easy, but safety is not optional.

## Spec vocabulary
  - Max load: 10A / 1250W (US) common; some outdoor/large-appliance plugs 15A / 1800W.
  - Energy monitoring: reports Volts/Amps/Watts over time (Kasa KP-115, Meross MSSxxx, Eve Energy).
  - Matter support: Kasa EP25, Tapo P125M, Meross, Eve Energy.
  - Outdoor: IP44/IP65; Wyze Plug Outdoor v2, Kasa Outdoor Plug, Meross Outdoor.

## Safety rules
- Do not use smart plugs with:
  - Space heaters almost universally (overcurrent); if you must, use 15A-rated plug and never set above 1100W.
  - Refrigerators or HVAC compressors (cycling causes contact wear and voltage spikes).
  - Medical equipment.
- Always use plug within marked wattage; 1500W space heater on a 10A/1250W plug = fire risk.

## Installation flow
1. Inspect wall outlet; ensure 3-prong grounded.
2. If plug is bulky and blocks adjacent outlet:
   - Consider extension cord rated 14AWG with single end only.
   - OR move device to a different outlet.
3. Plug in; LED confirms power.
4. App: install brand app > add device > Wi-Fi (2.4GHz for initial setup on many models).
5. Rename for location + device: “Kitchen - Crockpot” vs “Living Room - Fan”.
6. Group by room or automation tag.

## Energy monitoring setup
- Baseline: leave device running 24h; verify kWh reading matches utility expectation.
- Appliance detection: use logs to identify vampire loads (old receivers, game consoles on standby).
- Notifications: Kasa/Tapo allow alerts on high usage; ideal for “is freezer defrosting?” or “did dryer finish?”.

## Outdoor plugs
- Mount 12in+ above grade; do not lay in mud.
- Use GFCI-protected branch circuit.
- Weatherproof “bubble” cover when not in use.
- Cable routing: route through drip loop so water runs off rather than down into plug.

## Troubleshooting
  Symptom                   | Cause                    | Fix
  --------------------------|--------------------------|------------------------------------
  App shows offline          | Wi-Fi signal poor         | Move router or add extender
  No power after reset       | Wi-Fi failed to rejoin    | Hold setup button 5s, re-pair
  Energy reading stuck       | Calibration needed        | Re-baseline with known load

## Teaching drills
- Drill 1: reading plug rating and matching to appliance math (Watts = Volts × Amps).
- Drill 2: outdoor cord routing with drip loop; apprentice demonstrates on garden model.
- Drill 3: weekend-away energy audit; apprentice exports plug logs and identifies top 5 vampire loads.

## Post-install
- [ ] Plug name conveys room + appliance.
- [ ] Energy montioring baseline recorded.
- [ ] Voice scene tested (“Alexa, turn off living room fan”).
- [ ] Outdoor: GFCI tested, bubble cover closed.
