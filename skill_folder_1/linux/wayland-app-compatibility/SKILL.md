---
name: wayland-app-compatibility
description: "Practical Wayland app compatibility troubleshooting on Arch/Hyprland: detect XWayland fallbacks, fix common app breakage, and verify fixes."
---

# Wayland App Compatibility

## Platform
Linux, Arch-based, Hyprland, Omarchy

## When to use
- An Electron/Java/GTK app only opens as a tiny window, drags poorly, or has no decorations
- Screen sharing, global shortcuts, or clipboard sharing break in one app but not others
- An app reports "Wayland display not found" or falls back to X11 silently
- After a Hyprland or Mesa update, previously working native Wayland apps regress
- You need to decide whether to force XWayland, enable native flags, or change Hyprland rules

## Core concepts
1. **Native Wayland** is preferred. It avoids XWayland overhead, input quirks, and scaling bugs.
2. **XWayland** is the compatibility layer. Apps using X11 toolkits or old Electron run through it.
3. **Per-app overrides** in Hyprland can force XWayland or specific env vars without system-wide changes.
4. **Mesa / libdecor / xdg-desktop-portal** versions often cause regressions after Arch updates.

## Diagnostic workflow

### 1. Confirm whether the app is running natively or under XWayland
Run:
```bash
hyprctl clients
```
Look at the `class`/`title` entries. XWayland windows are often labeled with `Xwayland` or show an `X11` window type in some tooling.

Faster check with xprop if available:
```bash
xprop WM_CLASS
```
Click the suspect window. XWayland windows still respond to xprop. Native Wayland windows may not.

### 2. Scan journal for portal / XWayland warnings
```bash
journalctl --user -u hyprland --since "15 minutes ago" | rg -i "wayland|xwayland|portal|xdg-desktop-portal|electron|gtk|qt"
```
Look for:
- `Failed to connect to portal`
- `XWayland` startup errors or `GLX`
- `libdecor` or `wlroots` warnings

### 3. Check environment flags the app receives
```bash
pgrep -a -f "<app-name-or-executable>"
```
Then inspect env for common toggles:
```bash
cat /proc/<pid>/environ | tr '\0' '\n' | rg -i "wayland|x11|xdg|electron|qt|gtk|scale|backend"
```

## Fixes and per-app configuration

### Force an app to use XWayland
Useful for Electron apps that crash or render badly on Wayland:
```text
hypr
windowrulev2 = xwayland,class:^(electron|code|slack|discord)$
```
Match by exact class using `hyprctl clients` to confirm the class string. Avoid overly broad rules.

### Force native Wayland for Electron
Modern Electron supports Wayland; force it with env:
```text
hypr
windowrulev2 = env[WAYLAND_DISPLAY]:1,env[XDG_BACKEND]:wayland,class:^(electron|code)$
```
Some Electron releases also need:
```text
windowrulev2 = env[ELECTRON_OZONE_PLATFORM_HINT]:auto,class:^(electron|code)$
```

### Screen sharing / remote desktop
Needs `xdg-desktop-portal` and `xdg-desktop-portal-hyprland`:
```bash
pacman -Q xdg-desktop-portal xdg-desktop-portal-hyprland
```
If missing or stale:
```bash
sudo pacman -S xdg-desktop-portal xdg-desktop-portal-hyprland
```
After install, restart the portal and the app. If Chrome/Chromium still fails, also ensure:
```text
hypr
windowrulev2 = allow_exclusive_zone,class:^(chromium|google-chrome)$
```

### Global shortcuts / keyboard grab issues
Wayland restricts global grabs. Apps like Barrier/Synergy, custom hotkey daemons, or screen recorders may need:
```text
hypr
windowrulev2 = nofocus,class:^(barrier|synergy)$
windowrulev2 = pin,class:^(obs|obsidian)$   # only if sticky/always-on-top behavior is desired
```
For apps that must stay visible, use `pin` or `stayfocused` sparingly; they interfere with workspace switching.

### Clipboard / primary selection weirdness
Install and enable a clipboard manager that speaks Wayland:
```bash
sudo pacman -S clipman
```
Then start it in your Hyprland autostart:
```text
hypr
exec-once = clipman
```
If clipboard is empty after app close, ensure the app isn't disabling clipboard portals via sandbox flags (Flatpak/Snap).

### Scaling / fractional scaling artifacts
Fractional scaling can make XWayland apps blurry. If an app looks wrong:
1. Confirm it is XWayland with `hyprctl clients`.
2. If the app supports native Wayland, prefer native over XWayland scaling.
3. If forced XWayland is required, accept integer scaling for that app if possible:
   ```text
   hypr
   windowrulev2 = size 1280 720,class:^(problem-app)$
   ```

## Recovery workflow
1. Switch to a TTY if the compositor is unresponsive: `Ctrl+Alt+F2`
2. Move or rename the rule-heavy config section to isolate the regression:
   ```bash
   cp ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf.bak
   ```
3. Boot Hyprland with a minimal config fragment if needed.
4. Reintroduce one rule at a time, reloading with `hyprctl reload` after each.
5. Capture evidence for recurring bugs:
   ```bash
   journalctl --user -u hyprland --since "10 minutes ago" > ~/hyprland-evidence/journal.txt
   ```

## Verification
- `hyprctl clients` shows the target app without an XWayland classification when native is intended
- Screen sharing in the app successfully enumerates displays/windows
- Clipboard copy/paste works across the app and other Wayland windows
- Scaling remains sharp after `hyprctl reload`
- No new `Invalid parameters` or `XWayland` errors in `journalctl --user -u hyprland`

## Common pitfalls
- Forcing all Electron apps to XWayland via a broad regex hides regressions and increases memory use; prefer per-class fixes
- Mixing `windowrule` with `windowrulev2` leaves stale rules active; only use `windowrulev2` and `layerrulev2`
- Assuming XWayland works perfectly on fractional scaling; blur and input offsets are common at non-integer scales
- Installing `xdg-desktop-portal-gtk` alongside `xdg-desktop-portal-hyprland` can cause portal conflicts; prefer the Hyprland portal on Arch
- Forgetting to restart the portal after updates: `systemctl --user restart xdg-desktop-portal.service xdg-desktop-portal-hyprland.service`

## Post-resume / display-change regressions

Symptom: after suspend/resume, docking/undocking, or changing external displays, pointer moves but clicks don’t register, or windows don’t receive focus.

1. Quick recovery:
```bash
hyprctl reload
```
If that doesn’t help, restart Hyprland:
```bash
systemctl --user restart hyprland
```
Then log back in; this creates a fresh compositor instance.

2. If pointer events are lost on only one screen:
- Disconnect/reconnect that monitor, or
- Switch workspace, move the active window with `hyprctl dispatch movecurrent`, then return

3. If the issue reappears after every resume:
- Check whether you’re using a display manager or direct `exec Hyprland` login; direct autologin + suspend with HiDPI/external displays is the most common risk factor
- Verify no duplicate outputs are reported:
```bash
hyprctl monitors
```
Duplicate/ghost monitors can break input routing; if present, disable the bogus port in `hyprland.conf` or add an explicit `monitor` stanza for the actual outputs

4. If clicks are broken only on the laptop screen after docking:
- Set the laptop output explicitly in config
- Confirm dock/port events are sane:
```bash
udevadm monitor --udev
```

## References
- Arch Wiki: Wayland, XWayland, xdg-desktop-portal
- Hyprland Wiki: Variables, Window Rules
- Related skills: `hyprland-logging-and-evidence`, `wayland-hyprland-desktop`, `arch-troubleshooting`
