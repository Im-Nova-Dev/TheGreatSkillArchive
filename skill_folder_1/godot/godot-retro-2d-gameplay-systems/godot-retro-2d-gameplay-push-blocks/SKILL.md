---
name: godot-retro-2d-gameplay-push-blocks
description: Godot Retro 2D Gameplay Push Blocks
---

# Godot Retro 2D Gameplay Push Blocks

## Core Concepts
Pushable block puzzle.
```gdscript
class_name Pushable extends RigidBody2D

@export var push_force := 120.0
var held := false

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    if held:
        var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
        state.linear_velocity = dir * push_force
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
