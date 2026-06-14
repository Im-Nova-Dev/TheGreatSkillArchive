---
name: godot-learning-2d-physics-deep-dive
description: Godot Learning 2D Physics Deep Dive
---

# Godot Learning 2D Physics Deep Dive

## Core Concepts

## Core Concepts
Understanding Godot 2D physics.
```gdscript
# CharacterBody2D: Move and slide
# RigidBody2D: Physics simulation
# StaticBody2D: Static colliders
# Area2D: Overlap detection
# Use _physics_process for all physics queries.
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
