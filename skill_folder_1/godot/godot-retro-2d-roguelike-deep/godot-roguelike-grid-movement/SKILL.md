---
name: godot-roguelike-grid-movement
description: Godot Roguelike Grid Movement
---

# Godot Roguelike Grid Movement

## Core Concepts
Turn-based grid movement.
```gdscript
class_name GridMover extends Node2D

@export var move_delay := 0.15
var can_move := true

func try_move(dir: Vector2i) -> void:
    if not can_move: return
    var target := (owner as Node2D).global_position + dir * 16
    if is_walkable(target):
        (owner as Node2D).global_position = target
        can_move = false
        await get_tree().create_timer(move_delay).timeout
        can_move = true
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
