---
name: godot-retro-2d-melee-attack
description: Godot Retro 2D Melee Attack
---

# Godot Retro 2D Melee Attack

## Core Concepts
Hitbox-based melee.
```gdscript
class_name MeleeAttack extends Area2D

@export var damage := 1
@export var lifetime := 0.25

func _ready() -> void:
    body_entered.connect(_on_hit)

func _on_hit(body: Node2D) -> void:
    if body.has_method("take_damage"):
        body.take_damage(damage)
    await get_tree().create_timer(lifetime).timeout
    queue_free()
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
