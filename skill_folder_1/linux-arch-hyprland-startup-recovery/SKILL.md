---
name: linux-arch-hyprland-startup-recovery
---

# Hyprland / Omarchy Startup Recovery

## Overview

This skill addresses a common Arch Linux / Omarchy failure mode: Hyprland (or another Wayland compositor used by Omarchy) does not start after boot, immediately crashes, or leaves the user at a TTY / display-manager loop. Typical triggers include a partial system upgrade, a Hyprland config syntax error, a missing GPU driver, or an incompatible package update.

Target platform: Arch Linux with Omarchy or manual Hyprland setups.

## Diagnostics

Use these checks in order on a TTY (Ctrl+Alt+F2…F6).

1. Confirm whether Hyprland can start manually:
   `Hyprland`

2. Inspect Hyprland logs for the immediate cause:
   `journalctl --user -u hyprland -b -e`
   or, if started directly:
   `journalctl --since "5 min ago" | rg -i hyprland`

3. Check XDG runtime / display availability:
   `echo $XDG_RUNTIME_DIR`
   `ls -l /run/user/$(id -u)`

4. Verify Wayland support is actually present:
   `loginctl show-session $(loginctl | awk '/tty/ {print $1}' | head -n1) -p Type`
   and check GPU acceleration in Wayland:
   `glxinfo | grep "OpenGL renderer"`  (from mesa-utils)
   ` vainfo`  (from libva-utils)

5. Look for broken packages or partial upgrades (Arch-specific):
   `pacman -Qk`
   `pacman -Dk`
   `ls /var/log/pacman.log | xargs grep -i error | tail -n 50`

6. Confirm Hyprland configuration parses:
   `hyprctl reload`
   If it errors, the issue is config syntax:
   `grep -R " " ~/.config/hypr/*.conf ~/.config/hypr/conf.d`

## Fixes

Apply these in approximate order of lowest risk → highest risk.

### A. Roll back or revalidate config

- Move the current config aside:
  `mv ~/.config/hypr ~/.config/hypr.bak`
- Start Hyprland again:
  `Hyprland`
- If it starts, the issue is Hyprland config. Migrate changes from the backup one stanza at a time.

### B. Repair display-manager / seat permissions

If using a DM ( greetd, GDM, SDDM ):

1. Ensure display manager is a Wayland-enabled session.
2. Check seat permissions:
   `loginctl show-session $(loginctl | awk '/seat/ {print $1}' | head -n1) -p Type`
3. For greetd, inspect:
   `cat /etc/greetd/config.toml`

### C. Restore missing GPU / Wayland dependencies

Common after partial upgrades:

- Nvidia:
  `sudo pacman -S --asdeps nvidia-dkms nvidia-utils egl-wayland`
- AMD/Intel:
  `sudo pacman -S --asdeps mesa libva-mesa-driver vulkan-radeon vulkan-intel`
- Remove stale mesa cache:
  `sudo rm -rf /var/cache/mesa/*`

### D. Force a known-good user runtime

Sometimes /run/user/$UID is corrupted or mounted incorrectly:

1. Log out of all sessions.
2. From a root TTY:
   `umount /run/user/$(id -u <your-user>) 2>/dev/null || true`
   `rm -rf /run/user/<your-user:1024>/.cache/hypr`
   `systemctl restart systemd-logind`
3. Log back in.

### E. Handle Arch partial upgrade lock

If pacman reported a partial upgrade, force database sync and reinstall:
`sudo pacman -Syu`

If that fails due to held packages:
`sudo pacman -S --overwrite '*' hyprland`

## Verification

Run these checks after applying fixes and confirm they succeed:

1. Hyprland starts without crashing:
   `Hyprland`  from TTY, or log in via DM.
2. Wayland session is active:
   `echo $XDG_SESSION_TYPE`  → should print `wayland`
3. GPU is being used for rendering:
   `hyprctl clients`  and `hyprctl info`
4. No relevant errors in current boot log:
   `journalctl --since "3 min ago" | rg -i hyprland`  should show empty/clean.
5. DM login loop has stopped:
   reboot once and confirm GUI login succeeds.

## References

- https://wiki.hypr.land/
- https://wiki.archlinux.org/title/Hyprland
- https://wiki.archlinux.org/title/Systemd
- https://www.ssp.sh/blog/linux-omarchy-the-good-bad-and-fixable/
