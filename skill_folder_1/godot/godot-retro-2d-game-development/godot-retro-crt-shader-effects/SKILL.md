---
name: godot-retro-crt-shader-effects
description: Godot Retro Crt Shader Effects
---

# Godot Retro Crt Shader Effects

## Core Concepts

## Core Concepts
CRT screen simulation using shaders.
```glsl
shader_type canvas_item;

uniform float scanline_intensity := 0.1;
uniform float curvature := 0.1;
uniform float vignette := 0.3;

void fragment() {
    vec2 uv = UV;
    // Barrel distortion
    vec2 cc = uv - 0.5;
    float dist = dot(cc, cc);
    uv = uv + cc * dist * curvature;
    // Sample with warped UVs
    vec4 tex = texture(TEXTURE, uv);
    // Scanlines
    float scanline = sin(SCREEN_UV.y * 800.0) * scanline_intensity;
    tex.rgb -= scanline;
    // Vignette
    float vig = 1.0 - dist * vignette;
    tex.rgb *= vig;
    COLOR = tex;
}
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
