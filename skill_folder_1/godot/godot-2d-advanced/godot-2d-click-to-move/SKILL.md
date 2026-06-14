---
name: godot-2d-click-to-move
description: Godot 2D Click To Move
---

# Godot 2D Click To Move

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Click To Move` in Godot 4.

## GDScript Example

Click-to-move movement.
```gdscript
extends CharacterBody2D

var target_pos := global_position

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        target_pos = get_global_mouse_position()

func _physics_process(delta: float) -> void:
    var dir := (target_pos - global_position)
    if dir.length() > 1:
        velocity = dir.normalized() * 160.0
    else:
        velocity = Vector2.ZERO
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
