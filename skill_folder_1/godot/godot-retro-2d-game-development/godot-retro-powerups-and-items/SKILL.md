---
name: godot-retro-powerups-and-items
description: Godot Retro Powerups And Items
---

# Godot Retro Powerups And Items

## Core Concepts

## Core Concepts
Classic item pickups (mushroom, fire flower, etc.).
```gdscript
class_name RetroPowerup
extends Area2D

@export var type := "speed"
var collected := false

func _on_body_entered(body: Node2D) -> void:
    if collected or not body.name == "Player":
        return
    collected = true
    match type:
        "speed": body.SPEED *= 1.5
        "health": body.health += 25
        "double_jump": body.can_double_jump = true
    queue_free()
```

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4.
3. **Deep dive**: Explore engine workflows and retro-specific techniques.
4. **Production**: Polish and ship a finished retro 2D game.

## Common Pitfalls

- Over-filtering textures (destroy pixel crispness).
- Using modern 3D patterns instead of tile-based thinking.
- Forgetting to lock input during cutscenes/dialogue.
- Hardcoding animation speeds rather than using delta.

## Best Practices

- Use project settings to lock pixel-perfect rendering.
- Keep a single source of truth for game state.
- Organize scenes and resources in clear folder structures.
- Profile performance before optimizing.
- Ship early; polish later.

## Resources

- Official Godot 4 documentation and class reference
- GDQuest courses
- KidsCanCode and HeartBeast tutorials
- /r/godot and Godot Forums
- Game jam communities
- YouTube: GYArray, GameDev Tavern, 41b
- itch.io game dev forums
