---
name: godot-retro-2d-ranged-weapon
description: Godot Retro 2D Ranged Weapon
---

# Godot Retro 2D Ranged Weapon

## Core Concepts
Projectile pooling and firing.
```gdscript
class_name RetroGun extends Node2D

@export var bullet_scene: PackedScene
@export var fire_rate := 0.2
@export var bullet_speed := 240.0

var cooldown := 0.0

func _process(delta: float) -> void:
    cooldown -= delta
    if Input.is_action_pressed("shoot") and cooldown <= 0:
        fire()

func fire() -> void:
    cooldown = fire_rate
    var b := bullet_scene.instantiate() as Node2D
    b.global_position = global_position
    b.velocity = Vector2.RIGHT.rotated(rotation) * bullet_speed
    get_tree().current_scene.add_child(b)
    $MuzzleFlash.show()
    await get_tree().create_timer(0.05).timeout
    $MuzzleFlash.hide()
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
