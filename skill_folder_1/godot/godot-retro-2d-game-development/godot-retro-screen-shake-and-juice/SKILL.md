---
name: godot-retro-screen-shake-and-juice
description: Godot Retro Screen Shake And Juice
---

# Godot Retro Screen Shake And Juice

## Core Concepts

## Core Concepts
Screen shake and juice techniques.
```gdscript
extends Camera2D

var shake_amount := 0.0
var shake_duration := 0.0

func shake(amount: float, duration: float) -> void:
    shake_amount = amount
    shake_duration = duration

func _process(delta: float) -> void:
    if shake_duration > 0:
        offset = Vector2(randf() - 0.5, randf() - 0.5) * shake_amount
        shake_duration -= delta
    else:
        offset = Vector2.ZERO
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
