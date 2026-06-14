---
name: godot-zelda-enemy-ai
description: Godot Zelda Enemy Ai
---

# Godot Zelda Enemy Ai

## Core Concepts
Simple patrol + aggro.
```gdscript
class_name ZeldaEnemy extends CharacterBody2D

@export var aggro_range := 80.0
@onready var player := get_tree().get_first_node_in_group("player")

func _physics_process(delta: float) -> void:
    if global_position.distance_to(player.global_position) < aggro_range:
        var dir := (player.global_position - global_position).normalized()
        velocity = dir * 40.0
    else:
        velocity = Vector2.ZERO
    move_and_slide()
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
