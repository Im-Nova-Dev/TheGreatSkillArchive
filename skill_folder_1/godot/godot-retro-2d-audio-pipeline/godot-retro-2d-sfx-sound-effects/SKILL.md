---
name: godot-retro-2d-sfx-sound-effects
description: Godot Retro 2D Sfx Sound Effects
---

# Godot Retro 2D Sfx Sound Effects

## Core Concepts
Retro sound design principles.
- Short, snappy envelopes.
- Limited channels (3-4 simultaneous).
- Pitch variation to avoid repetition.

## GDScript Example
```gdscript
func play_jump() -> void:
    var p := AudioStreamPlayer.new()
    p.stream = preload("res://sfx/jump.wav")
    p.pitch_scale = randf_range(0.95, 1.05)
    add_child(p)
    p.play()
    p.finished.connect(queue_free)
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
