---
name: godot-metroidvania-save-rooms
description: Godot Metroidvania Save Rooms
---

# Godot Metroidvania Save Rooms

## Core Concepts
Save station logic.
```gdscript
class_name SaveRoom extends Area2D

signal saved

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        Game.last_save = global_position
        saved.emit()
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
