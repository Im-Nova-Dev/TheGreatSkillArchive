---
name: lan-only-lighting-dashboards
description: Teach building LAN-only lighting dashboards using Home Assistant frontend, Grafana panels, or raw HTML/JS served from localhost. Covers offline UI work, widget set for mobile, and mirror dashboards for tablets.
---

# LAN-Only Lighting Dashboards

## Goal
User controls lights through an interface never reaching WAN.

## Options
1. HA Dashboard: built-in; tile, gauge, picture-glance cards.
2. Grafana + MQTT data source: metrics + control via URL links.
3. Custom HTML/JS + MQTT over WebSocket: lightweight on tablet.

## Visibility
- Expose dashboards on VLAN with firewall allowing only local access.
- Disable HA remote Nabu Casa or DDNS updates during privacy test.

## Teaching drill
Apprentice builds a responsive tablet dashboard for bedroom lights in <20 minutes.
