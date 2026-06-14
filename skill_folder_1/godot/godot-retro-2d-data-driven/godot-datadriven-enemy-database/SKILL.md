---
name: godot-datadriven-enemy-database
description: Godot Datadriven Enemy Database
---

# Godot Datadriven Enemy Database

## Core Concepts
Enemy stats from resources.
```gdscript
class_name EnemyData extends Resource
@export var name: String
@export var health := 3
@export var speed := 60.0
@export var sprite: Texture2D
@export var behavior := "patrol"
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
