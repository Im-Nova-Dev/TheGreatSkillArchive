---
name: godot-2d-area-2d-and-sensors
description: Godot 2D Area 2D And Sensors
---

# Godot 2D Area 2D And Sensors

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Area 2D And Sensors` in Godot 4.

## GDScript Example

Sensor using Area2D.
```gdscript
func _on_area_2d_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        emit_signal("player_entered_zone")
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
