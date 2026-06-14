---
name: godot-retro-procedural-generation
description: Godot Retro Procedural Generation
---

# Godot Retro Procedural Generation

## Core Concepts

## Core Concepts
Simple procedural dungeon generation.
```gdscript
class_name DungeonGenerator
extends Node2D

func generate(width: int, height: int) -> Array[Vector2i]:
    var floor_tiles: Array[Vector2i] = []
    for x in range(width):
        for y in range(height):
            if randf() > 0.3:
                floor_tiles.append(Vector2i(x, y))
    return floor_tiles
```

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4.
3. **Deep dive**: Explore engine workflows and retro-specific techniques.
4. **Production**: Polish and ship a finished retro 2D game.

## Common Pitfalls

- Over-filtering textures (destroy pixel crispness).
- Using modern 3D patterns instead of tile-based thinking.
- Forgetting to lock input during cutscenes/dialogue.
- Hardcoding animation speeds rather than using delta.

## Best Practices

- Use project settings to lock pixel-perfect rendering.
- Keep a single source of truth for game state.
- Organize scenes and resources in clear folder structures.
- Profile performance before optimizing.
- Ship early; polish later.

## Resources

- Official Godot 4 documentation and class reference
- GDQuest courses
- KidsCanCode and HeartBeast tutorials
- /r/godot and Godot Forums
- Game jam communities
- YouTube: GYArray, GameDev Tavern, 41b
- itch.io game dev forums
