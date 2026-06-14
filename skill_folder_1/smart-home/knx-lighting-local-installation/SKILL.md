---
name: knx-lighting-local-installation
description: Teach KNX as an open local standard for professional smart lighting. Covers twisted-pair bus wiring, programming with ETS, device addressing, scene programming, and pairing KNX with Home Assistant for unified control.
---

# KNX Local Lighting Installation

## Core concept
KNX is a wired, vendor-neutral local bus standard. It predates Zigbee but remains the gold standard for deterministic lighting control.

## Physical layer
- Twisted pair; 30V DC bus.
- Line / Branch topology with couplers.
- Each device draws ~10mA from bus.

## Installation
1. Terminate bus at ends with resistor ~100k.
2. Assign physical address: area.line.device.
3. Group addresses for functional groups (e.g., lighting.living).
4. Program with ETS (vendor tool; license needed for large projects).

## Local parity
- KNX does not need internet.
- Interacts with Home Assistant via KNX integration.
- Scenes written in KNX run locally without HA after download.

## Use case
Opaque multi-button panels in commercial spaces; retrofits where Wi-Fi is unacceptable.
