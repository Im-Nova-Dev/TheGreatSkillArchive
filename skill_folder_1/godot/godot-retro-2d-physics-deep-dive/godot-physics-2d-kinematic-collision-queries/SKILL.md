---
name: godot-physics-2d-kinematic-collision-queries
description: Godot Physics 2D Kinematic Collision Queries
---

# Godot Physics 2D Kinematic Collision Queries

## Core Concepts
Testing movement before moving.
```gdscript
func can_move_to(pos: Vector2) -> bool:
    var space := get_world_2d().direct_space_state
    var query := PhysicsMotionQueryParameters2D.new()
    query.from = global_position
    query.to = pos
    query.collision_mask = 1
    var result := space.intersect_motion(query)
    return result.collision_count == 0
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
