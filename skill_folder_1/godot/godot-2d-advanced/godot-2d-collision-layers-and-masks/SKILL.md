---
name: godot-2d-collision-layers-and-masks
description: Godot 2D Collision Layers And Masks
---

# Godot 2D Collision Layers And Masks

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Collision Layers And Masks` in Godot 4.

## GDScript Example

Collision filtering example.
```gdscript
func _ready() -> void:
    set_collision_layer_value(1, true)
    set_collision_mask_value(2, true)
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
