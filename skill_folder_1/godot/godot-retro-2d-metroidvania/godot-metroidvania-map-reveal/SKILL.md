---
name: godot-metroidvania-map-reveal
description: Godot Metroidvania Map Reveal
---

# Godot Metroidvania Map Reveal

## Core Concepts
Map reveal on room visit.
```gdscript
class_name MapManager extends Node

var visited_rooms: Array[String] = []

func mark_visited(room_id: String) -> void:
    if room_id not in visited_rooms:
        visited_rooms.append(room_id)
        save_map()
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
