---
name: godot-retro-2d-animation-state-machine
description: Godot Retro 2D Animation State Machine
---

# Godot Retro 2D Animation State Machine

## Core Concepts
Compact state machine with AnimationNodeStateMachine.
```gdscript
@onready var tree: AnimationTree = $AnimationTree

func set_state(new_state: StringName) -> void:
    tree.set("parameters/state/current", new_state)
```

## Common Pitfalls

- Overcomplicating scope before the core loop is confirmed fun.
- Polishing visuals before gameplay feels right.
- Missing one-click export workflow until submit day.
- Ignoring Godot’s built-in TileMap and Animation tools.

## Best Practices

- Scope to one screen first.
- Profile every build.
- Ship one polished level instead of three rough ones.
- Keep art in consistent palette and resolution.

## Resources

- Godot 4 class reference
- GDQuest retro/2D tutorials
- /r/godot
- Game jam communities (Ludum Dare, GMTK)
- itch.io devlogs
