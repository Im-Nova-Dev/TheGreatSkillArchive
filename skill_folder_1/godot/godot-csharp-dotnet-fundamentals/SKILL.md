---
name: godot-csharp-dotnet-fundamentals
description: Teach C#/.NET development in Godot 4+, including project setup, C# vs GDScript patterns, .NET APIs, Godot C# bindings, signals, async/await, NuGet packages, debugging, and migration from GDScript.
---

# Godot C#/.NET Fundamentals

## Prerequisites
- Godot 4.2+ (Mono/.NET version)
- .NET SDK 6.0+ or 8.0+ installed
- IDE: VS Code + C# Dev Kit, or Rider, or Visual Studio

## Project Setup

### Creating a C# Project
```bash
# From Godot Project Manager: select ".NET" template
# Or via CLI:
dotnet new console -o MyGodotProject
cd MyGodotProject
# Add Godot C# bindings via NuGet
dotnet add package GodotSharp --version 4.3.0
```

### Project Structure
```
MyGame/
├── MyGame.csproj          # .NET project file
├── project.godot          # Godot project config
├── src/                   # C# source (convention)
│   ├── Player.cs
│   ├── Enemy.cs
│   └── GameManager.cs
├── Scenes/                # .tscn files
├── Resources/             # .tres, images, etc.
```

### .csproj Essentials
```xml
<Project Sdk="Godot.NET.Sdk/4.3.0">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="GodotSharp" Version="4.3.0" />
  </ItemGroup>
</Project>
```

## C# vs GDScript Patterns

### Class Declaration
```csharp
// GDScript
class_name Player
extends CharacterBody2D

// C#
using Godot;

public partial class Player : CharacterBody2D
{
    // [Export] replaces @export
    [Export] public float Speed = 300.0f;
    [Export] public int MaxHealth = 100;
}
```

### Signals
```csharp
// GDScript
signal health_changed(new_health)

// C#
[Signal]
public delegate void HealthChangedEventHandler(int newHealth);

// Emitting
EmitSignal(SignalName.HealthChanged, currentHealth);

// Connecting
player.HealthChanged += OnHealthChanged;
```

### Nodes and Scene Tree
```csharp
// GetNode<T>() with type safety
var sprite = GetNode<AnimatedSprite2D>("Sprite");
var collision = GetNode<CollisionShape2D>("CollisionShape2D");

// FindNode with pattern
var enemies = GetTree().GetNodesInGroup("enemies");

// Add to group
AddToGroup("players");
```

### Async/Await (C# advantage)
```csharp
// GDScript: await get_tree().create_timer(1.0).timeout
// C#: proper async/await
public async Task WaitForSeconds(float seconds)
{
    await ToSignal(GetTree().CreateTimer(seconds), "timeout");
}

// Complex async flow
public async Task AttackSequence()
{
    PlayAnimation("attack");
    await ToSignal(animPlayer, "animation_finished");
    SpawnHitbox();
    await WaitForSeconds(0.2f);
    RemoveHitbox();
}
```

### Properties and Exports
```csharp
// Basic export
[Export] public float JumpForce = 500f;

// With hints
[Export(PropertyHint.Range, "0,100,1")] public int Level = 1;
[Export(PropertyHint.File, "*.tres")] public Resource CustomResource;
[Export(PropertyHint.Dir)] public string SaveDirectory;

// Groups for inspector organization
[ExportGroup("Movement")]
[Export] public float WalkSpeed = 300f;
[Export] public float RunSpeed = 500f;
```

### Collections
```csharp
// Arrays
[Export] public Vector2[] PatrolPoints;
public Godot.Collections.Array<string> Inventory = [];

// Dictionaries
public Godot.Collections.Dictionary<string, int> Stats = new()
{
    ["strength"] = 10,
    ["agility"] = 15
};

// Typed arrays (Godot 4.2+)
[Export] public Godot.Collections.Array<Vector2> Waypoints;
```

### Resource Handling
```csharp
// Load resource
var texture = GD.Load<Texture2D>("res://assets/player.png");
var scene = GD.Load<PackedScene>("res://scenes/enemy.tscn");

// Preload (compile-time)
[Export] public PackedScene BulletScene;

// Instantiate
var bullet = BulletScene.Instantiate<Node2D>();
AddChild(bullet);
```

## Advanced Patterns

### Partial Classes (Godot 4.3+)
```csharp
// Player.cs
public partial class Player : CharacterBody2D { }

// Player.Movement.cs
public partial class Player
{
    private void HandleMovement(double delta) { ... }
}
```

### Callable and Delegates
```csharp
// Creating callables
var myCallable = new Callable(this, nameof(MyMethod));
GetTree().CreateTimer(1.0).Timeout += myCallable;

// Lambda callables
button.Pressed += () => GD.Print("Clicked!");
```

### Interop with GDScript
```csharp
// Call GDScript from C#
var gdScriptNode = GetNode<Node>("GDScriptNode");
gdScriptNode.Call("gdscript_method", "arg1", 42);

// Call C# from GDScript
// In GDScript: csharp_node.call("csharp_method", "arg")
[Export] public void CSharpMethod(string message) { ... }
```

### NuGet Packages
```bash
# Common useful packages
dotnet add package Newtonsoft.Json
dotnet add package Dapper          # DB access
dotnet add package Polly           # Resilience
dotnet add package MediatR         # Mediator pattern
dotnet add package FluentValidation
```

## Debugging

### VS Code / Rider
```json
// launch.json for VS Code
{
    "configurations": [
        {
            "name": "Godot C# Debug",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/MyGame.exe"
        }
    ]
}
```

### Logging
```csharp
GD.Print("Standard print");
GD.PrintErr("Error print");
GD.PrintRich("[color=yellow]Rich[/color] [b]BBCode[/b]");
```

## Common Pitfalls
1. **Forgetting `[Export]`** - properties won't appear in inspector
2. **Partial class mismatch** - all parts must have `partial`
3. **Null reference on GetNode** - use `GetNodeOrNull<T>()` or `HasNode()`
4. **Signal signature mismatch** - delegate must match exactly
5. **Not calling base._Ready()** - in inheritance chains
6. **Blocking async with `.Result`** - always `await`
7. **Cyclic references** - Godot doesn't GC cycles across C#/GDScript boundary

## Migration Checklist (GDScript → C#)
- [ ] Add `[Export]` to all `@export` vars
- [ ] Replace `signal` with `[Signal]` delegate
- [ ] Change `await X` to `await ToSignal(...)` or `Task`
- [ ] Update `_ready()` → `public override void _Ready()`
- [ ] Update `_process(delta)` → `public override void _Process(double delta)`
- [ ] Use `Godot.Collections.Array/Dictionary` for exported collections
- [ ] Add `using Godot;` and `using System;`
- [ ] Check signal connections match delegate signatures