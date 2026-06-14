---
name: godot-datadriven-dialogue-system
description: Godot Datadriven Dialogue System
---

# Godot Datadriven Dialogue System

## Core Concepts
Dialogue as resource.
```gdscript
class_name DialogueData extends Resource
@export var lines: Array[DialogueLine]
@export var start_id := 0

class_name DialogueLine extends Resource
@export var speaker: String
@export var text: String
@export var next: int = -1
@export var choices: Array[DialogueChoice] = []

class_name DialogueChoice extends Resource
@export var text: String
@export var next: int
@export var condition: Callable
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
