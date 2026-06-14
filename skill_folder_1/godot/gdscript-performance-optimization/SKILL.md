---
name: gdscript-performance-optimization
description: Teach GDScript performance optimization including memory management, object pooling, array/dictionary optimization, avoiding allocations in hot paths, profiling with built-in tools, and common anti-patterns.
---

# GDScript Performance Optimization

## Memory Management Fundamentals

### Understanding GDScript Memory Model
- Reference counting (not GC) for Objects
- Value types (int, float, bool, Vector2, etc.) are copied
- Reference types (Array, Dictionary, Object, Resource) are shared
- Circular references **leak memory** - Godot doesn't collect them automatically

### Object Pooling Pattern
```gdscript
# Generic object pool
class_name ObjectPool
extends RefCounted

var _available: Array = []
var _in_use: Array = []
var _factory: Callable

func _init(factory: Callable):
    _factory = factory

func acquire() -> Object:
    var obj = _available.pop_back() if _available.size() > 0 else _factory.call()
    _in_use.append(obj)
    return obj

func release(obj: Object) -> void:
    if obj in _in_use:
        _in_use.erase(obj)
        obj.reset()  # Implement reset() on pooled objects
        _available.append(obj)

func clear() -> void:
    for obj in _in_use:
        release(obj)
    _available.clear()
```

### Usage Example
```gdscript
# Bullet pool
var bullet_pool = ObjectPool.new(Callable(BulletScene, "instantiate"))

func shoot():
    var bullet = bullet_pool.acquire()
    bullet.global_position = muzzle.global_position
    bullet.velocity = direction * speed
    
func _on_bullet_hit(bullet):
    bullet_pool.release(bullet)
```

## Array and Dictionary Optimization

### Pre-allocation
```gdscript
# BAD - reallocates on each append
var positions = []
for i in range(1000):
    positions.append(Vector2())

# GOOD - preallocate
var positions = Array(Vector2)  # Typed array
positions.resize(1000)
for i in range(1000):
    positions[i] = Vector2()
```

### Typed Arrays (Godot 4.2+)
```gdscript
# Faster iteration, type safety
var enemies: Array[Enemy] = []
var waypoints: Array[Vector2] = []

# Avoids boxing/unboxing
for enemy in enemies:
    enemy.update()  # Direct call, no variant dispatch
```

### Dictionary Reuse
```gdscript
# BAD - new dict every frame
func _process(delta):
    var data = {"pos": position, "vel": velocity}
    send_to_shader(data)

# GOOD - reuse
var _shader_data = {"pos": Vector2(), "vel": Vector2()}
func _process(delta):
    _shader_data.pos = position
    _shader_data.vel = velocity
    send_to_shader(_shader_data)
```

## Hot Path Optimization

### Avoid Allocations in _process/_physics_process
```gdscript
# BAD - creates new objects every frame
func _process(delta):
    var direction = (target.global_position - global_position).normalized()
    var new_pos = global_position + direction * speed * delta

# GOOD - reuse vectors
var _temp_dir = Vector2()
var _temp_pos = Vector2()
func _process(delta):
    _temp_dir = (target.global_position - global_position)
    _temp_dir = _temp_dir.normalized()
    _temp_pos = global_position + _temp_dir * speed * delta
    global_position = _temp_pos
```

### Cache Node References
```gdscript
# BAD - get_node every frame
func _process(delta):
    get_node("Sprite").visible = is_visible
    get_node("CollisionShape2D").disabled = not is_solid

# GOOD - cache once
@onready var _sprite = $Sprite
@onready var _collision = $CollisionShape2D
func _process(delta):
    _sprite.visible = is_visible
    _collision.disabled = not is_solid
```

### Use `@onready` Instead of `_ready` for Node References
```gdscript
# @onready runs before _ready, same performance
@onready var player = get_node("../Player")
@onready var camera = get_viewport().get_camera_2d()
```

## Physics Optimization

### Use Layers/Masks Instead of Groups for Collision
```gdscript
# BAD - checks all bodies in group
func _on_area_entered(area):
    if area.is_in_group("enemies"):
        area.take_damage(10)

# GOOD - collision layers filter at engine level
# Set collision_layer = 2 (enemies), collision_mask = 1 (player)
# No script check needed
```

### Raycast vs Area for Simple Checks
```gdscript
# Raycast - single check, very fast
var hit = raycast2d.get_collider()
if hit and hit.is_in_group("enemies"):
    hit.take_damage(10)

# Area - continuous, more expensive
# Use for triggers, pickup zones, etc.
```

## Rendering Optimization

### VisibilityNotifiers for Offscreen Culling
```gdscript
# Add VisibilityNotifier2D to scene
# Connect signals
@onready var notifier = $VisibilityNotifier2D

func _ready():
    notifier.screen_entered.connect(_on_screen_entered)
    notifier.screen_exited.connect(_on_screen_exited)

func _on_screen_entered():
    set_process(true)
    animation_player.play("idle")

func _on_screen_exited():
    set_process(false)
    animation_player.stop()
```

### MultiMesh for Many Identical Objects
```gdscript
# Instead of 1000 Sprite2D nodes
var multimesh = MultiMesh.new()
multimesh.mesh = preload("res://assets/grass_blade.tres")
multimesh.transform_format = MultiMesh.TransformFormat.TRANSFORM_2D
multimesh.instance_count = 1000

for i in range(1000):
    multimesh.set_instance_transform(i, Transform2D(0, random_position()))
```

## Profiling Tools

### Built-in Profiler
```bash
# Debug → Profiler → Start
# Or in code:
Performance.add_monitor("my_custom", "Custom Metric", 0)
Performance.set_monitor("my_custom", value)
```

### Debug Menu Monitors
- FPS, Frame Time, Draw Calls
- Object Count, Shader Changes, Texture Changes
- Video Memory, Physics Objects/Frames

### Custom Timing
```gdscript
var _frame_time = 0

func _process(delta):
    _frame_time = delta
    # Or use Time
    # Time.get_ticks_msec()
```

### Profiler Bottlenecks to Watch
1. **High draw calls** → Batch, MultiMesh, reduce state changes
2. **High object count** → Pool, queue_free unused
3. **Shader changes** → Sort by material, use atlases
4. **Physics frames spikes** → Simplify collision shapes
5. **Script time** → Move heavy math to C#/GDExtension

## Common Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `get_node()` in loops | Cache references |
| String concat in `_process` | Use `StringBuilder` or format once |
| `duplicate()` every frame | Pool objects |
| Large Array/Dict copies | Pass by reference, use `slice()` |
| Recursive functions without tail call | Iterate instead |
| Polymorphic calls in hot loops | Use typed arrays |

## When to Use C#/GDExtension
- Heavy math (pathfinding, physics simulation)
- Large data processing (procedural gen, serialization)
- Algorithms with tight loops (>100k iterations/frame)
- When GDScript profiler shows >2ms script time
