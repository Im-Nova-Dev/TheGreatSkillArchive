---
name: godot-optimization-2d-particles
description: Godot Optimization 2D Particles
---

# Godot Optimization 2D Particles

## Core Concepts
Particle limits.
- Use one GPUParticles2D per effect type.
- Limit lifetime and amount.
- Prefer curves over many tiny emitters.

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
