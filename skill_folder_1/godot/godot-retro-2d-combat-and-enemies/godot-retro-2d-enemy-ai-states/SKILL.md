---
name: godot-retro-2d-enemy-ai-states
description: Godot Retro 2D Enemy Ai States
---

# Godot Retro 2D Enemy Ai States

## Core Concepts
Simple state enum.
```gdscript
class_name Enemy extends CharacterBody2D

enum State { IDLE, PATROL, CHASE, ATTACK }
var state := State.IDLE

func _physics_process(delta: float) -> void:
    match state:
        State.IDLE:
            pass
        State.PATROL:
            patrol(delta)
        State.CHASE:
            chase(delta)
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
