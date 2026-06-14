---
name: godot-retro-achievements-and-leaderboard
description: Godot Retro Achievements And Leaderboard
---

# Godot Retro Achievements And Leaderboard

## Core Concepts

## Core Concepts
Local leaderboard using JSON.
```gdscript
class_name HighScoreManager
extends Node

const PATH := "user://highscores.json"
var scores: Array[int] = []

func load_scores() -> void:
    if FileAccess.file_exists(PATH):
        var json := FileAccess.get_file_as_string(PATH)
        scores = JSON.parse_string(json)
    else:
        scores = []

func save_score(score: int) -> void:
    scores.append(score)
    scores.sort()
    scores.reverse()
    scores = scores.slice(0, 10)
    FileAccess.store_string(PATH, JSON.stringify(scores))
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
