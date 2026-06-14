---
name: smart-light-panels-installation
description: Teach installation, layout planning, and post-install configuration for modular smart light panels (Nanoleaf Shapes/Lines/Skylight/Blocks) and flat-panel ceiling lights. Covers adhesive vs mounting, layout design, daisy chains, hub-free Thread pairing, and troubleshooting pixel/segment dropouts.
---

# Smart Light Panels Installation Mastery

## Core concept
Smart light panels are discrete, often modular units that fit a wall or ceiling. Unlike strips, they consume more power per unit and are usually addressable.

## Panel families to know
  - Nanoleaf Shapes: triangles/hexagons, adhesive or screw mount, 5V USB-C or 12V.
  - Nanoleaf Lines: linear bars; advanced mounting options.
  - Nanoleaf Skylight: flush-mount ceiling panels, mains powered.
  - Nanoleaf Blocks: pegboard/shelf-integrated modular panels.
  - Govee Mini Panel Lights: wall panels from 2025, smaller footprint panels.
  - LIFX Tiles: older, discontinued-ish; mention only as historical reference.

## Pre-installation planning

### Layout design
1. Sketch on grid paper or app layout tool first.
2. Keep control box (Hub/controller) within 1m of power outlet.
3. Plan camera distance if using Rhythm/sound-reactive modules.

### Power requirements
- Skylight: mains wired; must be installed in-junction box from house AC.
- Shapes/Lines/Blocks: USB-C or barrel adapter; count A @ voltage.
- Example: 9-panel Shapes kit at ~0.5A each = 4.5A on 5V adapter; use only included power supply.

## Installation flows

### Nanoleaf Shapes (wall)
1. Layout Assist app: virtual probe works; print or view plan.
2. Clean surface thoroughly (same rule as strips).
3. Start from corner nearest power supply.
4. Connect panels with physical clips; lock each clip.
5. Plug in, let calibration run.
6. In Nanoleaf app: set orientation, enable Rhythm if present.

### Nanoleaf Skylight (ceiling)
1. Power off breaker at panel.
2. Remove existing ceiling fixture and j-box.
3. Connect Skylight to house AC using wire nuts; secure mounting bracket.
4. Restore power; app auto-discovers if already paired.
5. If new install: hold phone close for Matter/Thread pairing.

### Govee Mini Panel
1. USB-C or supplied adapter power.
2. 3M pads included; may need supplemental brackets on textured paint.
3. Govee Home app > add device > exact model selection.

## Wiring and safety (ceiling panels)
- Always verify breaker off with non-contact tester.
- Use UL-listed junction components.
- Verify box is rated for fixture weight; use pancake box or fan-rated box if needed.
- Keep a helper: ceiling work requires second set of hands.

## Teaching drills for apprentices
  Drill 1: Layout-only session (no tools). Apprentice draws a 7-panel layout on graph paper and identifies cut/rotation symmetries.
  Drill 2: Adhesion failure recovery. Remove panel, clean residue, re-clean, remount with clips.
  Drill 3: Daisy-chain failure map. Swap power injection order and observe which panels light first.

## Common mistakes
- **Rhythm module orientation**: must face correct direction or detaches; app tells you to rotate.
- **Fragile clips**: never force clips; they crack. Keep spares or use gentle pressure.
- **Overlapping styles**: mixing Shapes wood-look Elements with standard shapes is allowed; do not assume color rendering matches across finishes exactly.
- **Controller loses network**: Skylight over 2.4GHz Wi-Fi; moving router or upgrading to Mesh fixes.

## Pairing checklist
- [ ] Breaker off before wiring (mains variants).
- [ ] Surface clean and dry (adhesive variants).
- [ ] Power supply matches input rating.
- [ ] Layout sequence documented with numbers on back.
- [ ] App pairing succeeds and first panel lights.
- [ ] Rhythm audio cable seated fully if using mic module.
