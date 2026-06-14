---
name: godot-2d-compositor-and-screen-effects
description: Godot 2D Compositor And Screen Effects
---

# Godot 2D Compositor And Screen Effects

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Compositor And Screen Effects` in Godot 4.

## GDScript Example

Compositor-based screen effects.
```gdscript
@onready var cs: Compositor = get_viewport().get_compositor()
# Add pre-defined effects via Code/Compositor resources.
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
