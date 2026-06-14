---
name: godot-2d-tool-script-and-editor-plugins
description: Godot 2D Tool Script And Editor Plugins
---

# Godot 2D Tool Script And Editor Plugins

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Tool Script And Editor Plugins` in Godot 4.

## GDScript Example

Tool script basic setup.
```gdscript
@tool
extends Node2D

func _process(delta: float) -> void:
    if not Engine.is_editor_hint():
        return
    queue_redraw()

func _draw() -> void:
    draw_circle(Vector2.ZERO, 32, Color.WHITE)
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
