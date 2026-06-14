---
name: godot-datadriven-loot-tables
description: Godot Datadriven Loot Tables
---

# Godot Datadriven Loot Tables

## Core Concepts
Weighted drops.
```gdscript
class_name LootTable extends Resource
@export var entries: Array[LootEntry]

func roll() -> LootEntry:
    var total := 0.0
    for e in entries:
        total += e.weight
    var acc := 0.0
    var roll := randf() * total
    for e in entries:
        acc += e.weight
        if roll <= acc:
            return e
    return entries[-1]

class_name LootEntry extends Resource
@export var item: ItemData
@export var weight: float
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
