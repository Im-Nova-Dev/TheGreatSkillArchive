---
name: godot-shmup-player-movement
description: Godot Shmup Player Movement
---

# Godot Shmup Player Movement

## Core Concepts
Fighter movement with bounds.
```gdscript
extends CharacterBody2D

const SPEED := 200.0
const FOCUS_SPEED := 80.0

func _physics_process(delta: float) -> void:
    var speed := FOCUS_SPEED if Input.is_action_pressed("focus") else SPEED
    var dir := Input.get_vector("left", "right", "up", "down")
    velocity = dir * speed
    move_and_slide()
    global_position = global_position.clamp(Vector2(0,0), Vector2(320, 240))
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
