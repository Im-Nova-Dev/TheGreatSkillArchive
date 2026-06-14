---
name: godot-2d-ink-dialogue-integration
description: Godot 2D Ink Dialogue Integration
---

# Godot 2D Ink Dialogue Integration

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Ink Dialogue Integration` in Godot 4.

## GDScript Example

Ink callback mapping to GDScript.

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
