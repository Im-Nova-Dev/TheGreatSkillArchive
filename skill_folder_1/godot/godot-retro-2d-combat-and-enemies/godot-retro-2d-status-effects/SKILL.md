---
name: godot-retro-2d-status-effects
description: Godot Retro 2D Status Effects
---

# Godot Retro 2D Status Effects

## Core Concepts
Burn and slow statuses.
```gdscript
class_name StatusEffect extends Resource

@export var duration := 2.0
@export var tick_rate := 0.5
var applied_to: Node2D

func apply(target: Node2D) -> void:
    applied_to = target

func tick() -> void:
    pass

func clear() -> void:
    pass
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
