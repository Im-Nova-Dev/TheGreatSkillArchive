---
name: godot-zelda-screen-transitions
description: Godot Zelda Screen Transitions
---

# Godot Zelda Screen Transitions

## Core Concepts
Wrapping around screen edges (original Zelda).
```gdscript
func _physics_process(delta: float) -> void:
    move_and_slide()
    wrap_position()

func wrap_position() -> void:
    if global_position.x < 0:
        global_position.x = 256
    if global_position.x > 256:
        global_position.x = 0
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
