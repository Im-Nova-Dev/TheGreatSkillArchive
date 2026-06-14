---
name: godot-genre-tutorial-dungeon-crawler
description: Godot Genre Tutorial Dungeon Crawler
---

# Godot Genre Tutorial Dungeon Crawler

## Core Concepts

## Core Concepts
Grid movement and FOV.
```gdscript
class_name DungeonCrawler extends Node2D

func turn_based_move(entity: Node2D, dir: Vector2i) -> void:
    var target := entity.grid_pos + dir
    if not is_blocked(target):
        entity.grid_pos = target
        entity.global_position = grid_to_world(target)
        emit_signal("turn_taken")
```

## Learning Path

1. **Foundation**: Study the concepts and examples.
2. **Implementation**: Rebuild the snippet in a Godot test project.
3. **Deep dive**: Adapt to your genre and art style.
4. **Production**: Polish and ship.

## Common Pitfalls

- Scoping too wide before core loop is fun.
- Hardcoding paths and magic numbers.
- Ignoring Godot’s built-in nodes (TileMap, AnimationPlayer).
- Skipping pixel-snap camera setup.

## Best Practices

- Use typed GDScript and `@onready`.
- Keep scenes modular and composable.
- Profile before optimizing.
- Ship a minimal vertical slice first.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b, KidsCanCode
- /r/godot
- itch.io devlogs
- Game jam communities
