---
name: godot-2d-debug-draw-and-gizmos
description: Godot 2D Debug Draw And Gizmos
---

# Godot 2D Debug Draw And Gizmos

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Debug Draw And Gizmos` in Godot 4.

## GDScript Example

Debug draw helpers.
```gdscript
extends Node2D

func _process(_delta: float) -> void:
    queue_redraw()

func _draw() -> void:
    draw_circle(Vector2.ZERO, 24, Color(1, 0, 0, 0.3))
    draw_line(Vector2.ZERO, Vector2.RIGHT * 64, Color.GREEN, 2.0)
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
