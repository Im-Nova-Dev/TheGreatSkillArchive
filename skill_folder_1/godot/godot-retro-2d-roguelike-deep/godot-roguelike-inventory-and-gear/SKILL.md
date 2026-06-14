---
name: godot-roguelike-inventory-and-gear
description: Godot Roguelike Inventory And Gear
---

# Godot Roguelike Inventory And Gear

## Core Concepts
Equipment slots and stats.
```gdscript
class_name Equipment extends Resource
@export var slot := "weapon"
@export var attack_bonus := 0
@export var defense_bonus := 0
@export var sprite: Texture2D

class_name Inventory extends Node
var equipment: Dictionary = {}
```

## Learning Path

1. **Foundation**: Study the core concepts.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand with more features.
4. **Production**: Make it a complete game.

## Common Pitfalls

- Scope creep: start tiny.
- Polishing before gameplay is locked.
- Forgetting pixel-snap camera.
- Over-engineering systems.

## Best Practices

- Keep one-click export ready.
- Profile 60 FPS target.
- Use Godot primitives (TileMap, AnimationPlayer).
- Ship one level, then iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b
- /r/godot
- itch.io devlogs
- Game jam communities
