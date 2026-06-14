---
name: godot-genre-tutorial-stealth-game
description: Godot Genre Tutorial Stealth Game
---

# Godot Genre Tutorial Stealth Game

## Core Concepts

## Core Concepts
Vision cone and alert level.
```gdscript
class_name VisionCone extends Area2D

@export var fov := 45.0
@export var range := 120.0
@export var alert_level := 0.0

func see(target: Node2D) -> bool:
    var dir := (target.global_position - global_position).normalized()
    var angle := rad_to_deg(atan2(dir.y, dir.x))
    if abs(angle) < fov and global_position.distance_to(target.global_position) < range:
        return has_line_of_sight(target)
    return False
```

## Learning Path

1. **Foundation**: Study the concepts and examples.
2. **Implementation**: Rebuild the snippet in a Godot test project.
3. **Deep dive**: Adapt to your genre and art style.
4. **Production**: Polish and ship.

## Common Pitfalls

- Scoping too wide before core loop is fun.
- Hardcoding paths and magic numbers.
- Ignoring Godot’s built-in nodes (TileMap, AnimationPlayer).
- Skipping pixel-snap camera setup.

## Best Practices

- Use typed GDScript and `@onready`.
- Keep scenes modular and composable.
- Profile before optimizing.
- Ship a minimal vertical slice first.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b, KidsCanCode
- /r/godot
- itch.io devlogs
- Game jam communities
