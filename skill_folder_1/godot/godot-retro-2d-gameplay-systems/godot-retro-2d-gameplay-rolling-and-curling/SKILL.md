---
name: godot-retro-2d-gameplay-rolling-and-curling
description: Godot Retro 2D Gameplay Rolling And Curling
---

# Godot Retro 2D Gameplay Rolling And Curling

## Core Concepts
Roll as movement option.
```gdscript
func start_roll(duration: float) -> void:
    state = "roll"
    speed *= 1.8
    invuln = true
    await get_tree().create_timer(duration).timeout
    speed /= 1.8
    invuln = false
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
