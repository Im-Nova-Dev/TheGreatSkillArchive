---
name: godot-retro-2d-item-pickup-animation
description: Godot Retro 2D Item Pickup Animation
---

# Godot Retro 2D Item Pickup Animation

## Core Concepts
Bounce and fade pickup.
```gdscript
class_name RetroPickup extends Area2D

func _ready() -> void:
    var t := create_tween()
    t.set_loops()
    t.tween_property(self, "position:y", position.y - 6, 0.5)
    t.tween_property(self, "position:y", position.y + 6, 0.5)
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
