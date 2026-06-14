---
name: godot-2d-singletons-and-autoload-patterns
description: Godot 2D Singletons And Autoload Patterns
---

# Godot 2D Singletons And Autoload Patterns

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Singletons And Autoload Patterns` in Godot 4.

## GDScript Example

Using autoloads for global state.
```gdscript
# global.gd (autoload)
extends Node
var current_level: int = 1
var player_health := 100
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
