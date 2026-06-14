---
name: audio-reactive-local-lighting
description: Teach audio-reactive lighting using offline audio analysis and local MQTT control without streaming audio to cloud APIs. Covers microphone placement, beat detection, FFT mapping to color/brightness, and localization rules to avoid music leakage outside the home.
---

# Audio-Reactive Local Lighting

## Data path
```
Mic -> PipeWire/PulseAudio -> fffmpeg/FFT pipeline -> MQTT -> HA/LED strips
```

## Options
1. PulseAudio monitor stream + Python FFT.
2. ESP32 with I2S mic: onboard FFT to MQTT.
3. Snapcast audio events + metadata.

## Teaching exercise
Make TV room strip pulse on bass and shut off on silence timeout 5 minutes.
