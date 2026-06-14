---
name: godot-zelda-room-graph
description: Godot Zelda Room Graph
---

# Godot Zelda Room Graph

## Core Concepts
Dungeon room graph.
```gdscript
class_name DungeonMap extends Resource
@export var rooms: Array[Room]
@export var connections: Array[Connection]

class_name Room extends Resource
@export var id := ""
@export var scene := ""
@export var north := ""
@export var south := ""
@export var east := ""
@export var west := ""

class_name Connection extends Resource
@export var from: String
@export var direction: String
@export var to: String
```

## Learning Path

1. **Foundation**: Study the core concepts.
2. **Implementation**: Build a small demo in Godot 4.
3. **Deep dive**: Polish and expand with more features.
4. **Production**: Make it a complete game.

## Common Pitfalls

- Scope creep: start tiny.
- Polishing before gameplay is locked.
- Forgetting pixel-snap camera.
- Over-engineering systems.

## Best Practices

- Keep one-click export ready.
- Profile 60 FPS target.
- Use Godot primitives (TileMap, AnimationPlayer).
- Ship one level, then iterate.

## Resources

- Godot 4 docs
- GDQuest, HeartBeast, 41b
- /r/godot
- itch.io devlogs
- Game jam communities
