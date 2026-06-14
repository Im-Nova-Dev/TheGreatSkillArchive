---
name: godot-2d-grid-snapping
description: Godot 2D Grid Snapping
---

# Godot 2D Grid Snapping

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Grid Snapping` in Godot 4.

## GDScript Example

Grid snapping helper.
```gdscript
func snap_to_grid(pos: Vector2, cell_size: float = 16.0) -> Vector2:
    return (pos / cell_size).floor() * cell_size
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
