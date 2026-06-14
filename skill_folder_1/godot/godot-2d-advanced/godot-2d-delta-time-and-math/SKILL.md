---
name: godot-2d-delta-time-and-math
description: Godot 2D Delta Time And Math
---

# Godot 2D Delta Time And Math

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Delta Time And Math` in Godot 4.

## GDScript Example

Frame-independent movement basics.
```gdscript
func move_toward_target(target: Vector2, speed: float, delta: float) -> Vector2:
    var dir := (target - global_position).normalized()
    return global_position + dir * speed * delta
```

## Common Pitfalls

- Writing physics in `_process` instead of `_physics_process`.
- Forgetting typed `@onready` variables.
- Using global magic numbers everywhere.
- Hardcoding paths and not using exported resources.

## Best Practices

- Prefer typed GDScript with `get_class()` checks.
- Keep node references in `@onready` or inject them.
- Use resources for data, nodes for behavior.
- Profile before optimizing; avoid premature caching.

## Resources

- Official Godot 4 docs
- GDQuest and HeartBeast tutorials
- /r/godot and official Q&A
- Godot Asset Library
- YouTube: GYArray, GameDev Tavern, 41b
