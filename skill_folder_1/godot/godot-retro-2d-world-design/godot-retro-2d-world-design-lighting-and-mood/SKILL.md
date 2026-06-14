---
name: godot-retro-2d-world-design-lighting-and-mood
description: Godot Retro 2D World Design Lighting And Mood
---

# Godot Retro 2D World Design Lighting And Mood

## Core Concepts
Retro lighting using 2D point lights.
```gdscript
@onready var torch := $PointLight2D

func toggle_torch(active: bool) -> void:
    torch.visible = active
    if active:
        torch.energy = 1.2
        torch.texture_scale = 0.8
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
