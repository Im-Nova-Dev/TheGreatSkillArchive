---
name: godot-retro-2d-adaptive-music
description: Godot Retro 2D Adaptive Music
---

# Godot Retro 2D Adaptive Music

## Core Concepts
Layered music by intensity.
```gdscript
class_name MusicManager extends Node

@onready var calm: AudioStreamPlayer = $Calm
@onready var battle: AudioStreamPlayer = $Battle

func set_intensity(level: int) -> void:
    if level == 0:
        battle.stop()
        calm.play()
    elif level >= 1:
        calm.stop()
        battle.play()
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
