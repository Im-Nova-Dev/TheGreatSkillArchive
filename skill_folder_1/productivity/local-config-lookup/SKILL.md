---
name: local-config-lookup
title: Local Config Lookup
description: Fast, low-token lookup of local config values and keybindings. Use for "what does X do", "where is Y set", "show me Z binding" questions about Hyprland, kitty, waybar, shell, etc.
---

## Core protocol

1. **Try the domain CLI first.** Most tools ship a query command that returns only the answer.
   - Hyprland keybinds: `hyprctl binds` (also `hyprctl -j binds` for JSON)
   - Omarchy Hyprland bindings: `omarchy-hyprland-bindings` / `omarchy-menu-keybindings --print`
   - Shell config (bash/zsh): `cat ~/.bashrc` / `cat ~/.zshrc` only if needed
   - Kitty keybinds: `grep -n "map" ~/.config/kitty/kitty.conf`
   - Waybar: inspect `~/.config/waybar/config`

2. **Path-scope every filesystem search.** Never grep the entire `~/.config` directory. Target the known config path (e.g. `~/.config/hypr/bindings.conf`).

3. **Use grep, not file reads.** `grep -n "pattern" /path` returns only matching lines. Only read full files if grep returns nothing.

4. **Stop at the first file that answers the question.** Do not open `hyprland.conf`, theme files, or sibling configs after finding the answer in `bindings.conf`.

5. **Avoid minified/binary dirs.** Never recursive-scan `~/.config/{chromium,google-chrome,Code,spotify,lib}` or any directory containing cache/databases. These blow up token usage and return noise.

6. **Do not read the same config twice in one task.** Cache the result mentally and query against it.

7. **Never claim a binding is "free" or "assigned" without searching the user's actual `~/.config/hypr/bindings.conf` first.** Omarchy default bindings are not authoritative if the user has local overrides. Search both default and user bindings before saying a key combination is available.

8. **Keyboard-to-mouse-button mapping** — Hyprland `pass` dispatcher with `mouse:273` emits a real mouse button event that applications receive natively. Correct syntax:
```ini
bindd = SUPER, B, Right-click, pass, mouse:273
```
This works when the modifier key reaches Hyprland. **Pitfall:** `kb_options = compose:caps` (Omarchy default) makes CapsLock a Compose key consumed by XKB — Hyprland sees modmask 2 but never gets the key event. Fix: `kb_options = caps:super` then `hyprctl reload`.

**Modmask reference (from `hyprctl -j binds`):**
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

For trackpads, prefer libinput `click_method = clickfinger` in `~/.config/hypr/input.conf` over synthetic events when possible.

**See also:** `references/hyprland-bindings-quickref.md` — modmask table, inspection commands, kb_options table, and mouse button mapping syntax.
