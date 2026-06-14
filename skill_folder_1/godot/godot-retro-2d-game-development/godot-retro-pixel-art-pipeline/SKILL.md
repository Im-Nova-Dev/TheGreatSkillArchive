---
name: godot-retro-pixel-art-pipeline
description: Godot Retro Pixel Art Pipeline
---

# Godot Retro Pixel Art Pipeline

## Core Concepts

## Core Concepts
Setting up a proper pixel art workflow in Godot 4.
```gdscript
# Project settings for pixel art:
# - Rendering > Textures > Canvas Textures > Use Filter: OFF
# - Viewport > Keep Aspect: Enabled, Aspect: 1 (square pixels)
# - Window > Size: e.g. 320x180 for 16:9 pixel games
# - Import textures with Filter disabled and no mipmaps
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
