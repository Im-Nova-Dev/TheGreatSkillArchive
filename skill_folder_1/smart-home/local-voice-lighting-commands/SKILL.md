---
name: local-voice-lighting-commands
description: Teach configuring fully local voice control for lighting including Siri local processing, Home Assistant Voice Pipeline, Zach's Vosk/Whisper local STT, and self-hosted TTS for voice feedback.
---

# Local Voice Control for Lighting

## Reality
Siri processes some commands on-device; Alexa and Google stream audio to cloud. For fully local, use Home Assistant audio stack.

## Local stack
- Audio capture: USB mic on RPi.
- Speech-to-text: Vosk (offline model) or faster-whisper.
- Intent parsing: Home Assistant conversation agent or Node-RED rules.
- Text-to-speech: Piper TTS (local).
- Output: Sonos, Snapcast, or PulseAudio sink.

## Trigger phrase
Choose unique phrase: "Hey Home" instead of "Alexa" to prevent accidental triggers.

## Teaching script
Explain why cloud voice is a privacy boundary and demonstrate latency difference on LAN.
