---
name: godot-2d-platformer-movement-advanced
description: Godot 2D Platformer Movement Advanced
---

# Godot 2D Platformer Movement Advanced

## Core Concepts

## Core Concepts
High-quality platformer kinematic controls.

## GDScript Example
```gdscript
extends CharacterBody2D

const SPEED := 180.0
const JUMP_VELOCITY := -320.0
const GRAVITY := 980.0

@export var coyote_time := 0.12
@export var jump_buffer := 0.1

var _coyote_timer := 0.0
var _jump_buffer_timer := 0.0

func _physics_process(delta: float) -> void:
    if is_on_floor():
        _coyote_timer = coyote_time
    else:
        _coyote_timer -= delta

    if Input.is_action_just_pressed("jump"):
        _jump_buffer_timer = jump_buffer
    else:
        _jump_buffer_timer -= delta

    if _jump_buffer_timer > 0 and _coyote_timer > 0:
        velocity.y = JUMP_VELOCITY
        _jump_buffer_timer = 0
        _coyote_timer = 0

    if not is_on_floor() and Input.is_action_just_released("jump") and velocity.y < 0:
        velocity.y *= 0.5

    velocity.y += GRAVITY * delta
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * SPEED
    move_and_slide()
```

## Learning Path

1. **Foundation**: Learn core principles and terminology.
2. **Implementation**: Build small working examples in Godot 4 / GDScript 2.
3. **Deep dive**: Explore editor workflows and advanced 2D patterns.
4. **Production**: Polish gameplay, input feel, and deployment.



## Common Pitfalls

- Misusing node parenting and scene composition.
- Mixing 3D patterns into a 2D project.
- Forgetting to use `delta` for frame-independent movement.
- Hardcoding input without using the Input Map.

## Best Practices

- Keep scripts small, single-responsibility, and well-named.
- Prefer signals and loose coupling.
- Profile with Godot’s debugger before optimizing.
- Use typed GDScript and `@icon` annotations.

## Resources

- Official Godot 4 documentation and class reference
- GDQuest 2D content
- /r/godot and Godot Forums
- KidsCanCode and HeartBeast tutorials
- YouTube: GYArray, GameDev Tavern, 41b
