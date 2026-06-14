---
name: local-weather-lighting-scenes
description: Teach driving lighting scenes from local weather data sources including self-hosted weather stations, open APIs available over LAN, and offline forecast caching integrated with Home Assistant automations.
---

# Local Weather-Based Lighting Scenes

## Data options
- Weather station: Ecowitt or local station -> MQTT.
- Offline cached forecast: dark-sky local cache or met.no via local proxy.
- Tide/sun data from HA built-in sun integration.

## Scene rules
- Overcast afternoon: warm/cool boost.
- Storm warning: porch lights max + red hallway strips.
- Clear cold night: timed porch off, bedroom warm.

## Teaching exercise
Create 3 automations that react to local weather without internet.
