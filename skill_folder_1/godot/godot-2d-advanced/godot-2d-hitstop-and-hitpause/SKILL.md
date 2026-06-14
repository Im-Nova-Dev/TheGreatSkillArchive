---
name: godot-2d-hitstop-and-hitpause
description: Godot 2D Hitstop And Hitpause
---

# Godot 2D Hitstop And Hitpause

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Hitstop And Hitpause` in Godot 4.

## GDScript Example

Hitstop juice.
```gdscript
func hitstop(duration: float) -> void:
    var prev := Engine.time_scale
    Engine.time_scale = 0.0
    await get_tree().create_timer(duration).timeout
    Engine.time_scale = prev
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
