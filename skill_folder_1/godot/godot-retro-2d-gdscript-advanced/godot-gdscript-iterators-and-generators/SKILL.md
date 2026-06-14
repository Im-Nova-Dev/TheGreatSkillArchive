---
name: godot-gdscript-iterators-and-generators
description: Godot Gdscript Iterators And Generators
---

# Godot Gdscript Iterators And Generators

## Core Concepts
Custom iterator.
```gdscript
class_name GridIterator extends RefCounted

var width := 10
var height := 10

func _iter_init(_arg) -> bool:
    _x = 0
    _y = 0
    return true

func _iter_next(_arg) -> bool:
    _x += 1
    if _x >= width:
        _x = 0
        _y += 1
    return _y < height

func _iter_get(_arg) -> Vector2i:
    return Vector2i(_x, _y)

var _x := 0
var _y := 0
```

## Learning Path

1. **Foundation**: Study the core concepts and examples.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand.
4. **Production**: Make it a complete game or tool.

## Common Pitfalls

- Overcomplicating scope.
- Forgetting typed GDScript.
- Hardcoding paths and magic numbers.
- Skipping project settings (pixel perfect, stretch mode).
- Neglecting mobile and export testing.

## Best Practices

- Keep one-click export ready.
- Use project settings for pixel-perfect rendering.
- Keep scripts small and focused.
- Organize resources in clear folders.
- Profile before optimizing.
- Ship early and iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b, KidsCanCode
- /r/godot
- itch.io devlogs
- Game jam communities
- Official Discord
