---
name: godot-2d-node-communication-patterns
description: Godot 2D Node Communication Patterns
---

# Godot 2D Node Communication Patterns

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Node Communication Patterns` in Godot 4.

## GDScript Example

Signals vs direct references vs groups.
```gdscript
# Direct reference
$Player.health_changed.connect(_on_player_health_changed)

# Signal bus pattern
SignalBus.health_changed.connect(_on_health_changed)
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
