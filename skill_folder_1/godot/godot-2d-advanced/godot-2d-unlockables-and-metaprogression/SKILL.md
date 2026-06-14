---
name: godot-2d-unlockables-and-metaprogression
description: Godot 2D Unlockables And Metaprogression
---

# Godot 2D Unlockables And Metaprogression

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Unlockables And Metaprogression` in Godot 4.

## GDScript Example

Unlock tracking.
```gdscript
class_name SaveData
extends Resource

@export var coins := 0
@export var unlocked_skins: Array[StringName] = []

func unlock_skin(skin: StringName) -> void:
    if skin not in unlocked_skins:
        unlocked_skins.append(skin)
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
