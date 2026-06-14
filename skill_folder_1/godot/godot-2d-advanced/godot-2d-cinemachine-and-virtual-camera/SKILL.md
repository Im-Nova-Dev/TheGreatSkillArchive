---
name: godot-2d-cinemachine-and-virtual-camera
description: Godot 2D Cinemachine And Virtual Camera
---

# Godot 2D Cinemachine And Virtual Camera

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Cinemachine And Virtual Camera` in Godot 4.

## GDScript Example

Camera state system.
```gdscript
class_name CameraState2D
extends Node2D

@export var follow_speed := 8.0
var target: Node2D
var current_target: Vector2

func _process(delta: float) -> void:
    if target:
        current_target = target.global_position
    global_position = global_position.lerp(current_target, follow_speed * delta)
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
