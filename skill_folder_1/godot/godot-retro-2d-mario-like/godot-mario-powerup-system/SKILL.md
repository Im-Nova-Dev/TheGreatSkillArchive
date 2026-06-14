---
name: godot-mario-powerup-system
description: Godot Mario Powerup System
---

# Godot Mario Powerup System

## Core Concepts
Mushroom and flower powerups.
```gdscript
class_name Powerup extends Area2D

@export var type := "mushroom"

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        if type == "mushroom":
            body.grow()
        elif type == "flower":
            body.gain_fire_ability()
        queue_free()
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
