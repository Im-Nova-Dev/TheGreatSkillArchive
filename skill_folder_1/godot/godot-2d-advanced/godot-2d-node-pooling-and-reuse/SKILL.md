---
name: godot-2d-node-pooling-and-reuse
description: Godot 2D Node Pooling And Reuse
---

# Godot 2D Node Pooling And Reuse

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Node Pooling And Reuse` in Godot 4.

## GDScript Example

Reduce allocations by pooling 2D nodes.
```gdscript
class_name BulletPool
extends Node2D

var pool: Array[Node2D] = []
var bullet_scene: PackedScene = preload("res://scenes/bullet.tscn")
var pool_size: int = 50

func _init(p_size: int = 50) -> void:
    pool_size = p_size
    for i in range(pool_size):
        var b := bullet_scene.instantiate() as Node2D
        b.visible = false
        add_child(b)
        pool.append(b)

func get_bullet() -> Node2D:
    for b in pool:
        if not b.visible:
            return b
    var b := bullet_scene.instantiate() as Node2D
    add_child(b)
    pool.append(b)
    return b

func release_bullet(b: Node2D) -> void:
    b.visible = false
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
