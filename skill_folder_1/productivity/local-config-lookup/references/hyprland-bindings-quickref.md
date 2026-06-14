# Hyprland Binding Debugging Quick Reference

## Modmask Values (from `hyprctl -j binds`)

| Mask | Modifiers |
|------|-----------|
| 0 | none |
| 1 | SHIFT |
| 2 | CAPSLOCK |
| 4 | CTRL |
| 8 | ALT |
| 64 | SUPER |
| 65 | SUPER+SHIFT |
| 68 | SUPER+CTRL |
| 72 | SUPER+ALT |
| 76 | SUPER+CTRL+ALT |
| 77 | SUPER+SHIFT+CTRL+ALT |

## Key Bindings Inspection Commands

```bash
# All bindings for a specific key (e.g., SPACE)
hyprctl -j binds | jq -r '.[] | select(.key=="SPACE") | "\(.modmask) \(.description) \(.dispatcher) \(.arg)"'

# All bindings with a specific modmask (e.g., SUPER=64)
hyprctl -j binds | jq -r '.[] | select(.modmask==64) | "\(.key) \(.description) \(.dispatcher) \(.arg)"'

# Pretty listing via Omarchy
omarchy-menu-keybindings --print
```

## Keyboard Options (`kb_options`)

| Option | CapsLock Behavior |
|--------|-------------------|
| `compose:caps` | Compose key (Omarchy default) |
| `caps:super` | Extra Super key |
| `caps:swapescape` | CapsLock ↔ Escape |
| `caps:escape` | Escape |
| `caps:ctrl_modifier` | Ctrl when held |

**Verify live state:** `hyprctl devices -j | jq -r '.keyboards[].options'`

## Mouse Button Mapping

```ini
# Right-click from keyboard (dispatcher=pass, arg=mouse:273)
bindd = SUPER, B, Right-click, pass, mouse:273

# Left-click
bindd = SUPER, N, Left-click, pass, mouse:272

# Middle-click
bindd = SUPER, M, Middle-click, pass, mouse:274
```

**Critical:** With `kb_options = compose:caps`, CapsLock is consumed by XKB — Hyprland sees `modmask: 2` but key events never reach it. Must use `caps:super` for CapsLock bindings to fire.

## Trackpad Right-Click (Native, Preferred)

In `~/.config/hypr/input.conf`:

```ini
touchpad {
    click_method = clickfinger  # or clickfinger_behavior = true
}
```

Then: 1 finger = left, 2 fingers = right, 3 fingers = middle.