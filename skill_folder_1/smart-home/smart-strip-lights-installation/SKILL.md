---
name: smart-strip-lights-installation
description: Teach LED strip/lightstrip installation including adhesion prep, power routing, cornering, connector use, controller setup (Wi-Fi, Zigbee, Thread), RGB vs RGBIC, and troubleshooting flicker or dropouts.
---

# Smart LED Strip Installation Mastery

## Why this skill matters
Bad adhesion, wrong power injection, and 2.4GHz issues cause 80% of failed strip installs. This skill prevents those.

## Form factor vocabulary
  - LED strip: flexible PCB with surface-mount LEDs; usually 5V, 12V, or 24V.
  - RGBIC: per-LED color control (WS2812B / SK6812 / proprietary). Allows segments, chasing effects. Govee’s key selling point.
  - RGB: same color for whole strip (3-channel).
  - RGBCCT / RGBWW: adds warm white + cool white channels.
  - Density: 30 LEDs/m (ambient), 60 LEDs/m (standard), 120 LEDs/m (high-brightness task).
  - IP20 = indoor dry; IP65 = silicone-coated indoor/outdoor; IP67 = submersible-grade.

## Pre-installation prep

### 1. Surface prep
  - Adhesion only works to 70°F–90°F (21°C–32°C) clean, dry, non-textured surface.
  - Clean with isopropyl alcohol > 90%; do not use Windex or oils.
  - Let dry 60 seconds. peel-and-stick on cold surfaces fails within hours.
  - Avoid freshly painted walls (< 72 hours cure time).

### 2. Cut points
  - Most strips cut at copper pads every 50mm or 100mm (marked “scissors” icon).
  - Cutting outside marks = kills the whole segment.
  - After cutting: seal with end caps (IP65/IP67) or heat-shrink if outdoor.

### 3. Power planning
  - Do not power strips over 5m/16ft from a single end connector. Voltage drop = dim and discolored far end.
  - Use power injection: run 18 AWG from power supply to middle cut-point for 10m+, and again at 16ft+.
  - Max run per data channel: ~5m for most controllers; for longer runs, put a second controller or amplifier in the middle.
  - Power supply sizing: Watts = voltage × amps. Budget 14.4W/m for RGBIC at full white. Round up 20%.

## Installation methods

### Mount A: Adhesive back (most common)
1. Peel ~10cm backer, press to surface corner, slowly peel while smoothing with card.
2. Fix corners with 3M VHB or included clips. Silicone strips eventually release on curved surfaces; use mounting brackets.

### Mount B: Clip/channel (recommended for permanent)
1. Aluminum channel diffuses light and protects strip.
2. Snap strip into channel, mount channel with screws or adhesive.
3. End-to-end mating: use clip for straight joints; avoid overlapping unless using soldered splice.

### Mount C: Corner and 3D shapes
1. Soldering is most reliable but requires skill.
2. For most users: use connector clips rated for the same pitch (usually 10mm).
3. Corners: fold strip inside flexible V-channel or corner bracket; don’t bend strip tighter than 30mm radius.

## Controller pairing

### Hue Lightstrip Plus / Outdoor
1. Connect strip to Hue power supply and controller box.
2. Controller box responds to Zigbee via Hue Bridge.
3. Use standard bulb-pairing flow; controller shows as “Hue Lightstrip”.
4. Controller has physical on/off; keep controller powered always-on.

### LIFX Z / Supercolor
1. Connect power to controller, ZIP to strip.
2. Controller joins Wi-Fi directly (no hub). Use LIFX app.
3. Range extender may be necessary if >10m from router; Wi-Fi signal attenuates through PCM and brick walls.

### Govee strips
1. Controller needs 5V/12V USB or barrel power.
2. Govee Home app: scan QR or add Manually.
3. Choose strip model exactly: strip model IDs differ between “Govee Strip Light 2” and “Strip Light 2 Pro”; choosing wrong model breaks controls or kills effects.
4. For scenes with music or camera sync: enable app permissions and keep Bluetooth on (used for audio/camera Handshake).

## Safety and code
- Class 2 low voltage, but large power supplies (5V/10A = 50W) still generate heat; mount in ventilated area.
- Do not route through insulation or tight enclosed spaces without airflow.
- Wall penetration: use low-voltage bushing; do not staple through cable.
- Outdoor: keep connections above grade, seal with silicone.
- NEC/locality: under-cabinet strips usually exempt from conduit rules, but check local code.

## Troubleshooting matrix
  Symptom                        | Cause                            | Fix
  -------------------------------|----------------------------------|----------------------------------
  Far end dim/white tint shift    | Voltage drop, insufficient power | Add power injection at mid-point
  Only first 10 LEDs work         | Data line not seated / cut        | Check controller data connector
  Entire strip dead               | Power supply under-sized or dead  | Measure voltage at end of strip
  Flickering on camera            | PWM freq too low (most strips)    | Use higher Hz controller or DC
  Colors wrong on half strip      | Wrong model selected in app       | Re-pair with correct model ID
  Strip detaches                  | Surface too cold/unsuitable       | Re-clean, use mounting clips

## Pro tips
- Use consistent model/controller; mixing Hue controller with non-Hue strip = no function.
- Buy 10-15% extra length; mistakes happen.
- For under-cabinet: aluminum channel + diffuser makes it look premium and protects from cooking grease.
