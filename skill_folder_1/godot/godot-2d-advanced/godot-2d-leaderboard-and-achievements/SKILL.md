---
name: godot-2d-leaderboard-and-achievements
description: Godot 2D Leaderboard And Achievements
---

# Godot 2D Leaderboard And Achievements

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Leaderboard And Achievements` in Godot 4.

## GDScript Example

Leaderboard stub.
```gdscript
class_name Leaderboard
extends Node

var scores: Array[int] = []

func add_score(score: int) -> void:
    scores.append(score)
    scores.sort()
    scores.reverse()
    if scores.size() > 10:
        scores.resize(10)
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
