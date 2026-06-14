---
name: smart-remotes-installation
description: Teach installation and pairing of handheld smart remotes including Lutron Pico, Hue Dimmer Switch, Aqara Wireless Remote, IKEA TRÅDFRI remote, and physical smart-bulb dimmers like Lutron Aurora. Covers labelling, multi-location control, and avoiding smart-bulb trap.
---

# Smart Remote Installation Mastery

## Core concept
A smart remote isn’t “programmed” into the wall — it pairs to a hub or device. This means one remote can control multiple fixtures, rooms, or scenes.

## Product profiles
  - Hue Dimmer Switch V2: 4 buttons, Bluetooth/Zigbee, powered by CR2450 coin cell. Default mapping: on/off, up/down, scene.
  - Lutron Aurora: dimmer plate that sits over existing toggle/bulb socket. Prevents dumb switch from cutting smart bulb power.
  - Pico Paddle Remote: Lutron radio remote; pairs to Caseta Hub; supports single paddle and 2-button variants.
  - Aqara Wireless Remote Switch: Zigbee/Thread; rocker or single button; 3V coin cell.
  - IKEA TRÅDFRI: Zigbee; works with Hue bridge or standalone Tradfri gateway.

## Selecting control mode
- Wired in-wall: use smart switch/dimmer instead.
- Multi-location control: remote + always-on smart switch/bulb is best pattern.
- No-neutral scenario: Aurora or battery remote avoids requiring always-hot.

## Pairing flows
### Hue Dimmer
1. With bulb on, hold dimmer near bulb (within 6ft).
2. Press-and-hold ON + OFF buttons on dimmer ~10s until LED flashes green.
3. Hue app: Accessories > Add accessory > Dimmer Switch.
4. Configure button actions.

### Lutron Aurora
1. Remove wall toggle switch cover; press Aurora base over switch.
2. By twisting on, Aurora mechanically locks toggle ON.
3. Press pairing button on Lutron app; Aurora joins Caseta Hub.
4. Assign to room, select dimmer curve.

### Pico Remote (Caseta)
1. Open Lutron app > Add device > Pico Remote.
2. Press pairing on remote.
3. Assign to control group (e.g., “Living Room Lights”).

## Mounting options
- Wall bracket: many remotes ship with adhesive or screw-mount backplates. Place near door or bed at reach height.
- Magnetic backplate: stick to fridge or steel plate above workbench.
- No mount: coffee table or nightstand.

## Teaching caveats
- **Bad teaching moment**: tell user to tape wall switch. Better: install Aurora or swap switch for smart switch. Tape is a hack, not a solution.
- **Battery life**: teach coin-cell replacement procedure at 12 months.
- **Kids/pets**: remotes as chokers; mount at 5ft+ on wall.

## Troubleshooting
  Symptom              | Cause                    | Fix
  ---------------------|--------------------------|-------------------------------------------
  Button lag            | Weak battery / interference | Replace coin cell / move closer to hub
  Remote controls wrong zone | paired to previous setup | Re-pair; delete old association
  Aurora won’t click    | Switch too wide/thick    | Box extender or Diva switch instead

## Post-install
- [ ] Remote paired and controlling intended lights/scenes.
- [ ] Battery health visible in app.
- [ ] Multiple remotes tested; one scene can be called from two locations.
- [ ] Physical override behavior documented: Aurora keeps bulb ON always; Pico controls via hub.
