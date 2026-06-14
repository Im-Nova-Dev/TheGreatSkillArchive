---
name: gdscript-testing-and-tdd
description: Teach GDScript testing patterns using GUT (Godot Unit Test), WAT (Where Are Tests), unit tests, integration tests, scene tests, mocking, and CI/CD integration for Godot projects.
---

# GDScript Testing & TDD

## GUT (Godot Unit Test) Setup

### Installation
```bash
# Via AssetLib in Godot Editor
# Search "GUT" and install

# Or manual: clone to addons/gut
git clone https://github.com/bitwes/Gut addons/gut
```

### Project Configuration
```ini
# project.gut
[general]
source_dirs=["res://src/", "res://tests/"]
suffixes=["_test.gd", "_test.tscn"]
```

### Basic Test Structure
```gdscript
# tests/player_test.gd
extends GutTest

func before_each():
    # Setup fresh state per test
    player = preload("res://scenes/player.tscn").instantiate()
    add_child(player)

func after_each():
    player.queue_free()

func test_player_starts_with_full_health():
    assert_eq(player.health, 100)

func test_taking_damage_reduces_health():
    player.take_damage(30)
    assert_eq(player.health, 70)

func test_death_at_zero_health():
    player.take_damage(100)
    assert_true(player.is_dead())

func test_healing_caps_at_max():
    player.take_damage(50)
    player.heal(100)
    assert_eq(player.health, 100)
```

### Async Tests
```gdscript
func test_attack_animation_completes():
    player.attack()
    # Wait for animation to finish
    await async_wait(player.animation_player, "animation_finished", "attack")
    assert_true(player.can_attack_again)
```

## Scene Integration Tests
```gdscript
# tests/game_integration_test.gd
extends GutTest

func test_level_loads_successfully():
    var scene = preload("res://scenes/main_level.tscn").instantiate()
    add_child_autofree(scene)
    
    await get_tree().process_frame
    await get_tree().process_frame
    
    assert_not_null(scene.get_node("Player"))
    assert_not_null(scene.get_node("Enemies"))
    assert_not_null(scene.get_node("UI"))
```

## Mocking with GUT
```gdscript
# Using GUT's mock system
func test_enemy_ai_targets_player():
    var mock_player = MockObject.new()
    mock_player.set_method("get_global_position", Callable(self, "_mock_player_position"))
    
    var enemy = preload("res://enemies/chaser.tscn").instantiate()
    enemy.target = mock_player
    add_child_autofree(enemy)
    
    await get_tree().process_frame
    # Verify enemy moved toward mock position
```

## Running Tests

### Editor
- Press `Shift+F6` or click GUT panel → Run Tests

### Headless (CI)
```bash
godot --headless -d -s addons/gut/gut_cmdln.gd
```

### Exit Codes
- 0: All passed
- 1: Failures
- 2: Errors

## TDD Workflow

### Red-Green-Refactor Cycle
```gdscript
# 1. RED - Write failing test
func test_double_jump_allowed_after_first_jump():
    player.jump()
    player.jump()  # Second jump
    assert_true(player.is_double_jumping)

# 2. GREEN - Minimal implementation
func jump():
    if is_on_floor():
        velocity.y = JUMP_FORCE
        _jumps_used = 1
    elif _jumps_used == 1:
        velocity.y = JUMP_FORCE
        _jumps_used = 2
        is_double_jumping = true

# 3. REFACTOR - Clean up
```

## Test Organization
```
tests/
├── unit/
│   ├── player_test.gd
│   ├── enemy_test.gd
│   └── inventory_test.gd
├── integration/
│   ├── combat_test.gd
│   └── level_loading_test.gd
├── fixtures/
│   ├── mock_player.gd
│   └── test_level.tscn
└── utils/
    └── test_helpers.gd
```

## Best Practices
1. **One assertion per test** - Easier debugging
2. **Descriptive names** - `test_health_decreases_when_hit` not `test_hit`
3. **Isolate tests** - Use `before_each`/`after_each`
4. **Test behavior, not implementation** - Don't test private methods
5. **Fast tests** - Headless tests should run in seconds
6. **Deterministic** - No randomness in unit tests
