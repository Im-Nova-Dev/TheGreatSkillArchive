---
name: godot-2d-dialog-and-choice-system
description: Godot 2D Dialog And Choice System
---

# Godot 2D Dialog And Choice System

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Dialog And Choice System` in Godot 4.

## GDScript Example

Dialog choice data.
```gdscript
class_name DialogLine
extends Resource

@export var speaker: StringName
@export var text: String
@export var choices: Array[DialogChoice] = []

class_name DialogChoice
extends Resource

@export var text: String
@export var next_id: int
@export var condition: Callable
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
