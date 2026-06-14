---
name: smart-bulb-installation
description: Teach smart bulb selection, compatibility checks, installation steps, and troubleshooting for Philips Hue, LIFX, Wyze, Nanoleaf, GE Cync, and WiZ bulbs. Focuses on safety, avoiding the dumb-switch trap, pairing flows, and post-install tuning.
---

# Smart Bulb Installation Mastery

## What makes this skill different
It’s not just “screw in bulb, download app.” Mismatched sockets, constant off-switches, and skipped pairing steps are the #1 reasons users abandon smart bulbs after 48 hours.

## Pre-flight checks

### 1. Socket compatibility
  - Form factor: A19 (standard), BR30 (flood), GU10 (spot), ST19 (edison/filament), A60/E27 (European base).
  - Voltage: almost all are 120V in US; 220-240V in EU. A 120V bulb on 240V destroys it instantly.
  - Max temperature: enclosed fixtures need IC-rated bulbs; Philips Hue A19 and LIFX Mini are rated for enclosed use.
  - Dimmer check: smart bulbs need *dumb* trailing-edge or no dimmer on the circuit. If the wall switch is a dimmer, replace it with a standard toggle or install a Lutron Aurora.

### 2. Hub or hubless decision
  - Hue: needs Bridge or Bridge Pro (or Bluetooth per bulb without hub, but that limits automations.)
  - LIFX / WiZ / Wyze / Govee direct: Wi-Fi only, no hub.
  - Nanoleaf / Eve / Aqara: Thread/Matter supported; Apple TV / HomePod / Echo (4th gen) acts as border router.
  - Trade-off: hub = local reliability + fast response; Wi-Fi = simpler but more router-dependent.

## Installation paths

### Path A: Wi-Fi bulb (LIFX, Govee, Wyze, WiZ)
1. Turn off wall switch. Screw in bulb. Turn switch back on.
2. Bulb cycles (if RGB, usually flashes or goes into pairing mode automatically).
3. App steps: install brand app > add device > select Wi-Fi network (2.4GHz required for most initial setup; some add 5GHz later) > enter Wi-Fi password > bulb blinks confirmation.
4. Rename in app: use room + position convention (“Kitchen - Counter 1”, “Bedroom - Left Lamp”).
5. Test from app. Verify it toggles correctly.

### Path B: Zigbee hub bulb (Philips Hue, older GE Cync, innr)
1. Install Hue Bridge on network (ethernet to router, power via USB-C).
2. Open Hue app: Settings > Bridges > add bridge if not auto-detected.
3. Press link button on bridge, then screw in bulb and flip wall switch.
4. Bulb found within 30-60 seconds.
5. Assign room, zone, and firmware update (bridge handles this automatically after 11pm by default).

### Path C: Thread/Matter bulb (Nanoleaf Essentials, Eve, Aqara T2, future Hue Thread)
1. Need a Thread border router: Apple TV 4K, HomePod mini, Echo (4th gen), or Aqara M3 hub.
2. In Home app (Apple) or Google Home / Alexa: scan for Matter device > hold device close to border router for first broadcast.
3. Bulb confirms with blink.
4. Delete duplicates: Hue Bridge Pro can also act as Thread border router; don’t create same bulb twice in different apps.

## Safety rules
- Always turn off wall switch before screwing/unscrewing.
- Never install a wet/bulb-socket with current active (risk of short).
- Enclosed fixture: check “IC” (Insulated Ceiling) rating on bulb packaging.
- Max wattage: never exceed fixture maximum. Most LEDs are 8-11W, trivially below 60W limits.
- Exterior damp vs wet: bulbs in outdoor fixtures need wet-rated; IP65+ usually means sealed.

## Common mistakes
- **The dumb-switch death**: user turns off physical switch, then wonders why app can’t find bulb. Fix: tape switch “on” or replace with smart switch/pico remote so bulb never loses power.
- **2.4GHz hidden**: modern routers merge 2.4GHz and 5GHz SSIDs; initial pairing may fail. Steps: temporarily split SSIDs, pair on 2.4GHz, merge back.
- **Too many bulbs at once**: Zigbee bulbs can flood the network on first pairing. Pair one at a time, wait 30 seconds between each.
- **Wrong app**: some bulbs use brand app only for setup, then work in HomeKit / Alexa exclusively. Stop opening brand app once stable.

## Post-install checklist
- [ ] Bulb toggles on/off reliably in app and via voice.
- [ ] Firmware updated if prompted.
- [ ] Room assignment correct.
- [ ] Scenes created (“Goodnight” = all off, “Reading” = warm 2700K at 80%).
- [ ] Physical switch tape/policy documented for household members.
- [ ] Zigbee channel set to avoid Wi-Fi overlap: 11, 15, 20, or 25 if using Hue.
