---
name: godot-retro-2d-gameplay-slopes-and-sliding
description: Godot Retro 2D Gameplay Slopes And Sliding
---

# Godot Retro 2D Gameplay Slopes And Sliding

## Core Concepts
Slide down steep slopes.
```gdscript
class_name Player extends CharacterBody2D

var on_slope := false

func _physics_process(delta: float) -> void:
    if on_slope and velocity.y == 0:
        slide_down_slope()
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
