---
name: godot-2d-scene-instantiation-and-initialization
description: Godot 2D Scene Instantiation And Initialization
---

# Godot 2D Scene Instantiation And Initialization

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Scene Instantiation And Initialization` in Godot 4.

## GDScript Example

Scene instantiation patterns.
```gdscript
var scene := preload("res://scenes/enemy.tscn") as PackedScene
var enemy := scene.instantiate()
enemy.global_position = spawn_point.global_position
add_child(enemy)
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
