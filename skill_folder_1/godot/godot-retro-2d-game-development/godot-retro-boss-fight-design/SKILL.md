---
name: godot-retro-boss-fight-design
description: Godot Retro Boss Fight Design
---

# Godot Retro Boss Fight Design

## Core Concepts

## Core Concepts
Phased boss fights.
```gdscript
class_name Boss
extends CharacterBody2D

enum Phase { ONE, TWO, THREE }
var phase := Phase.ONE

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 66 and phase == Phase.ONE:
        enter_phase_two()
    elif health <= 33 and phase == Phase.TWO:
        enter_phase_three()

func enter_phase_two() -> void:
    phase = Phase.TWO
    speed *= 1.5
    # Spawn minions
    for i in range(3):
        spawn_minion()
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
