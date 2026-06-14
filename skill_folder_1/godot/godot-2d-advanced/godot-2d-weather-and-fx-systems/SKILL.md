---
name: godot-2d-weather-and-fx-systems
description: Godot 2D Weather And Fx Systems
---

# Godot 2D Weather And Fx Systems

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Weather And Fx Systems` in Godot 4.

## GDScript Example

Weather state controller.
```gdscript
class_name WeatherManager
extends Node2D

@export var rain := false

func set_rain(active: bool) -> void:
    rain = active
    $RainParticles.emitting = active
    if active:
        $RainAudio.play()
    else:
        $RainAudio.stop()
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
