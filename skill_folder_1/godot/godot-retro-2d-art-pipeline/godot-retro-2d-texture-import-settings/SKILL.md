---
name: godot-retro-2d-texture-import-settings
description: Godot Retro 2D Texture Import Settings
---

# Godot Retro 2D Texture Import Settings

## Core Concepts
Correct import for crisp pixels.
```gdscript
# Project settings, or per-texture via import dialog:
# - Filter: OFF (nearest neighbor)
# - Mipmaps: OFF
# - Compress: Lossless / VRAM compressed
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
