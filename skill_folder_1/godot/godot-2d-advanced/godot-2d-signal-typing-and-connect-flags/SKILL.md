---
name: godot-2d-signal-typing-and-connect-flags
description: Godot 2D Signal Typing And Connect Flags
---

# Godot 2D Signal Typing And Connect Flags

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Signal Typing And Connect Flags` in Godot 4.

## GDScript Example

Typed signals and connect flags in Godot 4.
```gdscript
signal health_changed(new_health: int)

func _ready() -> void:
    health_changed.connect(_on_health_changed, CONNECT_DEFERRED)
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
