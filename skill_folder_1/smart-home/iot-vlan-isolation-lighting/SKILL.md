---
name: iot-vlan-isolation-lighting
description: Teach VLAN and firewall setup for smart lighting networks to isolate Wi-Fi bulbs from personal devices, block vendor telemetry, and allow only necessary local access.
---

# IoT VLAN Isolation for Lighting

## Why lighting needs its own subnet
Bulk cheap bulbs often lack sane network behavior. Keep them separate.

## Recommended topology
```
Router
  |-- LAN (trusted: phones, laptops, HA)
  |-- IoT VLAN (192.168.2.0/24)
       |-- Wi-Fi bulbs
       |-- Zigbee coordinator (optional)
       |-- Shelly relays
```

## Rules
- Allow IoT -> LAN for MQTT and HA API only.
- Block IoT -> WAN except necessary.
- Block LAN -> IoT except originate from HA admin host.
- DHCP reservations to known MACs.

## DNS hardening
- Block known telemetry domains at Pi-hole or router DNS.
- Optionally provide fake DNS for vendor update checks.

## Test
WAN unplug still working for Z2M. Wi-Fi bulbs lose cloud app only.
