---
name: godot-retro-2d-enemy-ai-chase
description: Godot Retro 2D Enemy Ai Chase
---

# Godot Retro 2D Enemy Ai Chase

## Core Concepts
Chase when player is nearby.
```gdscript
extends Node2D

@export var chase_range := 120.0
@onready var player := get_tree().get_first_node_in_group("player")

func _process(delta: float) -> void:
    if global_position.distance_to(player.global_position) < chase_range:
        var dir := (player.global_position - global_position).normalized()
        global_position += dir * 60 * delta
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
