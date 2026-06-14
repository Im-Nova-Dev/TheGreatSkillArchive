---
name: godot-2d-event-bus-and-deferred-signals
description: Godot 2D Event Bus And Deferred Signals
---

# Godot 2D Event Bus And Deferred Signals

## Core Concepts

Practical patterns and working GDScript for `Godot 2D Event Bus And Deferred Signals` in Godot 4.

## GDScript Example

Deferred and one-shot signal helpers.
```gdscript
func defer(callable: Callable) -> void:
    call_deferred(callable)

func oneshot_connect(target: Object, signal_name: StringName, callable: Callable) -> void:
    target.connect(signal_name, func(_a=null,_b=null):
        callable.call()
        target.disconnect(signal_name, func(_a=null,_b=null): return true)
    , CONNECT_ONE_SHOT)
```

## Common Pitfalls

- Writing physics in `_process` instead of `_physics_process`.
- Forgetting typed `@onready` variables.
- Using global magic numbers everywhere.
- Hardcoding paths and not using exported resources.

## Best Practices

- Prefer typed GDScript with `get_class()` checks.
- Keep node references in `@onready` or inject them.
- Use resources for data, nodes for behavior.
- Profile before optimizing; avoid premature caching.

## Resources

- Official Godot 4 docs
- GDQuest and HeartBeast tutorials
- /r/godot and official Q&A
- Godot Asset Library
- YouTube: GYArray, GameDev Tavern, 41b
