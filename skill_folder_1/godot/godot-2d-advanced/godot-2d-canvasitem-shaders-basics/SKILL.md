---
name: godot-2d-canvasitem-shaders-basics
description: Godot 2D Canvasitem Shaders Basics
---

# Godot 2D Canvasitem Shaders Basics

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Canvasitem Shaders Basics` in Godot 4.

## GDScript Example

Minimal 2D shader.
```glsl
shader_type canvas_item;

void fragment() {
    COLOR = texture(TEXTURE, UV) * vec4(1.0, 0.5, 0.8, 1.0);
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
