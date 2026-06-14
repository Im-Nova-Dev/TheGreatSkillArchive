---
name: godot-retro-2d-gameplay-moving-platforms
description: Godot Retro 2D Gameplay Moving Platforms
---

# Godot Retro 2D Gameplay Moving Platforms

## Core Concepts
Moving platforms with player parenting.
```gdscript
class_name MovingPlatform extends Node2D

@export var amplitude := 64.0
@export var speed := 1.0
var time := 0.0

func _physics_process(delta: float) -> void:
    time += delta * speed
    position.y = sin(time) * amplitude
    # Reparent rider temporarily
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
