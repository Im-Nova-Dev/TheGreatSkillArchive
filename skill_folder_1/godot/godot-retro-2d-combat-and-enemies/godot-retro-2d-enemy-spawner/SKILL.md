---
name: godot-retro-2d-enemy-spawner
description: Godot Retro 2D Enemy Spawner
---

# Godot Retro 2D Enemy Spawner

## Core Concepts
Wave-based spawner.
```gdscript
class_name WaveSpawner extends Node2D

@export var enemy_types: Array[PackedScene]
@export var waves: Array[Wave]

var alive := 0

func spawn_wave(index: int) -> void:
    var wave := waves[index]
    for entry in wave.enemies:
        for i in range(entry.count):
            var enemy := entry.scene.instantiate() as Node2D
            enemy.global_position = global_position
            get_tree().current_scene.add_child(enemy)
            alive += 1

class_name Wave extends Resource
@export var enemies: Array[EnemyEntry]

class_name EnemyEntry extends Resource
@export var scene: PackedScene
@export var count: int
```

## Common Pitfalls

- Overcomplicating scope before the core loop is confirmed fun.
- Polishing visuals before gameplay feels right.
- Missing one-click export workflow until submit day.
- Ignoring Godot’s built-in TileMap and Animation tools.

## Best Practices

- Scope to one screen first.
- Profile every build.
- Ship one polished level instead of three rough ones.
- Keep art in consistent palette and resolution.

## Resources

- Godot 4 class reference
- GDQuest retro/2D tutorials
- /r/godot
- Game jam communities (Ludum Dare, GMTK)
- itch.io devlogs
