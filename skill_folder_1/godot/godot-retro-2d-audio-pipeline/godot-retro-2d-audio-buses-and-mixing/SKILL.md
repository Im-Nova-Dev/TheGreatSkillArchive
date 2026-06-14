---
name: godot-retro-2d-audio-buses-and-mixing
description: Godot Retro 2D Audio Buses And Mixing
---

# Godot Retro 2D Audio Buses And Mixing

## Core Concepts
Organizing audio buses.
- Master > Music > SFX > UI
- Duck music when SFX plays.
- Reverb send for dungeons/caves.

## GDScript
```gdscript
var music_bus := AudioServer.get_bus_index("Music")
AudioServer.set_bus_volume_db(music_bus, -6.0)
```

## Learning Path

1. **Foundation**: Study the core concepts.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand with more features.
4. **Production**: Make it a complete game.

## Common Pitfalls

- Scope creep: start tiny.
- Polishing before gameplay is locked.
- Forgetting pixel-snap camera.
- Over-engineering systems.

## Best Practices

- Keep one-click export ready.
- Profile 60 FPS target.
- Use Godot primitives (TileMap, AnimationPlayer).
- Ship one level, then iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b
- /r/godot
- itch.io devlogs
- Game jam communities
