---
name: godot-retro-2d-crt-post-process
description: Godot Retro 2D Crt Post Process
---

# Godot Retro 2D Crt Post Process

## Core Concepts
CRT shader applied globally.
```glsl
shader_type canvas_item;
uniform float scan := 0.08;
uniform float curve := 0.04;

void fragment() {
    vec2 uv = UV;
    vec2 cc = uv - 0.5;
    uv += cc * dot(cc, cc) * curve;
    vec4 col = texture(TEXTURE, uv);
    col.rgb -= sin(SCREEN_UV.y * 600.0) * scan;
    COLOR = col;
}
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
