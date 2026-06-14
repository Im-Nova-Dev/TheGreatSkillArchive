---
name: godot-roguelike-dungeon-generation-bsp
description: Godot Roguelike Dungeon Generation Bsp
---

# Godot Roguelike Dungeon Generation Bsp

## Core Concepts
Binary space partitioning.
```gdscript
class_name BSPTree
var rect: Rect2
var left: BSPTree
var right: BSPTree
var room: Rect2

func split(min_size: int) -> bool:
    if left and right: return true
    var split_h := randf() < 0.5
    if split_h and rect.size.y >= min_size * 2 + 1:
        var y := randi_range(rect.position.y + min_size, rect.end.y - min_size - 1)
        left = BSPTree.new(Rect2(rect.position, Vector2(rect.size.x, y - rect.position.y)))
        right = BSPTree.new(Rect2(Vector2(rect.position.x, y), Vector2(rect.size.x, rect.end.y - y)))
    elif rect.size.x >= min_size * 2 + 1:
        var x := randi_range(rect.position.x + min_size, rect.end.x - min_size - 1)
        left = BSPTree.new(Rect2(rect.position, Vector2(x - rect.position.x, rect.size.y)))
        right = BSPTree.new(Rect2(Vector2(x, rect.position.y), Vector2(rect.end.x - x, rect.size.y)))
    else:
        return false
    return left.split(min_size) and right.split(min_size)
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
