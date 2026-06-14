---
name: godot-datadriven-wave-config
description: Godot Datadriven Wave Config
---

# Godot Datadriven Wave Config

## Core Concepts
Wave data.
```gdscript
class_name WaveData extends Resource
@export var enemies: Array[SpawnEntry]
@export var delay := 0.0
@export var music: AudioStream

class_name SpawnEntry extends Resource
@export var scene: PackedScene
@export var count := 5
@export var interval := 0.5
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
