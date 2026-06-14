---
name: godot-2d-raycast-2d-and-line-of-sight
description: Godot 2D Raycast 2D And Line Of Sight
---

# Godot 2D Raycast 2D And Line Of Sight

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Raycast 2D And Line Of Sight` in Godot 4.

## GDScript Example

Simple line-of-sight with RayCast2D.
```gdscript
@onready var ray := $RayCast2D

func has_line_of_sight(to: Vector2) -> bool:
    ray.target_position = to_global(to) - global_position
    ray.force_raycast_update()
    return ray.is_colliding() == false
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
