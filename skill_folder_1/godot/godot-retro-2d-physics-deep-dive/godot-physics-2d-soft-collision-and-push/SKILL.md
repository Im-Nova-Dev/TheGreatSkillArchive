---
name: godot-physics-2d-soft-collision-and-push
description: Godot Physics 2D Soft Collision And Push
---

# Godot Physics 2D Soft Collision And Push

## Core Concepts
Gentle push for overlapping soft bodies.
```gdscript
func push_away(others: Array[Node2D]) -> void:
    for other in others:
        var dir := (global_position - other.global_position).normalized()
        global_position += dir * 1.5
```

## Learning Path

1. **Foundation**: Learn the core concepts.
2. **Implementation**: Build a focused demo.
3. **Deep dive**: Refine and extend.
4. **Production**: Integrate into your game.

## Common Pitfalls

- Hardcoding values everywhere.
- Writing monolithic scripts.
- Skipping physics and input setup first.
- Polishing too early.

## Best Practices

- Keep data in Resources.
- Keep logic in small nodes/components.
- Use typed GDScript consistently.
- Profile and optimize after gameplay is locked.

## Resources

- Godot 4 documentation
- GDQuest tutorials
- /r/godot
- itch.io devlogs
- Game jam communities
