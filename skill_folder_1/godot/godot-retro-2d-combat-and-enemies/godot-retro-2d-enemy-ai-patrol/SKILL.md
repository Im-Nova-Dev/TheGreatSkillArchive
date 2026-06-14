---
name: godot-retro-2d-enemy-ai-patrol
description: Godot Retro 2D Enemy Ai Patrol
---

# Godot Retro 2D Enemy Ai Patrol

## Core Concepts
Basic patrol with waits.
```gdscript
class_name PatrolAI extends Node2D

@export var points: Array[Vector2]
@export var wait_time := 0.5
var index := 0

func _ready() -> void:
    global_position = points[0]

func _process(delta: float) -> void:
    var target := points[index]
    var dir := (target - global_position).normalized()
    global_position += dir * 40 * delta
    if global_position.distance_to(target) < 2:
        index = (index + 1) % points.size()
        await get_tree().create_timer(wait_time).timeout
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
