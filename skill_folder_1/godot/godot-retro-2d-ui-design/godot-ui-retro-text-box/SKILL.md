---
name: godot-ui-retro-text-box
description: Godot Ui Retro Text Box
---

# Godot Ui Retro Text Box

## Core Concepts
Typewriter dialog.
```gdscript
class_name DialogBox extends RichTextLabel

@export var speed := 0.04
var text := ""
var idx := 0

func show(text: String) -> void:
    self.text = ""
    idx = 0
    visible = true
    type_next()

func type_next() -> void:
    if idx < text.length():
        self.text += text[idx]
        idx += 1
        await get_tree().create_timer(speed).timeout
        type_next()
```

## Learning Path

1. **Foundation**: Learn the core concepts.
2. **Implementation**: Build a focused demo.
3. **Deep dive**: Refine and extend.
4. **Production**: Integrate into your game.

## Common Pitfalls

- Hardcoding values everywhere.
- Writing monolithic scripts.
- Skipping physics and input setup first.
- Polishing too early.

## Best Practices

- Keep data in Resources.
- Keep logic in small nodes/components.
- Use typed GDScript consistently.
- Profile and optimize after gameplay is locked.

## Resources

- Godot 4 documentation
- GDQuest tutorials
- /r/godot
- itch.io devlogs
- Game jam communities
