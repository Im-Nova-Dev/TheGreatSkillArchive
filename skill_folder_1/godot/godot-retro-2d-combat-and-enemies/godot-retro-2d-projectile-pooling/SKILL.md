---
name: godot-retro-2d-projectile-pooling
description: Godot Retro 2D Projectile Pooling
---

# Godot Retro 2D Projectile Pooling

## Core Concepts
Object pool for bullets.
```gdscript
class_name BulletPool extends Node2D

var pool: Array[Node2D] = []
@export var bullet_scene: PackedScene
@export var initial := 100

func _ready() -> void:
    for i in range(initial):
        var b := bullet_scene.instantiate() as Node2D
        b.visible = false
        add_child(b)
        pool.append(b)

func spawn(pos: Vector2, dir: Vector2) -> Node2D:
    var b := pool.find(func(x): return not x.visible)
    if b == -1:
        b = bullet_scene.instantiate() as Node2D
        add_child(b)
        pool.append(b)
        b = pool.size() - 1
    var bullet := pool[b] as Node2D
    bullet.global_position = pos
    bullet.velocity = dir * 200
    bullet.visible = true
    return bullet
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
