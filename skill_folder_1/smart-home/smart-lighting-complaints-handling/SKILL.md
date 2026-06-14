---
name: smart-lighting-complaints-handling
description: Teach handling of post-install customer complaints including lights turning off unexpectedly, colors looking wrong, latency complaints, and device "disappearance" from apps. Gives exact phrasing to users and diagnostic order.
---

# Customer Complaint Response Scripts for Smart Lighting

## Complaint patterns and responses
  1. "My lights randomly turn off."
     - Cause: dumb switch flipped, motion timeout, schedule conflict.
     - Response: "Let's check if the physical switch is accidentally flipping off. Smart bulbs must always have power."
  2. "The colors look wrong."
     - Cause: wrong model selected in app (strip), unsupported color gamut, diffuser wash.
     - Response: "Colors on video won't match reality. Let's calibrate your white point first."
  3. "The light is laggy when I tap the app."
     - Cause: Wi-Fi congestion, cloud latency, Zigbee channel overlap.
     - Response: "Which ecosystem? If Hue, this is local and should be fast; let's test hub connection."
  4. "One light keeps disappearing."
     - Cause: Zigbee mesh weak, bulb paired to another bridge, power cycling.
     - Response: "Rebuild Zigbee mesh by adding a plug as repeater within 10ft."

## Diagnostic teaching order
1. Power state (switch flipped?)
2. App and hub connection status
3. Firmware current?
4. Distance/repeater placement
5. Factory reset last resort
