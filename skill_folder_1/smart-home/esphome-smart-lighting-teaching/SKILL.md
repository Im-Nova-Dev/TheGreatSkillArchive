---
name: esphome-smart-lighting-teaching
description: Teach ESPHome as an open-source firmware for DIY smart bulbs, switches, and relays. Covers compatible hardware, YAML configuration, Wi-Fi vs Ethernet, deep sleep for battery sensors, and why ESP32-S2/S3 is preferred for lighting.
---

# ESPHome Smart Lighting — Teaching Framework

## Core concept
ESPHome replaces Tuya/cloud firmware on ESP32/ESP8266 with open-source local firmware that speaks Home Assistant API directly.

## Hardware selection
  - ESP32-S2/S3: best for RGBW bulbs; plenty of PWM/SPI/I2C.
  - ESP32-C3: cheaper, lower pin count; okay for on/off relays and white dimming.
  - ESP8266: legacy; avoid for new designs.

## YAML config anatomy
```yaml
light:
  - platform: rgb
    red: gpio16
    green: gpio17
    blue: gpio18
    white: gpio19
    name: "Desk Lamp"
```

## Wi-Fi vs wired in lighting
- Wi-Fi ESP32 inside fixture: fine if fixture is mains-isolated from Wi-Fi module; use isolated driver.
- ESP32 behind smart switch: preferred location; keeps ESP32 cool and accessible.

## Teaching sequence
1. Flash ESPHome firmware via USB.
2. Configure API and OTA.
3. Pair in Home Assistant.
4. Set up light entity and scene.

## Privacy wins
- No cloud callbacks.
- OTA updates via local network only.
- Full audit of code on GitHub.

## Limitations
- ESP32 inside bulb voids many bulb warranties.
- I code buys bulb + flash = legal; vendor may disable OTA in future bootloader revs.
