---
name: godot-2d-input-mapping-and-actions
description: Godot 2D Input Mapping And Actions
---

# Godot 2D Input Mapping And Actions

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Input Mapping And Actions` in Godot 4.

## GDScript Example

Using InputMap instead of hardcoded keys.
```gdscript
# In project settings, map "move_left" and "move_right".
func get_movement() -> float:
    return Input.get_axis("move_left", "move_right")
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
