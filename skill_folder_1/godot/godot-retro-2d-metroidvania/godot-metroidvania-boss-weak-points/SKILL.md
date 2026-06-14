---
name: godot-metroidvania-boss-weak-points
description: Godot Metroidvania Boss Weak Points
---

# Godot Metroidvania Boss Weak Points

## Core Concepts
Weak point targeting.
```gdscript
class_name BossWeakPoint extends Area2D

@export var boss: Node2D

func _on_body_entered(body: Node2D) -> void:
    if body.name == "PlayerProjectile":
        boss.take_damage(3)
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
