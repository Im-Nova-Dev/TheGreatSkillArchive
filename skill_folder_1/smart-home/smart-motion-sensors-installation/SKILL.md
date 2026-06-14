---
name: smart-motion-sensors-installation
description: Teach selection, placement, wiring or battery installation, pairing, and automation strategy for smart motion sensors including Eve Motion, Aqara P1/P2/FP2, Hue Motion, Lutron Occupancy, TP-Link Tapo T100. Covers mounting height, field-of-view masking, and lux-based rules.
---

# Smart Motion Sensors Installation Mastery

## Core concept
A motion sensor reports presence to a hub/app, which then triggers scenes. Sensor quality is judged by detection range, false-positive rate, battery life, and lux integration.

## Product profiles
  - Eve Motion: Matter, 120°, 9m (30ft), IPX3, CR123A, built-in lux sensor.
  - Aqara Motion Sensor P1: Zigbee, ultra-long battery, 180°.
  - Aqara FP2: mmWave presence (not PIR), room-level zoning, no-mask privacy, mains powered.
  - Hue Motion Sensor: Zigbee via Hue Bridge; outdoor version IP65; includes lux.
  - Lutron Caseta Wireless Occupancy Sensor: integrated into switch ecosystem; no hub if wired.
  - TP-Link Tapo T100: Wi-Fi motion sensor; no hub.

## Mounting science
  - Height: 6-8ft (1.8-2.4m) for general occupancy.
  - PIR detection pattern: cone-shaped; aim down 45° to cover walkways.
  - Avoid heat sources: HVAC vents, radiators, dryer exhausts within 10ft cause false triggers.
  - Metal housing: mounting on metal studs or junction boxes may skew PIR range.
  - Corner mounting: widens coverage but reduces sensitivity at long distances.

## Battery vs mains
  - Battery (CR123A, CR2450, AA): easier placement; plan annual/biannual replacement.
  - Mains (Aqara FP2, Lutron): continuous; placement limited to outlet/j-box proximity.

## Pairing flows
### Eve Motion + Apple Home
1. Install Eve app > Devices > Add.
2. Hold within 3ft of HomePod mini / Apple TV (Thread border router).
3. Confirm blink.
4. Assign room.

### Hue Motion Sensor
1. Screw in or mount near power supply.
2. Open Hue app > Settings > Accessories > Add accessory.
3. Press link button on Hue Bridge; sensor pairs automatically.
4. Set lux and motion timeout.

### Aqara FP2
1. Power via USB-C or junction box wiring.
2. Open Aqara app; device appears.
3. Map room zones in app; set privacy zones for areas to ignore.

## False-positive reduction
- Adjust sensitivity in app if supported.
- Use lux minimum: “only trigger if dark” prevents daytime firing.
- Delay window: set 30-60s delay between triggers to avoid chatter.

## Zone and privacy strategies
  - Aqara FP2: define bed as privacy zone so sensor doesn’t track sleep location.
  - Hue, Eve: combine sensors with time-of-day rules so night hallway triggers low-level night light.

## Teaching drills
- Drill 1: apprentice marks optimal sensor height on wall template and explains why.
- Drill 2: false-positive triage; apprentice identifies 3 bad placements on room diagram and corrects them.
- Drill 3: lux rule lab; apprentice writes automation rule: “if hallway dark + motion after 11pm, turn on nightlight at 5%.”

## Post-install
- [ ] Sensor paired and reports motion within 1-2s.
- [ ] Lux reading matches ambient at desk if bulb is smart.
- [ ] No false triggers in first 72-hour observation.
- [ ] Battery health recorded in app.
