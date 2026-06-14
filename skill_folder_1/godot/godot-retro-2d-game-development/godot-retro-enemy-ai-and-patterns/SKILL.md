---
name: godot-retro-enemy-ai-and-patterns
description: Godot Retro Enemy Ai And Patterns
---

# Godot Retro Enemy Ai And Patterns

## Core Concepts

## Core Concepts
Classic enemy behaviors.
```gdscript
class_name PatrolEnemy
extends CharacterBody2D

@export var patrol_points: Array[Vector2]
@export var speed := 60.0
var current_point := 0
var forward := true

func _physics_process(delta: float) -> void:
    var target := patrol_points[current_point]
    var dir := (target - global_position).normalized()
    velocity = dir * speed
    move_and_slide()
    if global_position.distance_to(target) < 2:
        advance_patrol()

func advance_patrol() -> void:
    if forward:
        current_point += 1
        if current_point >= patrol_points.size():
            forward = false
            current_point = patrol_points.size() - 2
    else:
        current_point -= 1
        if current_point < 0:
            forward = true
            current_point = 1
```

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4.
3. **Deep dive**: Explore engine workflows and retro-specific techniques.
4. **Production**: Polish and ship a finished retro 2D game.

## Common Pitfalls

- Over-filtering textures (destroy pixel crispness).
- Using modern 3D patterns instead of tile-based thinking.
- Forgetting to lock input during cutscenes/dialogue.
- Hardcoding animation speeds rather than using delta.

## Best Practices

- Use project settings to lock pixel-perfect rendering.
- Keep a single source of truth for game state.
- Organize scenes and resources in clear folder structures.
- Profile performance before optimizing.
- Ship early; polish later.

## Resources

- Official Godot 4 documentation and class reference
- GDQuest courses
- KidsCanCode and HeartBeast tutorials
- /r/godot and Godot Forums
- Game jam communities
- YouTube: GYArray, GameDev Tavern, 41b
- itch.io game dev forums
