---
name: gdscript-async-patterns-and-coroutines
description: Teach GDScript async patterns including await, coroutines, signal-based async, task management, timeout handling, and cancellation patterns for Godot 4.
---

# GDScript Async Patterns & Coroutines

## Core Await Patterns

### Signal-Based Await
```gdscript
# Wait for any signal
await button.pressed
await animation_player.animation_finished
await timer.timeout

# With parameters (Godot 4.2+)
await animation_player.animation_finished("attack")
```

### Creating Timers
```gdscript
# One-shot timer
await get_tree().create_timer(1.0).timeout

# Reusable timer pattern
func wait_seconds(seconds: float) -> void:
    await get_tree().create_timer(seconds).timeout
```

### Custom Signal Await
```gdscript
# In your class
signal task_completed(result)

func do_work():
    await some_async_operation()
    emit_signal("task_completed", result)

# Caller
func caller():
    var instance = MyClass.new()
    var result = await instance.task_completed
    print(result)
```

## Advanced Coroutine Patterns

### Parallel Execution
```gdscript
# Run multiple async operations in parallel
func load_all_assets() -> void:
    var texture_task = load_texture_async("res://tex.png")
    var audio_task = load_audio_async("res://sfx.ogg")
    var data_task = load_json_async("res://data.json")
    
    # Wait for all
    var texture = await texture_task
    var audio = await audio_task
    var data = await data_task

# Using arrays for dynamic parallelism
func load_multiple(paths: Array[String]) -> Array[Texture2D]:
    var tasks = []
    for path in paths:
        tasks.append(load_texture_async(path))
    
    var results = []
    for task in tasks:
        results.append(await task)
    return results
```

### Sequential with Error Handling
```gdscript
func fetch_and_process() -> void:
    try:
        var raw = await http_request("api/game/data")
        var parsed = JSON.parse_string(raw)
        var validated = validate_data(parsed)
        await save_to_disk(validated)
        ui.show_success()
    except err:
        ui.show_error("Failed: " + err.message)
```

### Timeout Patterns
```gdscript
func with_timeout(task: Callable, seconds: float, fallback) -> Variant:
    var timer = get_tree().create_timer(seconds)
    var task_finished = false
    var result
    
    func _on_task_done(res):
        task_finished = true
        result = res
    
    task.call_deferred(_on_task_done)
    
    await timer.timeout
    
    if not task_finished:
        return fallback
    return result
```

### Cancellation Token Pattern
```gdscript
class_name CancellationToken
extends RefCounted

var cancelled = false

func cancel() -> void:
    cancelled = true

func throw_if_cancelled() -> void:
    if cancelled:
        push_error("Operation cancelled")
        return  # Or custom error handling

# Usage
func long_operation(token: CancellationToken) -> void:
    for i in range(100):
        token.throw_if_cancelled()
        await get_tree().process_frame
        do_work_chunk(i)

func caller():
    var token = CancellationToken.new()
    long_operation(token)
    # Later...
    token.cancel()
```

## Signal-Based Async Helpers

### SignalAwaiter Utility
```gdscript
class_name SignalAwaiter
extends RefCounted

static func wait_for_signal(obj: Object, signal_name: String, timeout: float = -1) -> Variant:
    var awaiter = SignalAwaiter.new()
    var result
    var finished = false
    
    func _on_signal(*args):
        finished = true
        result = args.size() == 1 ? args[0] : args
    
    obj.connect(signal_name, _on_signal.bind()).once()
    
    if timeout > 0:
        await get_tree().create_timer(timeout).timeout
        if not finished:
            push_error("Signal timeout: " + signal_name)
            return null
    else:
        while not finished:
            await get_tree().process_frame
    
    return result
```

### Tween Async Wrapper
```gdscript
func tween_async(tween: Tween, property: String, final_val: Variant, duration: float) -> void:
    var completed = false
    tween.tween_property(null, property, final_val, duration).finished.connect(_on_tween_done)
    
    func _on_tween_done():
        completed = true
    
    while not completed:
        await get_tree().process_frame
```

## Task Management

### Task Queue
```gdscript
class_name TaskQueue
extends RefCounted

var _queue: Array[Callable] = []
var _running = false
var _max_concurrent = 3
var _active = 0

func add(task: Callable) -> void:
    _queue.append(task)
    _process_queue()

func _process_queue() -> void:
    while _queue.size() > 0 and _active < _max_concurrent:
        var task = _queue.pop_front()
        _active += 1
        await _run_task(task)
        _active -= 1
    if _queue.size() > 0:
        call_deferred("_process_queue")

async func _run_task(task: Callable) -> void:
    try:
        await task.call()
    except err:
        push_error("Task failed: " + err.message)
```

### Debounced Async
```gdscript
func debounced_action(action: Callable, delay: float = 0.3) -> void:
    if _debounce_timer:
        _debounce_timer.stop()
    _debounce_timer = get_tree().create_timer(delay)
    await _debounce_timer.timeout
    action.call()
```

## Best Practices

1. **Always handle cancellation** - prevent memory leaks
2. **Use `call_deferred`** for cross-thread safety
3. **Avoid `await` in `_process`** - use signals instead
4. **Return `void` from async functions** unless you need the result
5. **Test timeouts** - network/resouce loads can hang
6. **Don't block the main thread** - use `await get_tree().process_frame` for yielding
7. **Pool timers** for frequent short delays
