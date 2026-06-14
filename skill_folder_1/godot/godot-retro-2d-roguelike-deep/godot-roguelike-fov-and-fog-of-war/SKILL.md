---
name: godot-roguelike-fov-and-fog-of-war
description: Godot Roguelike Fov And Fog Of War
---

# Godot Roguelike Fov And Fog Of War

## Core Concepts
Shadowcasting field of view.
```gdscript
class_name FOVSystem extends Node

func compute_fov(origin: Vector2i, radius: int) -> Array[Vector2i]:
    var visible: Array[Vector2i] = []
    # Implement recursive shadowcasting (0-4 octants)
    return visible
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
