---
name: godot-retro-2d-pixel-font-setup
description: Godot Retro 2D Pixel Font Setup
---

# Godot Retro 2D Pixel Font Setup

## Core Concepts
Bitmap fonts in Godot.
- Generate `.fnt` or `.xml` bitmap font from BMFont.
- Import as Font.
- Apply to `Label.add_theme_font_override("font", bitmap_font)`.

## GDScript
```gdscript
var font := load("res://fonts/pixel_font.tres")
$ScoreLabel.add_theme_font_override("font", font)
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
