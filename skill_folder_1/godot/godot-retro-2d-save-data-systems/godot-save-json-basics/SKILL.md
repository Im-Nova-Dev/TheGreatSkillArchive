---
name: godot-save-json-basics
description: Godot Save Json Basics
---

# Godot Save Json Basics

## Core Concepts
Save/load with JSON.
```gdscript
class_name SaveSystem extends Node

const PATH := "user://save.json"

func save(data: Dictionary) -> void:
    FileAccess.store_string(PATH, JSON.stringify(data))

func load() -> Dictionary:
    if not FileAccess.file_exists(PATH):
        return {}
    return JSON.parse_string(FileAccess.get_file_as_string(PATH))
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
