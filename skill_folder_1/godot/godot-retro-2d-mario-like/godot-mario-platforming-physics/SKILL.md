---
name: godot-mario-platforming-physics
description: Godot Mario Platforming Physics
---

# Godot Mario Platforming Physics

## Core Concepts
Acceleration-based Mario physics.
```gdscript
extends CharacterBody2D

const ACCEL := 1200.0
const FRICTION := 800.0
const MAX_SPEED := 160.0
const JUMP := 260.0

func _physics_process(delta: float) -> void:
    var input_x := Input.get_axis("left", "right")
    if input_x != 0:
        velocity.x = move_toward(velocity.x, input_x * MAX_SPEED, ACCEL * delta)
    else:
        velocity.x = move_toward(velocity.x, 0, FRICTION * delta)
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -JUMP
    if not is_on_floor() and Input.is_action_just_released("jump") and velocity.y < 0:
        velocity.y *= 0.5
    velocity.y += 980 * delta
    move_and_slide()
```

## Learning Path

1. **Foundation**: Study the core concepts.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand with more features.
4. **Production**: Make it a complete game.

## Common Pitfalls

- Scope creep: start tiny.
- Polishing before gameplay is locked.
- Forgetting pixel-snap camera.
- Over-engineering systems.

## Best Practices

- Keep one-click export ready.
- Profile 60 FPS target.
- Use Godot primitives (TileMap, AnimationPlayer).
- Ship one level, then iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b
- /r/godot
- itch.io devlogs
- Game jam communities
