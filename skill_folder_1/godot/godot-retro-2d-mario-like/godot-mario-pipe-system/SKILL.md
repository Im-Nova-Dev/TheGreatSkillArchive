---
name: godot-mario-pipe-system
description: Godot Mario Pipe System
---

# Godot Mario Pipe System

## Core Concepts
Enter pipe warp.
```gdscript
class_name PipeWarp extends Area2D

@export var target := "World1-2"
@export var spawn := "pipe_spawn"

func _on_body_entered(body: Node2D) -> void:
    if body.name == "Player" and Input.is_action_pressed("down"):
        get_tree().change_scene_to_file("res://levels/%s.tscn" % target)
```

## Learning Path

1. **Foundation**: Study the core concepts.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand with more features.
4. **Production**: Make it a complete game.

## Common Pitfalls

- Scope creep: start tiny.
- Polishing before gameplay is locked.
- Forgetting pixel-snap camera.
- Over-engineering systems.

## Best Practices

- Keep one-click export ready.
- Profile 60 FPS target.
- Use Godot primitives (TileMap, AnimationPlayer).
- Ship one level, then iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b
- /r/godot
- itch.io devlogs
- Game jam communities
