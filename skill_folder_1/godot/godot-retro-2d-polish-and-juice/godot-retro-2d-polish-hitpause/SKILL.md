---
name: godot-retro-2d-polish-hitpause
description: Godot Retro 2D Polish Hitpause
---

# Godot Retro 2D Polish Hitpause

## Core Concepts
Hitstop gives weight.
```gdscript
func hitstop(duration: float) -> void:
    var prev := Engine.time_scale
    Engine.time_scale = 0.0
    await get_tree().create_timer(duration).timeout
    Engine.time_scale = prev
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
