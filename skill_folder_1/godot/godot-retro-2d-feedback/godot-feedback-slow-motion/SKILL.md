---
name: godot-feedback-slow-motion
description: Godot Feedback Slow Motion
---

# Godot Feedback Slow Motion

## Core Concepts
Slow-mo.
```gdscript
func slow_mo(scale: float, time: float) -> void:
    var prev := Engine.time_scale
    Engine.time_scale = scale
    await get_tree().create_timer(time).timeout
    Engine.time_scale = prev
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
