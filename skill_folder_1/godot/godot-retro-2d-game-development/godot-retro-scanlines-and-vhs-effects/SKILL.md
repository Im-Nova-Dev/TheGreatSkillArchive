---
name: godot-retro-scanlines-and-vhs-effects
description: Godot Retro Scanlines And Vhs Effects
---

# Godot Retro Scanlines And Vhs Effects

## Core Concepts

## Core Concepts
VHS/retro tape effects.
```glsl
shader_type canvas_item;

uniform float noise_strength := 0.05;
uniform float aberration := 1.0;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

void fragment() {
    vec2 uv = UV;
    // Chromatic aberration
    float r = texture(TEXTURE, uv + vec2(aberration / SCREEN_PIXEL_SIZE.x, 0.0)).r;
    float g = texture(TEXTURE, uv).g;
    float b = texture(TEXTURE, uv - vec2(aberration / SCREEN_PIXEL_SIZE.x, 0.0)).b;
    COLOR = vec4(r, g, b, 1.0);
    COLOR.rgb += random(uv + vec2(TIME, 0.0)) * noise_strength;
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
