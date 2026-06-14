---
name: godot-2d-decals-and-dirt
description: Godot 2D Decals And Dirt
---

# Godot 2D Decals And Dirt

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Decals And Dirt` in Godot 4.

## GDScript Example

Simple decal pattern.
```gdscript
class_name Decal2D
extends Node2D

@export var texture: Texture2D

func _ready() -> void:
    var sprite := Sprite2D.new()
    sprite.texture = texture
    add_child(sprite)
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
