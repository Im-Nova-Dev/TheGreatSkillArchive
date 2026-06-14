---
name: godot-shmup-scrolling-background
description: Godot Shmup Scrolling Background
---

# Godot Shmup Scrolling Background

## Core Concepts
Parallax starfield.
```gdscript
class_name StarField extends Node2D

@export var layers := 3
@export var speeds := [30.0, 60.0, 100.0]

func _process(delta: float) -> void:
    for i in range(get_child_count()):
        var layer := get_child(i) as Node2D
        layer.position.x -= speeds[i] * delta
        if layer.position.x < -320:
            layer.position.x += 640
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
