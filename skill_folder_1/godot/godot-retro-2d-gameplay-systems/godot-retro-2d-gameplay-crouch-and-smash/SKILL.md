---
name: godot-retro-2d-gameplay-crouch-and-smash
description: Godot Retro 2D Gameplay Crouch And Smash
---

# Godot Retro 2D Gameplay Crouch And Smash

## Core Concepts
Crouch and smash block.
```gdscript
func _physics_process(delta: float) -> void:
    if Input.is_action_pressed("crouch"):
        collision_shape.shape.height = 8
    else:
        collision_shape.shape.height = 16
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
