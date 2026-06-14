---
name: godot-retro-2d-noise-and-percussion
description: Godot Retro 2D Noise And Percussion
---

# Godot Retro 2D Noise And Percussion

## Core Concepts
White noise burst for snare/explosion.
```gdscript
func noise_burst(duration: float = 0.1) -> void:
    # Generate using AudioStreamGenerator
    pass
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
