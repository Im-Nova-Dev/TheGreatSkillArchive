---
name: godot-optimization-2d-memory
description: Godot Optimization 2D Memory
---

# Godot Optimization 2D Memory

## Core Concepts
Avoiding GC spikes.
- Pool bullets and particles.
- Cache node references, avoid get_node in hot paths.
- Use typed arrays.

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
