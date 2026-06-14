---
name: godot-metroidvania-ability-gating
description: Godot Metroidvania Ability Gating
---

# Godot Metroidvania Ability Gating

## Core Concepts
Gating with abilities.
```gdscript
class_name AbilityManager extends Node

var has_double_jump := false
var has_dash := false
var has_morph := false

func can_pass(ability: String) -> bool:
    match ability:
        "double_jump": return has_double_jump
        "dash": return has_dash
        "morph": return has_morph
        _: return false
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
