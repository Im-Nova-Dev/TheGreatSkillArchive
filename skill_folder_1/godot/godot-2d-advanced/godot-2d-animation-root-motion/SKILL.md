---
name: godot-2d-animation-root-motion
description: Godot 2D Animation Root Motion
---

# Godot 2D Animation Root Motion

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Animation Root Motion` in Godot 4.

## GDScript Example

2D root motion.
```gdscript
@onready var anim_tree: AnimationTree = $AnimationTree

func apply_root_motion() -> void:
    var motion := anim_tree.get_root_motion_position()
    global_position += motion
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
