---
name: godot-retro-2d-character-controller
description: Godot Retro 2D Character Controller
---

# Godot Retro 2D Character Controller

## Core Concepts
Unified character controller for retro games.
```gdscript
class_name RetroCharacter extends CharacterBody2D

@export var speed := 80.0
@export var jump := 220.0
@export var gravity := 600.0
@export var coyote_time := 0.12
@export var jump_buffer := 0.08

var coyote := 0.0
var buffer := 0.0

func _physics_process(delta: float) -> void:
    if is_on_floor():
        coyote = coyote_time
    else:
        coyote -= delta

    if Input.is_action_just_pressed("jump"):
        buffer = jump_buffer
    else:
        buffer -= delta

    if buffer > 0 and coyote > 0:
        velocity.y = -jump
        buffer = 0
        coyote = 0

    velocity.y += gravity * delta
    if not is_on_floor() and Input.is_action_just_released("jump") and velocity.y < 0:
        velocity.y *= 0.5
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    move_and_slide()
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
