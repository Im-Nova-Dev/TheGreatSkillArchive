---
name: diy-smart-bulb-hardware-teaching
description: Teach building custom local smart bulbs from ESP32 + LED driver + socket. Covers selecting driver ICs, isolated vs non-isolated designs, thermal design, form factor selection, FCC/CE warnings, and why most DIY bulbs cost more than store-bought in 2026.
---

# DIY Smart Bulb Hardware — Teaching

## Why this is niche
Store-bought ESPHome bulbs like KAUF exist because DIY is expensive and time-consuming. Teach DIY for education, not to save money.

## Block diagram
```
E26 base -> AC-DC driver (e.g., Mean Well LDD module) -> LED string
                                      -> ESP32 (non-isolated) controls PWM
```

## Isolation rule
Put ESP32 on isolated DC supply. Do not tie ESP32 ground to mains neutral./isolation gap or opto-coupler mandatory if sharing power.

## Thermal
Enclosed bulb traps heat. 5V/10A in metal cap exceeds 85C quickly. Use:
- Exposed driver.
- Heatsink cap.
- Derate power to 70%.

## Shopping list for teaching lab
- E26 socket breakout board.
- ESP32-S2 mini.
- 12V LED driver + buck to 5V for ESP.
- WS2812B or PWM white LED strip segment.
- Case printed or heatshrink.

## Teaching takeaway
DIY bulbs demonstrate how proprietary bulbs work internally. Most users are better served buying pre-flashed open bulbs.
