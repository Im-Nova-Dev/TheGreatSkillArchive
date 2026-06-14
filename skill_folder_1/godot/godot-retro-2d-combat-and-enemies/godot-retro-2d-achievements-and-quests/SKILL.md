---
name: godot-retro-2d-achievements-and-quests
description: Godot Retro 2D Achievements And Quests
---

# Godot Retro 2D Achievements And Quests

## Core Concepts
Quest manager and flags.
```gdscript
class_name QuestManager extends Node

var active_quests: Array[Quest] = []
var completed: Array[Quest] = []

func start(quest: Quest) -> void:
    active_quests.append(quest)

func complete(quest: Quest) -> void:
    active_quests.erase(quest)
    completed.append(quest)
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
