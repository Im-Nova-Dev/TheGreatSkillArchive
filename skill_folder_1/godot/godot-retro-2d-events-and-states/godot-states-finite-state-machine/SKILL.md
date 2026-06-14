---
name: godot-states-finite-state-machine
description: Godot States Finite State Machine
---

# Godot States Finite State Machine

## Core Concepts
FSM skeleton.
```gdscript
class_name State extends Node

var machine: Node
var actor: Node

func enter() -> void: pass
func exit() -> void: pass
func update(delta: float) -> void: pass
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
