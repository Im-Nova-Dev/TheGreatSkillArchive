---
name: godot-2d-scene-structure-and-best-practices
description: Godot 2D Scene Structure And Best Practices
---

# Godot 2D Scene Structure And Best Practices

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Scene Structure And Best Practices` in Godot 4.

## GDScript Example

Key topics: organizing 2D scenes, root node choices, instancing.
Code snippet:
```gdscript
# Example: Main scene structure
# - Node2D (root)
#   - CanvasLayer (UI/HUD)
#   - Node2D (World)
#     - TileMapLayer
#     - Node2D (Player)
#     - Node2D (Enemies)
#     - Node2D (Effects)
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
