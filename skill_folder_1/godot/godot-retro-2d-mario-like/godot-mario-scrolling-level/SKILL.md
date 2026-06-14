---
name: godot-mario-scrolling-level
description: Godot Mario Scrolling Level
---

# Godot Mario Scrolling Level

## Core Concepts
Side-scrolling level with camera follow.
```gdscript
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
    camera.limit_left = 0
    camera.limit_right = 3200
    camera.limit_top = -128
    camera.limit_bottom = 224
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
