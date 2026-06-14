---
name: godot-2d-event-unhandling-and-bubbling
description: Godot 2D Event Unhandling And Bubbling
---

# Godot 2D Event Unhandling And Bubbling

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Event Unhandling And Bubbling` in Godot 4.

## GDScript Example

Using _unhandled_input and _input for game-wide vs local input.
```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and event.key_label == KEY_ESCAPE:
        get_tree().quit()
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
