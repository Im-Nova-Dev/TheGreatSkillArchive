---
name: godot-2d-pickup-and-powerup-system
description: Godot 2D Pickup And Powerup System
---

# Godot 2D Pickup And Powerup System

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Pickup And Powerup System` in Godot 4.

## GDScript Example

Powerup base class.
```gdscript
class_name Powerup
extends Area2D

signal collected(powerup: Powerup)

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        collected.emit(self)
        queue_free()
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
