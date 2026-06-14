---
name: godot-physics-2d-area2d-sensors
description: Godot Physics 2D Area2D Sensors
---

# Godot Physics 2D Area2D Sensors

## Core Concepts
Sensors with Area2D.
```gdscript
func _on_area_2d_body_entered(body: Node2D) -> void:
    if body.name == "Player":
        emit_signal("player_entered")
```

## Learning Path

1. **Foundation**: Learn the core concepts.
2. **Implementation**: Build a focused demo.
3. **Deep dive**: Refine and extend.
4. **Production**: Integrate into your game.

## Common Pitfalls

- Hardcoding values everywhere.
- Writing monolithic scripts.
- Skipping physics and input setup first.
- Polishing too early.

## Best Practices

- Keep data in Resources.
- Keep logic in small nodes/components.
- Use typed GDScript consistently.
- Profile and optimize after gameplay is locked.

## Resources

- Godot 4 documentation
- GDQuest tutorials
- /r/godot
- itch.io devlogs
- Game jam communities
