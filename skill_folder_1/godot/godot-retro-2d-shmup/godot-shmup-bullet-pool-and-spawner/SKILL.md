---
name: godot-shmup-bullet-pool-and-spawner
description: Godot Shmup Bullet Pool And Spawner
---

# Godot Shmup Bullet Pool And Spawner

## Core Concepts
Object pooling for bullets.
```gdscript
class_name BulletPool extends Node2D

var pool: Array[Node2D] = []

func get_bullet(scene: PackedScene) -> Node2D:
    for b in pool:
        if not b.visible:
            return b
    var b := scene.instantiate() as Node2D
    add_child(b)
    pool.append(b)
    return b
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
