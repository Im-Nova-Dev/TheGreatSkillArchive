---
name: godot-2d-animation-blend-space-2d
description: Godot 2D Animation Blend Space 2D
---

# Godot 2D Animation Blend Space 2D

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Animation Blend Space 2D` in Godot 4.

## GDScript Example

Blend space example in AnimationNodeBlendSpace2D.
# Configure blend positions in editor and blend via animation tree.
```gdscript
@onready var tree := $AnimationTree

func set_blend(direction: Vector2) -> void:
    tree.set("parameters/blend_position", direction)
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
