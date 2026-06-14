---
name: godot-2d-light2d-and-shadows-advanced
description: Godot 2D Light2D And Shadows Advanced
---

# Godot 2D Light2D And Shadows Advanced

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Light2D And Shadows Advanced` in Godot 4.

## GDScript Example

2D shadow setup.
```gdscript
@onready var light := $PointLight2D
@onready var shadow := $LightOccluder2D

func update_light() -> void:
    light.position = global_position
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
