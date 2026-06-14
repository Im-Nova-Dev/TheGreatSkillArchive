---
name: godot-2d-bootstrap-and-game-manager
description: Godot 2D Bootstrap And Game Manager
---

# Godot 2D Bootstrap And Game Manager

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Bootstrap And Game Manager` in Godot 4.

## GDScript Example

Game manager skeleton.
```gdscript
class_name GameManager
extends Node

signal state_changed(state: StringName)

enum State { MENU, PLAYING, PAUSED, GAME_OVER }
var state := State.MENU

func change_state(next: State) -> void:
    state = next
    state_changed.emit(State.keys()[next])
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
