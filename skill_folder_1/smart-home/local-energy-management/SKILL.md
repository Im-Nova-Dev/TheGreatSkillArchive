---
name: local-energy-management
description: Teach monitoring and optimizing home energy usage with local sensors including Shelly EM/Plus, ESPHome energy monitors, Z-Wave Aeotec, Grafana dashboards, and automated load shedding without cloud APIs.
---

# Local Energy Management

## Hardware stack
- Shelly EM/Plus: clamp CTs on mains; expose via MQTT or REST.
- ESPEnergyShield / DIY eMonLib on ESP32: publish to MQTT.
- Z-Wave Aeotec Home Energy Meter if Z-Wave stack present.

## Data path
```
Sensor -> MQTT topic: energy/* -> Mosquitto -> HA energy dashboard -> Grafana
```

## Actions
- Shed non-essential loads during peak generation gap.
- Schedule high-wattage loads to solar production windows.
- Local-only low-battery alerts via HA notification.

## Privacy
All watt-hours stay in local InfluxDB/Timescale. No cloud meter.

## Teaching exercise
Build a 24h load graph and implement a 3-load shed rule triggered by solar export falling below 1kW.
