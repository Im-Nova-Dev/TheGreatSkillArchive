---
name: godot-datadriven-stat-buffs
description: Godot Datadriven Stat Buffs
---

# Godot Datadriven Stat Buffs

## Core Concepts
Buff/debuff system.
```gdscript
class_name Buff extends Resource
@export var name: String
@export var duration := 5.0
@export var speed_mod := 1.0
@export var health_mod := 0
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
