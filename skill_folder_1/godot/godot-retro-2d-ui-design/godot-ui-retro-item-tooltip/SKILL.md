---
name: godot-ui-retro-item-tooltip
description: Godot Ui Retro Item Tooltip
---

# Godot Ui Retro Item Tooltip

## Core Concepts
Tooltip follow mouse.
```gdscript
func _process(delta: float) -> void:
    global_position = get_global_mouse_position() + Vector2(12, 12)
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
