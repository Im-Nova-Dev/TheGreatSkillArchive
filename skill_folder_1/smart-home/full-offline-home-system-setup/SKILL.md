---
name: full-offline-home-system-setup
description: Master install and teaching guide for a 100% offline, open-source smart home system. Covers hardware selection, network hardening, hub choice, firmware flashing, local protocol stack, MQTT architecture, voice/dashboards, automation, backup, and a day-by-day teachable install plan.
---

# Full Offline Home System Setup

## Ground rules
- No cloud accounts. No vendor apps after setup.
- Every device must be controllable from the LAN without WAN.
- Fail-closed: WAN unplug = no service loss for local features.

---

## 1. Hardware base

### Core server (1 only)
- In decreasing preference: x86 mini PC > RPi5 4/8GB > Rock 5B
- SSD, not SD (wear under logs/MQTT/Z2M).
- Enclosure with fan for always-on context.
- UPS recommended for power loss resilience.

### Network
- Router with VLAN support (OpenWrt / EdgeRouter / MikroTik).
- Separate SSIDs: primary LAN + IoT VLAN.
- Switch ports: trunk to hub server + APs.
- DNS sinkhole for vendor telemetry (Pi-hole, AdGuard Home, or unbound).

### Zigbee coordinator
- Sonoff P or EFR32-based dongle (Z-Stack 3 / EZSP) — avoid CC2531.
- USB extension cord 1m from server to avoid radio noise.

### Z-Wave dongle (optional but recommended)
- Zooz 800 or Nortek HUSBZB-1 (discontinued but reseller stock).
- Allows Z-Wave JS UI alongside Zigbee2MQTT.

### Matter/Thread border router
- Home Assistant Green/Yellow, or Apple TV/HomePod (if Siri local needed).
- Border router must stay powered for Thread device commissioning.

### Audio (local voice)
- USB mic array (Respeaker Core HAT or AnyTone SDR dongle).
- Speaker on HA host or Snapcast speaker group.

---

## 2. Operating system

### Recommended: bare-metal Debian + Docker Compose on dedicated box
- K3s / Docker Compose for services.
- Avoid HA OS if user wants flexibility; HA OS locks to single USB stick.

### Container map
```
-- services --
homeassistant (official container)
zigbee2mqtt
mosquitto (MQTT broker)
zwave-js-ui (if Z-Wave present)
nodered
grafana (optional)
pi-hole / adguard (optional)
```

---

## 3. Network hardening

### VLAN design
```
LAN (trusted): phones, laptops, admin terminals
IoT VLAN:     bulbs, relays, sensors (isolated)
MGMT VLAN:    server + switches for SSH/API
```

### Firewall defaults
- IoT VLAN → LAN: only MQTT (1883) and HA API port.
- IoT VLAN → WAN: blocked (or allowed for firmware updates only with schedule).
- LAN → IoT: source restricted to HA server MAC/IP.
- DNSSEC + DNS sinkhole on IoT VLAN.

### Verification
- `tcpdump` on IoT bridge: zero WAN attempts after commissioning.

---

## 4. Firmware leg choices

### ESP devices
- Prefer ESPHome over Tasmota for integration depth and HA sync.
- Flash with web flasher if stock bootloader intact; otherwise USB UART.
- Pin map curated per schematic.

### Wi-Fi bulbs with unlockable firmware
- Tuya-Convert if bootloader unlocked (now rare): migrate to ESPHome.
- Closed stock firmware: keep hardware; gate cloud at router level.

### Special
- WLED: use for LED strips; expose HA integration.
- Shelly: stock firmware is already local-first (MQTT + REST) — no flash needed.

---

## 5. Hub software selection

### Home Assistant (default)
- Best integrations, strongest community, long-term stable.
- Supervised install on Debian keeps core portable.
- Zigbee: Z2M over ZHA if multi-vendor; ZHA acceptable for smaller stacks.
- Automation: HA native OR Node-RED (prefer Node-RED for visual debugging).

### openHAB (alternative)
- More Java overhead; excellent for multi-protocol bindings.
- Consider when user already knows OSGi/bindings model.

### Logic rule
- Use ONE hub as source of truth; avoid running both HA and openHAB against same Zigbee coordinator.

---

## 6. Local protocol stack

### Zigbee light path (typical)
```
Bulb <--Zigbee--> CC2652P coordinator <--USB--> Server
  -> zigbee2mqtt <--MQTT--> Mosquitto <--MQTT--> HA
```

### WiFi/relay path
```
Shelly relay --MQTT/HTTP--> Mosquitto --> HA
Tasmota device --MQTT--> Mosquitto --> HA
ESPHome device --native integration--> HA
```

### Voice local path
```
Mic --> PipeWire
  -> Vosk STT / faster-whisper
  -> HA Conversation or Node-RED intent matcher
  -> Piper TTS
  -> Snapcast speaker group
```

---

## 7. MQTT broker

### Mosquitto config must-haves
- `listener 1883` no anonymous; per-device username/password.
- `allow_anonymous false`
- TLS optional but recommended on LAN.
- Persistent session on for battery devices; off for relays.

### Topics
- `zigbee2mqtt/<friendly_name>/set` and `/get`.
- `homeassistant/+/+/config` for HA autodiscovery.

---

## 8. Security and privacy

### Offline guarantees
- No outbound internet from devices except explicit update window.
- No dynamic DNS / Nabu Casa / cloud tunnels.
- HomeKit local: disable homekit controller on devices if local sync is unwanted.

### Credentials
- Broker credentials, SSH keys, AP keys in single `secrets.yaml` not in git.
- Physical access to server = physical access to all keys.

### Firmware pinning
- Hold mantra: one approved firmware version per device type.
- Update via MQTT OTA or local file, not vendor cloud.

---

## 9. Backup and disaster recovery

### Backup layers
1. Mosquitto persistence + retained messages (not enough alone).
2. HA snapshots nightly to local disk, then replicated USB.
3. ESPHome configs in git, backed up to local Git server.

### Coordinator swap drill
- If dongle dies: re-flash same firmware, restore Z2M `database.db`.
- Devices rejoin via permit-join; no factory reset needed.

### Full offline restore test
- Kill WAN, power cycle server, verify all lights come back controllable.

---

## 10. Full install plan (teachable 4-day plan)

### Day 1 — Network + server
- VLANs, firewall rules, DNS sinkhole.
- Install Docker, Mosquitto.
- Verify HA container boots, reachable only on LAN.

### Day 2 — Zigbee + lights
- Flash coordinator firmware if needed.
- Install Z2M.
- Pair 3 bulbs, control from HA; verify WAN-blocked bulbs still work.

### Day 3 — Firmware + broader install
- ESPHome setup for one test strip or relay.
- Add REST or MQTT devices.
- Local voice mic + Piper + Intent.

### Day 4 — Harden + teach
- Remove any remaining cloud account pairing.
- Run full connectivity test.
- Document: device inventory with original brand, MAC, firmware, integration path.

---

## 11. Common pitfalls

- Using cloud bulbs plugged into IoT VLAN still phones home on 5 GHz Wi-Fi.
- Z2M permit-join timeout too short on large house.
- Mosquitto credential mismatch blocks HA autodiscovery.
- Thread border routers wanting WAN for commissioning on some Android phones.
- SD card failure (use SSD/USB for server).

---

## 12. Verification checklist

- [ ] Unplug WAN; all included devices remain controllable.
- [ ] No outbound traffic to vendor domains from IoT VLAN.
- [ ] HA + Z2M + Mosquitto restart automatically on power loss.
- [ ] Voice command turns lights on/off while server has zero WAN.
- [ ] Backup restored to blank server restores automation and device state.
