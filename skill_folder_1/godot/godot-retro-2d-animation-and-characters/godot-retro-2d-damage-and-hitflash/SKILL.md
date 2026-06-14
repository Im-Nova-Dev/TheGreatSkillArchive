---
name: godot-retro-2d-damage-and-hitflash
description: Godot Retro 2D Damage And Hitflash
---

# Godot Retro 2D Damage And Hitflash

## Core Concepts
Classic damage feedback.
```gdscript
class_name HurtBox extends Area2D

signal hurt(amount: int)

func take_damage(amount: int) -> void:
    emit_signal("hurt", amount)
    modulate = Color.RED
    await get_tree().create_timer(0.08).timeout
    modulate = Color.WHITE
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
