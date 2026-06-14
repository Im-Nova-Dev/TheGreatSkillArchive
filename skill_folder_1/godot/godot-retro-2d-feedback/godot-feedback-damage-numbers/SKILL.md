---
name: godot-feedback-damage-numbers
description: Godot Feedback Damage Numbers
---

# Godot Feedback Damage Numbers

## Core Concepts
Floating damage text.
```gdscript
class_name FloatingText extends Node2D

@export var value := "1"
@export var lifetime := 0.5

func _ready() -> void:
    $Label.text = value
    var tween := create_tween()
    tween.tween_property(self, "position:y", position.y - 16, lifetime)
    tween.tween_property(self, "modulate:a", 0.0, lifetime)
    tween.tween_callback(queue_free)
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
