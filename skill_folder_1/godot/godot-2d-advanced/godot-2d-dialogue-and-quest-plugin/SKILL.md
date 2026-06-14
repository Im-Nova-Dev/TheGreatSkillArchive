---
name: godot-2d-dialogue-and-quest-plugin
description: Godot 2D Dialogue And Quest Plugin
---

# Godot 2D Dialogue And Quest Plugin

## Core Concepts

## Core Concepts
Build a dialogue system using `Resource` and `Array[Dictionary]`.

## GDScript Example
```gdscript
class_name DialogueLine
extends Resource
@export var speaker: String
@export var text: String
@export var next_id: int = -1
@export var choices: Array[DialogueChoice] = []

class_name DialogueChoice
extends Resource
@export var text: String
@export var next_id: int
@export var condition: Callable
```

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4 / GDScript 2.
3. **Deep dive**: Explore editor workflows and advanced 2D patterns.
4. **Production**: Polish gameplay, input feel, and deployment.



## Common Pitfalls

- Misusing node parenting and scene composition.
- Mixing 3D patterns into a 2D project.
- Forgetting to use `delta` for frame-independent movement.
- Hardcoding input without using the Input Map.

## Best Practices

- Keep scripts small, single-responsibility, and well-named.
- Prefer signals and loose coupling.
- Profile with Godot’s debugger before optimizing.
- Use typed GDScript and `@icon` annotations.

## Resources

- Official Godot 4 documentation and class reference
- GDQuest 2D content
- /r/godot and Godot Forums
- KidsCanCode and HeartBeast tutorials
- YouTube: GYArray, GameDev Tavern, 41b
