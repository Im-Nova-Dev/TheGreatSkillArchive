---
name: godot-2d-crunch-and-damage-numbers
description: Godot 2D Crunch And Damage Numbers
---

# Godot 2D Crunch And Damage Numbers

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Crunch And Damage Numbers` in Godot 4.

## GDScript Example

Damage number billboard.
```gdscript
class_name DamageNumber
extends Node2D

@export var value := 0

func _ready() -> void:
    $Label.text = str(value)
    await get_tree().create_timer(0.5).timeout
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
