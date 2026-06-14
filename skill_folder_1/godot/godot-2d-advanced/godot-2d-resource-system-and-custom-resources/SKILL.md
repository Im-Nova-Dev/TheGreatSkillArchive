---
name: godot-2d-resource-system-and-custom-resources
description: Godot 2D Resource System And Custom Resources
---

# Godot 2D Resource System And Custom Resources

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Resource System And Custom Resources` in Godot 4.

## GDScript Example

Designing custom data-driven resources.
```gdscript
class_name ItemData
extends Resource
@export var item_name: String
@export var icon: Texture2D
@export var damage: int
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
