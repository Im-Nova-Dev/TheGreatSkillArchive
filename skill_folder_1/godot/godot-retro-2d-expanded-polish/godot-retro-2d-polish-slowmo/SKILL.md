---
name: godot-retro-2d-polish-slowmo
description: Godot Retro 2D Polish Slowmo
---

# Godot Retro 2D Polish Slowmo

## Core Concepts

## Core Concepts
Slow motion for dramatic moments.
```gdscript
func slow_mo(scale: float, duration: float) -> void:
    var prev := Engine.time_scale
    Engine.time_scale = scale
    await get_tree().create_timer(duration).timeout
    Engine.time_scale = prev
```

## Learning Path

1. **Foundation**: Study the concepts and examples.
2. **Implementation**: Rebuild the snippet in a Godot test project.
3. **Deep dive**: Adapt to your genre and art style.
4. **Production**: Polish and ship.

## Common Pitfalls

- Scoping too wide before core loop is fun.
- Hardcoding paths and magic numbers.
- Ignoring Godot’s built-in nodes (TileMap, AnimationPlayer).
- Skipping pixel-snap camera setup.

## Best Practices

- Use typed GDScript and `@onready`.
- Keep scenes modular and composable.
- Profile before optimizing.
- Ship a minimal vertical slice first.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b, KidsCanCode
- /r/godot
- itch.io devlogs
- Game jam communities
