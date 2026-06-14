---
name: godot-2d-hud-and-ui-bindings
description: Godot 2D Hud And Ui Bindings
---

# Godot 2D Hud And Ui Bindings

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Hud And Ui Bindings` in Godot 4.

## GDScript Example

HUD updating from signals.
```gdscript
func _on_player_health_changed(new_health: int) -> void:
    $HUD/HealthBar.value = new_health
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
