---
name: hyprland-wallpaper
title: Hyprland Wallpaper Management
description: Diagnose missing/blank wallpapers on Hyprland and set per-output wallpapers using swaybg, including persistent autostart config updates.
---

# Hyprland Wallpaper Management

Use this skill when:
- wallpapers are missing, black, or need to be changed on a Hyprland/Omarchy setup that uses `swaybg`; OR
- Hyprland fails to start, shows a blank screen, drops to a tty, or immediately returns to the display manager.

## Hyprland not starting / blank screen on launch

1. Distinguish "no compositor" from "compositor running without wallpaper"
   - No cursor / black terminal-only = Hyprland likely didn't start.
   - Cursor tiling but no wallpaper = wallpaper daemon problem.

2. Check config syntax
   - Run: `hyprctl reload`
   - Return code 0 + `OK` means config loads.
   - Nonzero + `⚠️` means a syntax/parse error; edit `~/.config/hypr/hyprland.conf` to fix.

3. Inspect logs
   - Run: `journalctl --user -u hyprland.service -b --no-pager -n 200`
   - Run: `journalctl -b --user -u swaybg -n 100`
   - Look for GL errors, missing module `wlroots`, segfaults, or XDG_RUNTIME_DIR misconfig.

4. Common Arch fixes
   - Ensure GPU drivers: `mesa`, `xf86-video-amdgpu`, `xf86-video-nouveau`, `nvidia`, etc.
   - Ensure `wayland` and `xorg-xwayland` are installed.
   - Ensure EGL/Wayland libs are present (`libgl`, `libdrm`, `libxkbcommon`, `qt5-wayland`/`qt6-wayland`).
   - If using NVIDIA: enable modesetting and kernel modeset (see ArchWiki Hyprland section).

5. Conf path and naming
   - Use `hyprland`, not `Hyprland`, when launching from TTY.
   - If multiple monitors stop working, test with `hyprctl monitors all` to confirm detection.

## Steps for wallpaper issues

1. Identify connected outputs
   - Run: `hyprctl monitors`
   - Note output names like `DP-1`, `DP-2`, `HDMI-A-1`.

2. Check current wallpaper state
   - Check running swaybg processes: `ps aux | grep swaybg | grep -v grep`
   - If nothing is running, wallpaper will appear black/blank.
   - If multiple swaybg processes exist per monitor, there may be stale/duplicate daemons conflicting. Kill them with `pkill swaybg` before applying new wallpapers.

3. Inspect current wallpaper sources
   - Check `~/.config/hypr/autostart.conf` for existing `swaybg` lines.
   - Check `~/.config/omarchy/current/background` for theme background symlink.
   - Verify target images exist with `ls -la <path>`.

4. Set wallpapers per output
   - Use: `hyprctl dispatch exec "swaybg -o <OUTPUT> -i <IMAGE> -m fill"`
   - Common modes: `fill`, `fit`, `center`, `stretch`, `tile`.

5. Make it persistent
   - Write matching `exec-once` lines into `~/.config/hypr/autostart.conf` in this form:
     `exec-once = swaybg --output <OUTPUT> --image <IMAGE> --mode fill`

## Omarchy-specific background tracking

- On Omarchy, the active background is also tracked via:
  `~/.config/omarchy/current/background`
  This path is a symlink to the current theme/image. When setting a wallpaper manually, also update or replace this symlink so other Omarchy tooling stays in sync.
- Preferred Omarchy-native way to set background:
  `omarchy-theme-bg-set <path-to-image>`
  This updates the symlink, kills stale `swaybg`, and restarts it with the new image.
- For per-monitor setups, Omarchy's `omarchy-theme-bg-set` takes a single image. Use direct `swaybg -o <OUTPUT> -i <IMAGE>` calls per monitor when you need different images per output, and still update the `~/.config/omarchy/current/background` symlink to one of the chosen images.

## Common Pitfalls

- `hyprctl outputs` is invalid; use `hyprctl monitors`.
- Output names from xorg (`HDMI1`, `DP-0`) may differ from Hyprland names (`HDMI-A-1`, `DP-1`); always read `hyprctl monitors` first.
- `swaybg` may not be installed; verify with `command -v swaybg`.
- A theme symlink can point to a missing file; verify with `ls -la`.
- Changing `autostart.conf` alone does not update the current running wallpaper. `hyprctl reload` does not restart `exec-once` commands. After editing `autostart.conf`, also restart the wallpaper daemon: `pkill swaybg` then start fresh `swaybg --output <OUTPUT> --image <IMAGE> --mode fill` commands so the new config is actually live.
- Omarchy can leave duplicate background daemons running side-by-side with new ones; keep the daemon set to one process per monitor.

## One-liner examples

```bash
hyprctl dispatch exec "swaybg -o DP-1 -i /path/to/image.jpg -m fill"
```
```bash
pkill swaybg || true
```