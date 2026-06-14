---
name: godot-feedback-screen-flash
description: Godot Feedback Screen Flash
---

# Godot Feedback Screen Flash

## Core Concepts
Flash overlay.
```gdscript
extends ColorRect

func flash(color: Color, duration: float = 0.1) -> void:
    modulate.a = 0.6
    modulate = color
    var tween := create_tween()
    tween.tween_property(self, "modulate:a", 0.0, duration)
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
