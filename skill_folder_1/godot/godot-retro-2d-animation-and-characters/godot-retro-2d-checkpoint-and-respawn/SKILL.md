---
name: godot-retro-2d-checkpoint-and-respawn
description: Godot Retro 2D Checkpoint And Respawn
---

# Godot Retro 2D Checkpoint And Respawn

## Core Concepts
Respawn logic.
```gdscript
class_name Checkpoint extends Area2D

signal activated(pos: Vector2)

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        activated.emit(global_position)
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
