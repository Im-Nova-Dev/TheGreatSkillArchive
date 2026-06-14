---
name: godot-2d-background-and-parallax
description: Godot 2D Background And Parallax
---

# Godot 2D Background And Parallax

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Background And Parallax` in Godot 4.

## GDScript Example

Parallax background pattern.
```gdscript
class_name ParallaxLayer2D
extends Node2D

@export var speed := 0.5

func _process(delta: float) -> void:
    position.x -= speed * 60.0 * delta
    if position.x <= -1920:
        position.x += 1920
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
