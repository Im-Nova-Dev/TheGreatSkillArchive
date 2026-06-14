# Omarchy Elephant/Walker Launcher Reference

## Architecture
- **Walker** (`walker`): GTK-based application launcher (UI)
- **Elephant** (`elephant`): Data provider daemon with plugin system
- Walker queries Elephant via D-Bus for search results
- Both run as user systemd services

## Config Paths
| Component | Config |
|-----------|--------|
| Walker UI | `~/.config/walker/config.toml` + theme in `~/.config/omarchy/current/theme/walker.css` |
| Elephant core | `~/.config/elephant/*.toml` (calc, clipboard, desktopapplications, symbols, unicode, files, providerlist, todo) |
| Elephant menus | `~/.config/elephant/menus/*.lua` (omarchy_themes, omarchy_background_selector, omarchy_unlocks) |
| Default providers | `/home/nova/.local/share/omarchy/default/walker/` |
| Walker service | `~/.config/systemd/user/app-walker@autostart.service.d/` |
| Elephant service | `elephant.service` (user) |

## Keybindings
Default Omarchy bindings (from `~/.local/share/omarchy/default/hypr/bindings/utilities.conf`):
- `SUPER, SPACE` → Walker app launcher (`omarchy-launch-walker`)
- `SUPER ALT, SPACE` → Omarchy menu (`omarchy-menu`)
- `SUPER SHIFT, SPACE` → Toggle waybar
- `SUPER CTRL, SPACE` → Theme background menu

**Note:** Custom prefixes in Walker config (e.g., `@` for websearch, `=` for calc, `$` for clipboard) can appear as "key bindings" when users type them.

## Debugging Commands
```bash
# List all Elephant providers
elephant listproviders

# Show active keybindings with symbols (Omarchy wrapper)
omarchy-menu-keybindings --print

# Raw Hyprland bindings (JSON)
hyprctl -j binds

# Verify live keyboard options
hyprctl devices -j | jq -r '.keyboards[] | "\(.name): \(.options)"'

# Restart launcher stack
systemctl --user restart elephant app-walker@autostart
```

## Common Pitfalls
1. **CapsLock as Compose (`compose:caps`)**: Key consumed by XKB, never reaches Hyprland for bindings. Shows `modmask: 2` in `hyprctl binds` but doesn't fire.
2. **Walker providers mimic bindings**: Typing "email" in Walker search can launch Hey.com via a provider, looking like a global keybind.
3. **Config precedence**: User `~/.config/hypr/bindings.conf` overrides Omarchy defaults. Always check both.