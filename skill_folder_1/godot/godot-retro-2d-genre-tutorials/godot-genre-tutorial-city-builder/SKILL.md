---
name: godot-genre-tutorial-city-builder
description: Godot Genre Tutorial City Builder
---

# Godot Genre Tutorial City Builder

## Core Concepts

## Core Concepts
Grid-based placement.
```gdscript
class_name Building extends Resource
@export var size: Vector2i
@export var cost: int
@export var population: int
@export var texture: Texture2D
```

## Learning Path

1. **Foundation**: Study the concepts and examples.
2. **Implementation**: Rebuild the snippet in a Godot test project.
3. **Deep dive**: Adapt to your genre and art style.
4. **Production**: Polish and ship.

## Common Pitfalls

- Scoping too wide before core loop is fun.
- Hardcoding paths and magic numbers.
- Ignoring Godot’s built-in nodes (TileMap, AnimationPlayer).
- Skipping pixel-snap camera setup.

## Best Practices

- Use typed GDScript and `@onready`.
- Keep scenes modular and composable.
- Profile before optimizing.
- Ship a minimal vertical slice first.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b, KidsCanCode
- /r/godot
- itch.io devlogs
- Game jam communities
