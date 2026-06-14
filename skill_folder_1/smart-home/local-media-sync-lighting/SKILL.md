---
name: local-media-sync-lighting
description: Teach synchronizing lighting with local media using Plex/Jellyfin webhooks, Kodi events, and Spotify Connect-local or Snapcast sinks for mood lighting without cloud-dependent media players.
---

# Local Media Sync Lighting

## Stack
- Jellyfin/Plex over LAN with webhook to HA.
- Kodi JSON-RPC to HA.
- Snapcast multi-room audio + MQTT lighting events.

## Mood patterns
- Horror movie: red low ambient.
- Morning news: cool neutral + rising brightness.

## Teaching exercise
Trigger wallpaper wash when music starts via Snapcast state.
