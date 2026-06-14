---
name: godot-feedback-screen-shake
description: Godot Feedback Screen Shake
---

# Godot Feedback Screen Shake

## Core Concepts
Camera shake.
```gdscript
extends Camera2D

func shake(amount: float, time: float) -> void:
    var init := offset
    var t := 0.0
    while t < time:
        offset = Vector2(randf() - 0.5, randf() - 0.5) * amount
        await get_tree().process_frame
        t += get_process_delta_time()
    offset = init
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
