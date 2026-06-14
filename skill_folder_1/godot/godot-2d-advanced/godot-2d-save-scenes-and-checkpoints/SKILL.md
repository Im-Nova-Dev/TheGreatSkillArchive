---
name: godot-2d-save-scenes-and-checkpoints
description: Godot 2D Save Scenes And Checkpoints
---

# Godot 2D Save Scenes And Checkpoints

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Save Scenes And Checkpoints` in Godot 4.

## GDScript Example

Checkpoint manager.
```gdscript
class_name CheckpointManager
extends Node

var last_checkpoint: Vector2

func set_checkpoint(pos: Vector2) -> void:
    last_checkpoint = pos

func respawn_player(player: Node2D) -> void:
    player.global_position = last_checkpoint
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
