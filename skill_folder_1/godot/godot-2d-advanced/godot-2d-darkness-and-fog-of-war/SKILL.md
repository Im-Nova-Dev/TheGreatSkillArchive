---
name: godot-2d-darkness-and-fog-of-war
description: Godot 2D Darkness And Fog Of War
---

# Godot 2D Darkness And Fog Of War

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Darkness And Fog Of War` in Godot 4.

## GDScript Example

Fog of war using ColorRect or shaders.
```glsl
shader_type canvas_item;

uniform vec2 player_pos;
uniform float radius := 120.0;

void fragment() {
    vec2 uv = SCREEN_UV * vec2(textureSize(TEXTURE, 0));
    float dist = distance(SCREEN_UV, player_pos / vec2(textureSize(TEXTURE, 0)));
    float visibility = smoothstep(radius, radius - 16.0, dist);
    COLOR = texture(TEXTURE, UV);
    COLOR.a *= visibility;
}
```

## Common Pitfalls

- Writing physics in `_process` instead of `_physics_process`.
- Forgetting typed `@onready` variables.
- Using global magic numbers everywhere.
- Hardcoding paths and not using exported resources.

## Best Practices

- Prefer typed GDScript with `get_class()` checks.
- Keep node references in `@onready` or inject them.
- Use resources for data, nodes for behavior.
- Profile before optimizing; avoid premature caching.

## Resources

- Official Godot 4 docs
- GDQuest and HeartBeast tutorials
- /r/godot and official Q&A
- Godot Asset Library
- YouTube: GYArray, GameDev Tavern, 41b
