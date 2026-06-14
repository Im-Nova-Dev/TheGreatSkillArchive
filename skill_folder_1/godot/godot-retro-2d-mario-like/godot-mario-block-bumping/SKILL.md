---
name: godot-mario-block-bumping
description: Godot Mario Block Bumping
---

# Godot Mario Block Bumping

## Core Concepts
Bumpable question block.
```gdscript
class_name QuestionBlock extends Node2D

@export var contains := "coin"
var used := false

func bump() -> void:
    if used: return
    used = true
    $Sprite2D.frame = 1
    spawn_contents()
    var tween := create_tween()
    tween.tween_property(self, "position:y", position.y - 8, 0.08)
    tween.tween_property(self, "position:y", position.y, 0.12)

func spawn_contents() -> void:
    if contains == "coin":
        # Spawn coin popup
        pass
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
