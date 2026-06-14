---
name: godot-2d-signal-bus-pattern
description: Godot 2D Signal Bus Pattern
---

# Godot 2D Signal Bus Pattern

## Core Concepts

## Core Concepts
Global event systems using `SignalBus` autoload.

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4 / GDScript 2.
3. **Deep dive**: Explore editor workflows and advanced 2D patterns.
4. **Production**: Polish gameplay, input feel, and deployment.


1. Create an autoload `SignalBus.gd` with `signal`.
2. Connect player signals to UI/HUD.
3. Decouple scene communication safely.

## GDScript Example
```gdscript
# signal_bus.gd
extends Node

signal health_changed(new_health: int)
signal player_died

# player.gd
SignalBus.health_changed.emit(80)
```


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
