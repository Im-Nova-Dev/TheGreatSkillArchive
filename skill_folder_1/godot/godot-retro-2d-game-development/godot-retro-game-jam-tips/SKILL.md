---
name: godot-retro-game-jam-tips
description: Godot Retro Game Jam Tips
---

# Godot Retro Game Jam Tips

## Core Concepts

## Core Concepts
Succeeding in a game jam with retro 2D.
```gdscript
# GODOT GAME JAM CHECKLIST:
# 1. Core loop in first 2 hours.
# 2. Minimal scope: move, jump, one interaction.
# 3. Use Godot primitives (Rect2, Color, ArrayMesh).
# 4. Polish last: screen shake, juice, particles.
# 5. One-click export early.
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
