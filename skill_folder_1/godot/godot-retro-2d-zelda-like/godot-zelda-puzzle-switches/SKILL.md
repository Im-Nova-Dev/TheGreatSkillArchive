---
name: godot-zelda-puzzle-switches
description: Godot Zelda Puzzle Switches
---

# Godot Zelda Puzzle Switches

## Core Concepts
Toggle blocks.
```gdscript
class_name SwitchBlock extends TileMapLayer

@export var active := false

func toggle() -> void:
    active = not active
    set_collision_layer_value(1, not active)
    modulate.a = 0.5 if active else 1.0
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
