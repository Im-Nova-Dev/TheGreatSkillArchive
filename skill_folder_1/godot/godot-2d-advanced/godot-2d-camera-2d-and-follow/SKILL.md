---
name: godot-2d-camera-2d-and-follow
description: Godot 2D Camera 2D And Follow
---

# Godot 2D Camera 2D And Follow

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Camera 2D And Follow` in Godot 4.

## GDScript Example

Camera2D follow setup.
```gdscript
@onready var camera: Camera2D = $Camera2D

func _process(delta: float) -> void:
    camera.global_position = global_position
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
