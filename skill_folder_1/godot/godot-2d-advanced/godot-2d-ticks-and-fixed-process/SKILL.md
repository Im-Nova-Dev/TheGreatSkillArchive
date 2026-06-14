---
name: godot-2d-ticks-and-fixed-process
description: Godot 2D Ticks And Fixed Process
---

# Godot 2D Ticks And Fixed Process

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Ticks And Fixed Process` in Godot 4.

## GDScript Example

Using _physics_process for deterministic movement.
```gdscript
func _physics_process(delta: float) -> void:
    # Physics, movement, collision queries here.
    move_and_slide()
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
