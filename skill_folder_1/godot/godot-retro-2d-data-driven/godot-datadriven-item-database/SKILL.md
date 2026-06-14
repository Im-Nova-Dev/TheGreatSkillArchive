---
name: godot-datadriven-item-database
description: Godot Datadriven Item Database
---

# Godot Datadriven Item Database

## Core Concepts
Central item DB.
```gdscript
class_name ItemDB extends Node

var items: Dictionary = {}

func register(item: ItemData) -> void:
    items[item.id] = item

func get(id: String) -> ItemData:
    return items.get(id)
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
