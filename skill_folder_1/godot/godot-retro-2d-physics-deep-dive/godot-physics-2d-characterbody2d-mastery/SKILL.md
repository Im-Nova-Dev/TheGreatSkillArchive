---
name: godot-physics-2d-characterbody2d-mastery
description: Godot Physics 2D Characterbody2D Mastery
---

# Godot Physics 2D Characterbody2D Mastery

## Core Concepts
Complete CharacterBody2D setup.
```gdscript
extends CharacterBody2D

const SPEED := 120.0
const JUMP := 240.0
const GRAVITY := 600.0

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y += GRAVITY * delta
    velocity.x = Input.get_axis("left", "right") * SPEED
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -JUMP
    move_and_slide()
```

## Learning Path

1. **Foundation**: Learn the core concepts.
2. **Implementation**: Build a focused demo.
3. **Deep dive**: Refine and extend.
4. **Production**: Integrate into your game.

## Common Pitfalls

- Hardcoding values everywhere.
- Writing monolithic scripts.
- Skipping physics and input setup first.
- Polishing too early.

## Best Practices

- Keep data in Resources.
- Keep logic in small nodes/components.
- Use typed GDScript consistently.
- Profile and optimize after gameplay is locked.

## Resources

- Godot 4 documentation
- GDQuest tutorials
- /r/godot
- itch.io devlogs
- Game jam communities
