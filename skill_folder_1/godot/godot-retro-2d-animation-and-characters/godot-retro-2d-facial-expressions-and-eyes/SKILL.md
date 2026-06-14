---
name: godot-retro-2d-facial-expressions-and-eyes
description: Godot Retro 2D Facial Expressions And Eyes
---

# Godot Retro 2D Facial Expressions And Eyes

## Core Concepts
Procedural blinking.
```gdscript
class_name BlinkController extends Node

@onready var eyes: Array[Node2D] = [$LeftEye, $RightEye]
var next_blink := 2.0

func _process(delta: float) -> void:
    next_blink -= delta
    if next_blink <= 0:
        blink()
        next_blink = 2 + randf() * 3

func blink() -> void:
    for eye in eyes:
        eye.scale.y = 0.1
        await get_tree().create_timer(0.1).timeout
        eye.scale.y = 1.0
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
