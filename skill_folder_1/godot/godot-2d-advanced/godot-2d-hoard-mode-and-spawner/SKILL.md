---
name: godot-2d-hoard-mode-and-spawner
description: Godot 2D Hoard Mode And Spawner
---

# Godot 2D Hoard Mode And Spawner

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Hoard Mode And Spawner` in Godot 4.

## GDScript Example

Spawner example.
```gdscript
class_name EnemySpawner
extends Node2D

@export var enemy_scene: PackedScene
@export var max_enemies: int = 20
@export var spawn_radius: float = 300.0

var spawned: Array[Node2D] = []

func _process(delta: float) -> void:
    if spawned.size() < max_enemies:
        spawn_enemy()

func spawn_enemy() -> void:
    var enemy := enemy_scene.instantiate() as Node2D
    var angle := randf() * TAU
    var pos := Vector2(cos(angle), sin(angle)) * spawn_radius
    enemy.global_position = global_position + pos
    get_parent().add_child(enemy)
    spawned.append(enemy)
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
