---
name: godot-shmup-boss-fight
description: Godot Shmup Boss Fight
---

# Godot Shmup Boss Fight

## Core Concepts
Boss with pattern phases.
```gdscript
class_name Boss extends Node2D

var patterns := ["spread", "aimed", "spiral"]
var current := 0

func next_phase() -> void:
    current = (current + 1) % patterns.size()
    start_pattern(patterns[current])
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
