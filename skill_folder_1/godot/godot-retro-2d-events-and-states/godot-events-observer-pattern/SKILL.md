---
name: godot-events-observer-pattern
description: Godot Events Observer Pattern
---

# Godot Events Observer Pattern

## Core Concepts
Observer in GDScript.
```gdscript
class_name EventBus extends Node

var listeners: Dictionary = {}

func on(event: StringName, callable: Callable) -> void:
    if event not in listeners:
        listeners[event] = []
    listeners[event].append(callable)

func emit(event: StringName, args: Array = []) -> void:
    if event in listeners:
        for cb in listeners[event]:
            cb.callv(args)
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
