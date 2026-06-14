---
name: godot-retro-2d-gameplay-conveyor-belts
description: Godot Retro 2D Gameplay Conveyor Belts
---

# Godot Retro 2D Gameplay Conveyor Belts

## Core Concepts
Conveyor belt movement.
```gdscript
class_name ConveyorBelt extends Area2D

@export var speed := 60.0

func _physics_process(delta: float) -> void:
    for body in get_overlapping_bodies():
        if body.is_class("CharacterBody2D"):
            body.velocity.x += speed * delta
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
