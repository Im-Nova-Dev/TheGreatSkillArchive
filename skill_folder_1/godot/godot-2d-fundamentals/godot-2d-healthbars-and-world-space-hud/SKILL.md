---
name: godot-2d-healthbars-and-world-space-hud
description: Godot 2D Healthbars And World Space Hud
---

# Godot 2D Healthbars And World Space Hud

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Healthbars And World Space Hud` in Godot 4.

## GDScript Example

World-space billboard UI.

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
