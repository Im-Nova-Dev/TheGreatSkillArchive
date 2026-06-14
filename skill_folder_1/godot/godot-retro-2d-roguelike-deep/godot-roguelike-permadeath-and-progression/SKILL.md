---
name: godot-roguelike-permadeath-and-progression
description: Godot Roguelike Permadeath And Progression
---

# Godot Roguelike Permadeath And Progression

## Core Concepts
Meta-progression with unlocks.
```gdscript
class_name MetaProgression extends Node

var unlocked_classes: Array[String] = []
var total_gold_earned := 0

func unlock_class(class_name: String) -> void:
    if class_name in unlocked_classes:
        return
    unlocked_classes.append(class_name)
    FileAccess.store_string("user://meta.json", JSON.stringify({
        "classes": unlocked_classes,
        "total_gold": total_gold_earned
    }))
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
