---
name: gdscript-advanced-patterns-and-metaprogramming
description: Teach advanced GDScript patterns including metaprogramming, reflection, duck typing, callable manipulation, dynamic method binding, and runtime code generation patterns for Godot 4.
---

# GDScript Advanced Patterns & Metaprogramming

## Reflection and Runtime Type Inspection

### Getting Class Information
```gdscript
# Get class name
var class_name = MyNode.get_class_static()

# Check inheritance
if obj.is_class("CharacterBody2D"):
    obj.velocity = Vector2.ZERO

# Get all methods
var methods = MyNode.get_method_list()
for method in methods:
    print(method.name, method.arguments)

# Get all signals
var signals = MyNode.get_signal_list()

# Get all properties
var properties = MyNode.get_property_list()
```

### Dynamic Method Invocation
```gdscript
# Call method by name string
obj.call("method_name", arg1, arg2)

# Call deferred (next frame)
obj.call_deferred("method_name", arg1, arg2)

# Check if method exists
if obj.has_method("custom_method"):
    obj.call("custom_method")

# Get method info
var method_info = obj.get_method_list().find({"name": "my_method"})
```

### Property Manipulation at Runtime
```gdscript
# Set property by name
obj.set("property_name", new_value)

# Get property by name
var value = obj.get("property_name")

# Check property existence
if obj.has_property("health"):
    obj.set("health", 100)

# Property info
var prop_info = obj.get_property_list().find({"name": "health"})
```

## Duck Typing and Structural Typing

### Using `Object` for Dynamic Types
```gdscript
# Accept any object with required methods
func process_entity(entity: Object) -> void:
    # Runtime check for required methods
    if entity.has_method("take_damage") and entity.has_method("get_position"):
        entity.take_damage(10)
        var pos = entity.call("get_position")
    else:
        push_error("Entity missing required interface")
```

### Protocol-like Patterns
```gdscript
# Define expected interface as documentation
# class_name IDamageable
# 
# @abstract
# func take_damage(amount: float) -> void
# 
# @abstract
# func get_health() -> float
# 
# @abstract
# func is_alive() -> bool

func apply_poison(target: Object, damage_per_second: float, duration: float) -> void:
    # Runtime verification
    assert target.has_method("take_damage")
    assert target.has_method("get_health")
    
    var tween = create_tween()
    tween.set_loops(int(duration))
    tween.tween_callback(Callable(target, "take_damage").bind(damage_per_second))
```
