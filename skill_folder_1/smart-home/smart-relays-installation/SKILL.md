---
name: smart-relays-installation
description: Teach behind-the-switch and inline smart relay installation including Shelly Plus, Aeotec, Inovelli relays, load matching, bypass of existing switches, and maintaining local control. Includes safety and common wiring mistakes.
---

# Smart Relay Installation Mastery

## Core concept
A relay goes behind an existing switch or in a fixture, making it “smart” without removing the visible switch. Critical for retrofits where strip/wire replacement is unwanted.

## Relay types
  - Behind-the-switch modules: Shelly Plus 1 / Plus 2PM; Aeotec Smart Switch 6/7; Inovelli behind-switch unit.
  - Fixture-mounted: placed in ceiling fan or light housing.
  - Load types: resistive (incandescent), capacitive (LED driver), inductive (motor/fan). Match relay type to load.

## Pre-installation targeting
- Appliance/target wattage must be below relay max (often 10-16A resistive).
- Check fixture wire insulation class; use low-voltage DC relays only inside driver housings, not directly on line voltage without enclosure.
- Determine if existing switch is 3/4-way; relays can be placed on one leg, then that leg becomes local override.

## Installation flow: behind switch
1. Turn breaker off; verify dead.
2. Remove wall plate; pull switch out.
3. Disconnect line (hot in) and load (hot out). Do NOT disconnect neutrals unless needed.
4. Connect line to relay IN; load to relay OUT.
5. Tuck relay into back of box; ensure it doesn’t block device screw terminals.
6. Re-mount physical switch (now controlling relay signal).
7. Restore power.
8. In app: local/remote enable, labeling.

## Installation flow: inline or fixture
1. Identify load hot on fixture wire; mark with tape.
2. Splice relay into line hot with wire nuts + mechanical strain relief.
3. Mount inside j-box if fits; else use project box.
4. Restore power; app discovery.

## Neutral dependency
- Some relays need neutrals; in older homes lacking white bundle, choose no-neutral model or run new wire (code constraint; consult sparky).

## Safety cautions
- Never exceed relay max load. 1800W on a 10A (= 1200W) relay = melted contact.
- Use appropriately rated wire nuts; junction inside switch box counts as accessible splice location.
- For LED loads: do not pair relay with an external trailing-edge dimmer; keep relay on/off and dim at bulb or embedded driver.

## Teaching drills
- Drill 1: label 5 wire colors under time pressure; apprentice must correctly tag line/load/neutral/ground on photo sets.
- Drill 2: virtual relay sizing problem: 8 LED downlights at 12W each; apprentice calculates draw and picks correct relay.
- Drill 3: failure scenario — relay overheated due to oversized fan; apprentice diagnoses amp rating and respec to correct part.

## Post-install
- [ ] Relay not warm after 30 min with load.
- [ ] Physical switch still toggles load locally.
- [ ] App and voice control on same device within <1s latency.
- [ ] Relay wired with mechanical strain relief; no wire pulling at nut.
