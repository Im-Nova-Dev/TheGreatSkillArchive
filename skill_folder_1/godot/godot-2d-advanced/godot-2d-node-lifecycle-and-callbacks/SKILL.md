---
name: godot-2d-node-lifecycle-and-callbacks
description: Godot 2D Node Lifecycle And Callbacks
---

# Godot 2D Node Lifecycle And Callbacks

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Node Lifecycle And Callbacks` in Godot 4.

## GDScript Example

Understanding _ready vs _enter_tree vs _process.
```gdscript
func _enter_tree() -> void:
    print("Enter tree")

func _ready() -> void:
    print("Ready")

func _process(delta: float) -> void:
    pass
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
