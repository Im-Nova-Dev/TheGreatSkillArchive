---
name: godot-2d-obstacle-course-design
description: Godot 2D Obstacle Course Design
---

# Godot 2D Obstacle Course Design

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Obstacle Course Design` in Godot 4.

## GDScript Example

Obstacle course with moving platforms.
```gdscript
extends Node2D

@export var amplitude := 64.0
@export var frequency := 1.0
var time := 0.0

func _process(delta: float) -> void:
    time += delta * frequency
    $Platform.position.y = sin(time) * amplitude
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
