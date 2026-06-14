---
name: godot-2d-time-and-day-night-cycle
description: Godot 2D Time And Day Night Cycle
---

# Godot 2D Time And Day Night Cycle

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Time And Day Night Cycle` in Godot 4.

## GDScript Example

Day/night cycle.
```gdscript
extends CanvasModulate

var time_of_day := 0.0

func _process(delta: float) -> void:
    time_of_day += delta * 0.02
    if time_of_day > 1:
        time_of_day -= 1
    var day_color := Color.WHITE
    var night_color := Color(0.02, 0.02, 0.08, 1.0)
    color = night_color.lerp(day_color, sin(time_of_day * PI))
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
