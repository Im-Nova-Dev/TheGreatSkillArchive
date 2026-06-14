---
name: godot-2d-pause-menu-and-state
description: Godot 2D Pause Menu And State
---

# Godot 2D Pause Menu And State

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Pause Menu And State` in Godot 4.

## GDScript Example

Pause handling.
```gdscript
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_cancel"):
        get_tree().paused = true
        $PauseMenu.show()

func resume_game() -> void:
    get_tree().paused = false
    $PauseMenu.hide()
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
