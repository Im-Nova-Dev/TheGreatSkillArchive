---
name: godot-2d-screen-shake-and-tooltips
description: Godot 2D Screen Shake And Tooltips
---

# Godot 2D Screen Shake And Tooltips

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Screen Shake And Tooltips` in Godot 4.

## GDScript Example

Shake helper with easing.
```gdscript
extends Camera2D

func shake(intensity: float, duration: float) -> void:
    var initial := offset
    var t := 0.0
    while t < duration:
        var strength := intensity * (1.0 - t / duration)
        offset = Vector2(randf() - 0.5, randf() - 0.5) * strength
        await get_tree().process_frame
        t += get_process_delta_time()
    offset = initial
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
