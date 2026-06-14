---
name: godot-contra-platformer-physics
description: Godot Contra Platformer Physics
---

# Godot Contra Platformer Physics

## Core Concepts
Run-and-gun movement.
```gdscript
extends CharacterBody2D

const RUN_SPEED := 200.0
const JUMP := 300.0
const GRAVITY := 900.0

func _physics_process(delta: float) -> void:
    velocity.y += GRAVITY * delta
    velocity.x = Input.get_axis("left", "right") * RUN_SPEED
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -JUMP
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
