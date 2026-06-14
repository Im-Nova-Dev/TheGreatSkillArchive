---
name: godot-2d-aim-assist-and-magnetism
description: Godot 2D Aim Assist And Magnetism
---

# Godot 2D Aim Assist And Magnetism

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Aim Assist And Magnetism` in Godot 4.

## GDScript Example

Snap aim to nearest target.

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
