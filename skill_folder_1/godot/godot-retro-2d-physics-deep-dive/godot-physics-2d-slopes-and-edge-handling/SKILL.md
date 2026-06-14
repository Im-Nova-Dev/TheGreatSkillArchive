---
name: godot-physics-2d-slopes-and-edge-handling
description: Godot Physics 2D Slopes And Edge Handling
---

# Godot Physics 2D Slopes And Edge Handling

## Core Concepts
Slopes in 2D.
- Use `move_and_slide()` and let physics resolve.
- For steep slopes, check `is_on_floor() and get_last_slide_collision().get_normal().y < 0.7`.

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
