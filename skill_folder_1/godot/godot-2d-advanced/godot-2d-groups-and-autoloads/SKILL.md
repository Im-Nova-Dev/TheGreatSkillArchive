---
name: godot-2d-groups-and-autoloads
description: Godot 2D Groups And Autoloads
---

# Godot 2D Groups And Autoloads

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Groups And Autoloads` in Godot 4.

## GDScript Example

Group-based lookup and autoload use cases.
```gdscript
# Add enemy to group
add_to_group("enemies")

# Find all enemies later
get_tree().get_nodes_in_group("enemies")
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
