---
name: godot-retro-2d-gameplay-bump-combat
description: Godot Retro 2D Gameplay Bump Combat
---

# Godot Retro 2D Gameplay Bump Combat

## Core Concepts
Mario-style bump combat.
```gdscript
func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        var dir := (global_position - body.global_position).normalized()
        # Player bounces up
        if body is CharacterBody2D:
            body.velocity = Vector2.UP * 180 + dir * 90
        # Enemy takes damage
        take_damage(1)
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
