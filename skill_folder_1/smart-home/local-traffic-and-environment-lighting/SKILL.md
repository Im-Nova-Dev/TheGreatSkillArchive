---
name: local-traffic-and-environment-lighting
description: Teach driving lighting decisions from local environmental sensors including CO2, VOC, temperature, lux, and outdoor traffic via LoRa or local stream -- without relying on cloud APIs.
---

# Local Traffic and Environment-Driven Lighting

## Sensors
- BME280 / SCD41 for temp/humidity/CO2 via I2C or BLE.
- BH1750 or TSL2561 lux sensor for adaptive brightness.
- LoRa node outside for noise/traffic detection.

## Rules
- High CO2: cool white workspace light.
- Evening noise spike: porch flood high + red accent alert.

## Teaching exercise
Automate one room lamp brightness from lux and one corridor color from CO2.
