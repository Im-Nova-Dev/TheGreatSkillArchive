---
name: omarchy-hyprland-post-update-fix
description: "Use when Hyprland fails after an Omarchy update, especially errors referencing windows.conf, looknfeel.conf, apps/*.conf, or rule migration. Covers config drift, incomplete updates, and windowrulev2/layerrulev2 migration."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [omarchy, hyprland, arch, post-update, wayland, config-migration]
    related_skills: [arch-troubleshooting, wayland-hyprland-desktop, omarchy-inspection]
---

# Omarchy Hyprland Post-Update Fix

## Overview
After Omarchy updates, Hyprland can fail to launch or flood logs due to common causes:
- Hyprland config syntax drift across versions
- Partial updates from interrupted `omarchy-update` or GUI-update sudo timeouts
- Missing or malformed `windows.conf` or `looknfeel.conf` after package migration
- Stale regex patterns or renamed config keys in user customizations

This skill provides targeted diagnostics and fixes so the user can recover the desktop without a full reinstall.

## When to Use
- Hyprland fails to start after `omarchy-update`
- Errors reference `windows.conf`, `looknfeel.conf`, or `apps/*.conf`
- Users see messages about unknown config options, invalid parameters, or old rule syntax
- Desktop starts but is blank with no wallpaper, waybar, or panels
- Theme assets appear missing or incomplete after switching or updating themes

## Recovery Workflow

Follow the steps in order. Stop once the desktop is fully restored.

### Step 1 — Capture the Failure Evidence

Switch to a TTY immediately if the GUI is stuck or crashing.

```bash
# TTY2 as a safe fallback
sudo systemctl restart getty@tty2
# Then log in on Ctrl+Alt+F2
```

Re-run Hyprland from the TTY to capture real error output:

```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
Hyprland 2>&1 | tee /tmp/hyprland-launch.log
```

Look for these failure signals:

| Signal | Likely Cause |
|--------|--------------|
| `config option ... does not exist` | Config syntax drift |
| `Invalid parameters` | Malformed config block |
| `unknown rule` or `windowrulev2` | Renamed rule keywords |
| `opacity 0.97 0.9` without `match:` | Pre-0.53 rule format |
| `windows.conf` / `looknfeel.conf` missing | Partial update or theme switch |
| Desktop is blank but Hyprland stays running with no obvious config error | Active theme inactive, missing parent theme assets, or overridden `~/.config/omarchy/active` |

Scan logs for patterns:

```bash
rg -n "config option|Invalid parameters|suppress_event_maximize|mscon_focus_under_fullscreen|no_focus on|hyprland\.conf|windows\.conf|looknfeel\.conf" \
  ~/.local/share/omarchy ~/.config/hypr/ /tmp/hyprland-launch.log 2>/dev/null | tail -n 80
```

### Step 2 — Determine Root Cause

#### Indicator A: Config Syntax Drift
If logs mention renamed options or rule keywords, your local config needs migration.

Known migration points:
- `suppress_event_maximize` → removed; use `windowrule`/`layerrule` instead
- `mscon_focus_under_fullscreen` → config key renamed
- `opacity` without `match:` → needs modern `windowrulev2` syntax
- `layerrule` → rename to `layerrulev2`
- `windowrule` → rename to `windowrulev2`

#### Indicator B: Incomplete / Partial Update
If the update was interrupted or GUI-update sudo timed out:

```bash
# Compare reported vs installed package state
omarchy --version
pacman -Q omarchy

# Force a clean re-sync
sudo pacman -Syy
omarchy-update

# If GUI processes were interrupted, verify system coherence
sudo pacman -Qkk 2>&1 | tail -n 40
```

#### Indicator D: Blank Desktop / Theme Not Loading
If Hyprland stays running but shows a blank desktop, no waybar, and no wallpaper:

```bash
# Check what theme is active and whether the link resolves
readlink -f ~/.config/omarchy/active || true
ls -la ~/.config/omarchy/active 2>/dev/null || true
ls -la ~/.local/share/omarchy/themes/ 2>/dev/null

# Identify whether parent assets exist
THEME_DIR=$(readlink -f ~/.config/omarchy/active 2>/dev/null || echo ~/.local/share/omarchy/themes/active/test_theme)
[ -d "$THEME_DIR" ] && ls -la "$THEME_DIR"/hypr/ || ls -la ~/.local/share/omarchy/themes/active/test_theme/hypr/ 2>/dev/null || true

# Look for absent generator/config entries in journal
journalctl --user -u hyprland --since "-10 minutes" | rg -i "not found|missing|omarchy|wallpaper|waybar|screenshot" || true
```

Common causes:
- `~/.config/omarchy/active` symlink is broken, points to a removed/renamed theme, or points to an empty partial theme directory
- Theme name was spelled differently between `~/.config/omarchy/` and `~/.local/share/omarchy/themes/`
- `hypr/` subfolder is missing in the theme or lacks the expected generator assets

#### Indicator C: Missing Theme Files
If `windows.conf` or `looknfeel.conf` is absent from the active theme:

```bash
ls -la ~/.local/share/omarchy/themes/active/hypr/
# Expected: at least hyprland.conf, plus optional windows.conf, looknfeel.conf
```

If missing, the theme did not migrate fully.

### Step 3 — Apply Targeted Fixes

#### Fix 1 — Complete or Re-run the Update
Only when Indicator B is present.

```bash
# From TTY, finish pending package operations
sudo pacman -Su --noconfirm
omarchy-update
```

After completion:

```bash
systemctl reboot
```

#### Fix 2 — Migrate Rule Syntax for Hyprland 0.53+
Only when Indicator A is present.

Modern Omarchy uses `windowrulev2` and `layerrulev2`. Convert shipped and local configs:

```bash
# Migrate shipped default app rules
sed -i 's/^layerrule = /layerrulev2 = /g' ~/.local/share/omarchy/default/hypr/apps/*.conf
sed -i 's/^windowrule = /windowrulev2 = /g' ~/.local/share/omarchy/default/hypr/apps/*.conf

# Migrate user input.conf if needed
if [ -f ~/.config/hypr/input.conf ]; then
  sed -i 's/^windowrule = /windowrulev2 = /g' ~/.config/hypr/input.conf
fi
```

Fix `opacity` blocks that lack `match:`:

```bash
# Example before:
#   opacity 0.97 0.9, class:*
# After:
#   windowrulev2 = opacity 0.97 0.9, match:class:*

# Convert simple opacity lines in user configs carefully:
rg -n "^[[:space:]]*opacity [0-9.]+ [0-9.]+" ~/.config/hypr/*.conf ~/.local/share/omarchy/default/hypr/apps/*.conf 2>/dev/null
```

For each match, wrap with `windowrulev2 = ` and add `match:` before the first non-opacity token.

Refresh:

```bash
hyprctl reload
```

#### Fix 3 — Repair Missing Theme Configs
Only when Indicator C is present.

1. Open the Omarchy menu from a TTY or fallback session:

```bash
omarchy-menu
```

2. Navigate to `Style > Theme`, then select a different theme.
3. Reboot:

```bash
systemctl reboot
```

If `omarchy-menu` cannot launch, manually copy a known-good theme:

```bash
# List available themes
ls ~/.local/share/omarchy/themes/

# Activate one by linking
OMARCHY_THEME=<theme-name>
mkdir -p ~/.config/omarchy
ln -sf ~/.local/share/omarchy/themes/$OMARCHY_THEME ~/.config/omarchy/active
```

#### Fix 3b — Rebuild a Known-Good Active Theme Link for Blank Desktops
Only when Indicator D is present.

Workflow:
1. Inspect the active theme path and available theme directories:

```bash
readlink -f ~/.config/omarchy/active || true
ls -la ~/.local/share/omarchy/themes/ 2>/dev/null || true
```

2. Confirm the user-intended theme is installed and that its `hypr` folder contains expected files:

```bash
OMARCHY_THEME=<observed-theme-name>
ls -la ~/.local/share/omarchy/themes/$OMARCHY_THEME 2>/dev/null || true
ls -la ~/.local/share/omarchy/themes/$OMARCHY_THEME/hypr 2>/dev/null || true
```

3. If the theme directory is missing, pick a known-good alternative and rebuild the active symlink, targeting the theme directory itself rather than a theme assets subfolder:

```bash
OMARCHY_THEME=<known-good-theme-name>
mkdir -p ~/.config/omarchy
ln -sf ~/.local/share/omarchy/themes/$OMARCHY_THEME ~/.config/omarchy/active
```

4. Reload Hyprland and verify wallpaper/waybar reappear:

```bash
hyprctl reload
```

#### Fix 4 — Fix Picture-in-Picture Regex Patterns
Older configs may contain `{0,1}` regex quantifiers which newer Hyprland rejects.

Check:

```bash
rg -n '\{0,1\}' ~/.local/share/omarchy/default/hypr/apps/pip.conf ~/.config/hypr/*.conf 2>/dev/null
```

Replace with `?` (same regex semantics):

```bash
# Before:
#   windowrule = tag +pip, title:(Picture.{0,1}in.{0,1}[Pp]icture)
# After:
#   windowrulev2 = tag +pip, title:(Picture.?in.?[Pp]icture)
```

#### Fix 5 — Restore User Customizations During Theme Changes
If a theme switch overwrote `~/.config/hypr/`:

1. Verify `hypr` directory is present:

```bash
ls -la ~/.config/hypr/
```

2. Re-link or re-create user configs from the Omarchy scaffold:

```bash
cp -a ~/.local/share/omarchy/default/hypr ~/.config/hypr
# Then re-apply any user customizations
```

### Step 4 — Verify Recovery

1. Launch Hyprland and confirm desktop, wallpaper, and waybar load:

```bash
Hyprland
```

2. Check for residual config errors over 30 seconds:

```bash
journalctl --user -u hyprland --since "30 seconds ago" | tail -n 80
```

3. Confirm update tree is consistent:

```bash
omarchy-update && echo UPDATE_OK
```

## Common Pitfalls

1. **Fixing shipped defaults without updating local copies.** Omarchy ships separate defaults in `~/.local/share/omarchy/default/hypr/`. Always update both shipped defaults and user-local configs in `~/.config/hypr/`.

2. **Using `sed` without preview.** Before bulk replacing config syntax, preview what will change:

```bash
rg -n "^(windowrule|layerrule) = " ~/.local/share/omarchy/default/hypr/apps/*.conf ~/.config/hypr/*.conf 2>/dev/null
sed -n 's/^windowrule/windowrulev2/p' ~/.config/hypr/*.conf
```

3. **Forgetting `match:` in new `windowrulev2` lines.** The new format requires an explicit `match:` selector. Moving the old rule body verbatim after the `=` often misses this requirement.

4. **Ignoring TTY fallback.** If the GUI is stuck in a login loop or blank screen, switch to TTY immediately. Trying to read logs from a stuck session wastes time and may overwrite the log buffer.

## Verification Checklist

- [ ] Hyprland reaches the desktop from `Hyprland` command
- [ ] Waybar appears and shows expected modules/theme
- [ ] Wallpaper and opacity rules apply correctly
- [ ] No config-option errors in `journalctl --user -u hyprland` for 60 seconds after startup
- [ ] `omarchy-update` completes without transaction errors
- [ ] User customizations in `~/.config/hypr/` are preserved or restored

## References

- Omarchy release notes for version-specific migration guidance
- Hyprland 0.53+ Window Rules docs on `windowrulev2` and `layerrulev2`
- Related Hermes skills: `arch-troubleshooting`, `wayland-hyprland-desktop`, `omarchy-inspection`, `hyprland-logging-and-evidence`
