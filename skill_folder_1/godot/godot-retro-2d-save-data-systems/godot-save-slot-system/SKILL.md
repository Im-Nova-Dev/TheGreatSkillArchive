---
name: godot-save-slot-system
description: Godot Save Slot System
---

# Godot Save Slot System

## Core Concepts
Multiple saves.
```gdscript
class_name SaveManager extends Node

func slot_path(slot: int) -> String:
    return "user://save_%d.json" % slot

func save_slot(slot: int, data: Dictionary) -> void:
    FileAccess.store_string(slot_path(slot), JSON.stringify(data))
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
