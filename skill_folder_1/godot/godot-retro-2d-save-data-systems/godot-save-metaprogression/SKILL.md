---
name: godot-save-metaprogression
description: Godot Save Metaprogression
---

# Godot Save Metaprogression

## Core Concepts
Meta progression.
```gdscript
class_name MetaProgression extends Node

var unlocked_classes: Array[String] = []

func unlock(cls: String) -> void:
    if cls not in unlocked_classes:
        unlocked_classes.append(cls)
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
