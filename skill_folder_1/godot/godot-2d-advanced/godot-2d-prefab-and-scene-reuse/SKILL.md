---
name: godot-2d-prefab-and-scene-reuse
description: Godot 2D Prefab And Scene Reuse
---

# Godot 2D Prefab And Scene Reuse

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Prefab And Scene Reuse` in Godot 4.

## GDScript Example

Run-time instancing patterns.
```gdscript
extends Node2D

@export var base_scene: PackedScene

func spawn_at(pos: Vector2) -> Node2D:
    var node := base_scene.instantiate() as Node2D
    node.global_position = pos
    get_tree().current_scene.add_child(node)
    return node
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
