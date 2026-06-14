---
name: godot-events-signalbus-advanced
description: Godot Events Signalbus Advanced
---

# Godot Events Signalbus Advanced

## Core Concepts
Typed signal bus.
```gdscript
extends Node

signal player_health_changed(new_health: int)
signal enemy_killed(enemy: Node2D)
signal level_completed(level_id: String)
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
