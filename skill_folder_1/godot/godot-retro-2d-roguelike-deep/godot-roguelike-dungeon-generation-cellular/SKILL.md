---
name: godot-roguelike-dungeon-generation-cellular
description: Godot Roguelike Dungeon Generation Cellular
---

# Godot Roguelike Dungeon Generation Cellular

## Core Concepts
Cellular automata caves.
```gdscript
func cellular_automata(width: int, height: int, iterations: int) -> Array[Array]:
    var grid := []
    for x in range(width):
        grid.append([])
        for y in range(height):
            grid[x].append(1 if randf() < 0.45 else 0)
    for i in range(iterations):
        smooth(grid, width, height)
    return grid
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
