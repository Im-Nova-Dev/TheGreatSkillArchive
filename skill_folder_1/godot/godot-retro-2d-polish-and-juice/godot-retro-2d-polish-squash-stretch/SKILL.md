---
name: godot-retro-2d-polish-squash-stretch
description: Godot Retro 2D Polish Squash Stretch
---

# Godot Retro 2D Polish Squash Stretch

## Core Concepts
Squash and stretch tween.
```gdscript
func squash(node: Node2D) -> void:
    var tween := node.create_tween()
    tween.tween_property(node, "scale", Vector2(1.4, 0.6), 0.08)
    tween.tween_property(node, "scale", Vector2.ONE, 0.08)

func stretch(node: Node2D) -> void:
    var tween := node.create_tween()
    tween.tween_property(node, "scale", Vector2(0.7, 1.3), 0.08)
    tween.tween_property(node, "scale", Vector2.ONE, 0.08)
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
