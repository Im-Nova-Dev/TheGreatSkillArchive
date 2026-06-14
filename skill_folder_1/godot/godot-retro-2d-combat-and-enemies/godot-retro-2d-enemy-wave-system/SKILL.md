---
name: godot-retro-2d-enemy-wave-system
description: Godot Retro 2D Enemy Wave System
---

# Godot Retro 2D Enemy Wave System

## Core Concepts
Wave configuration and escalation.
```gdscript
class_name WaveManager extends Node2D

@export var waves: Array[WaveConfig]
var current := 0

func next_wave() -> void:
    var config := waves[current]
    spawn_group(config.patrol_count)
    spawn_group(config.chaser_count)
    current += 1

class_name WaveConfig extends Resource
@export var patrol_count := 3
@export var chaser_count := 1
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
