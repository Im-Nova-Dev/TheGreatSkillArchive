---
name: godot-2d-trail-and-afterimage
description: Godot 2D Trail And Afterimage
---

# Godot 2D Trail And Afterimage

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Trail And Afterimage` in Godot 4.

## GDScript Example

Afterimage trail.
```gdscript
class_name AfterImage2D
extends Node2D

@export var interval := 0.05
@export var life := 0.3
var timer := 0.0
var parent_ref: Node2D

func _process(delta: float) -> void:
    timer -= delta
    if timer <= 0:
        spawn_image()
        timer = interval

func spawn_image() -> void:
    var sprite := Sprite2D.new()
    sprite.texture = parent_ref.texture
    sprite.global_position = parent_ref.global_position
    sprite.modulate.a = 0.5
    add_child(sprite)
    await get_tree().create_timer(life).timeout
    sprite.queue_free()
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
