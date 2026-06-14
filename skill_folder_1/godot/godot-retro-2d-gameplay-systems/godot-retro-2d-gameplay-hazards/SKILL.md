---
name: godot-retro-2d-gameplay-hazards
description: Godot Retro 2D Gameplay Hazards
---

# Godot Retro 2D Gameplay Hazards

## Core Concepts
Spikes and lava.
```gdscript
class_name Hazard extends Area2D

@export var damage := 1

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        body.take_damage(damage)
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
