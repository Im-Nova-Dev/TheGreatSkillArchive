---
name: godot-retro-2d-gameplay-powerup-system
description: Godot Retro 2D Gameplay Powerup System
---

# Godot Retro 2D Gameplay Powerup System

## Core Concepts
Temporary powerups.
```gdscript
class_name Powerup extends Area2D

@export var type := "speed"

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        match type:
            "speed":
                body.SPEED *= 1.4
                await get_tree().create_timer(8).timeout
                body.SPEED /= 1.4
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
