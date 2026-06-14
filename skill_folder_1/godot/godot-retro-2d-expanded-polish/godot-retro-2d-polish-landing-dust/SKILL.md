---
name: godot-retro-2d-polish-landing-dust
description: Godot Retro 2D Polish Landing Dust
---

# Godot Retro 2D Polish Landing Dust

## Core Concepts

## Core Concepts
Dust puff on landing.
```gdscript
func _physics_process(delta: float) -> void:
    if is_on_floor() and was_in_air:
        spawn_dust(global_position)
    was_in_air = not is_on_floor()
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
