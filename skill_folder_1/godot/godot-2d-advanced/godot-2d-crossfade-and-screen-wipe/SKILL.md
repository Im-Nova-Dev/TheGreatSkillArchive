---
name: godot-2d-crossfade-and-screen-wipe
description: Godot 2D Crossfade And Screen Wipe
---

# Godot 2D Crossfade And Screen Wipe

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Crossfade And Screen Wipe` in Godot 4.

## GDScript Example

Screen wipe shader.
```glsl
shader_type canvas_item;
uniform float progress: hint_range(0.0, 1.0) = 0.0;

void fragment() {
    float x = UV.x;
    COLOR = texture(TEXTURE, UV);
    if (x > progress) {
        COLOR.a -= smoothstep(progress, progress + 0.01, x);
    }
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
