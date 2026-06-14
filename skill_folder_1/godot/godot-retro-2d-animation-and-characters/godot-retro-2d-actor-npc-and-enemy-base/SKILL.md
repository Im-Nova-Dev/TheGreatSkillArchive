---
name: godot-retro-2d-actor-npc-and-enemy-base
description: Godot Retro 2D Actor Npc And Enemy Base
---

# Godot Retro 2D Actor Npc And Enemy Base

## Core Concepts
Shared actor base.
```gdscript
class_name Actor extends CharacterBody2D

@export var max_health := 3
@export var speed := 60.0
var health := max_health
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
