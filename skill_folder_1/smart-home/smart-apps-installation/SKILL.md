---
name: smart-apps-installation
description: Teach installing and organizing smart lighting apps across Hue, LIFX, Nanoleaf, Govee Home, Eve, Kasa, Tapo, and HomeKit. Covers naming conventions, firmware updates, voice sync, and reducing app sprawl.
---

# Smart Lighting Apps Setup Mastery

## Core concept
Households accumulate 4-6 apps. Poor organization leads to abandoned devices. Reduce sprawl, then fix names, then do discovery.

## Setup order
1. Install hub app first (Hue, Aqara).
2. Pair hub + devices; rename inside ecosystem app first.
3. Link hub to platform (HomeKit, Alexa, Google).
4. Do not rename after linking or names desync.

## Organization technique
- Use room-first names: "Living Room - Sofa Left" not "Hue Color 2".
- Keep names short; avoid emoji in device names (breaks some automations).
- Group by room first, scenes second.

## Firmware cadence
- Turn on automatic updates; off-hours only.
- Never power-cycle during bridge firmware update.

## Security hygiene
- Unique password per app account when separate accounts exist.
- Enable 2FA where available (Lutron, Hue).
- Disable UPnP on Hue Bridge if router exposes it externally.

## Voice-discovery hygiene
- Alexa/Google: re-run discovery after bulk renames.
- HomeKit/Matter: re-scan QR after rename moves device.

## Post-setup checklist
- [ ] Every device reachable in primary app.
- [ ] Names consistent across apps/voice.
- [ ] Firmware updates scheduled.
- [ ] Backup account info documented for landlord/renter turnover.
