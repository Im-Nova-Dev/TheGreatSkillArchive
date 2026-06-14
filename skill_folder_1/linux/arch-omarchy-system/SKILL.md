---
name: arch-omarchy-system
description: "Unified Arch/Omarchy system management: troubleshooting (boot, Hyprland, pacman keyring), desktop config (fonts, themes, cursors), shell/terminal config (zsh/bash, kitty/alacritty/ghostty/foot), system inspection (Hyprland, Waybar, Neovim, systemd, themes). Use for any Arch/Omarchy configuration, troubleshooting, or inspection task."
version: 1.0.0
category: linux
tags: [arch, omarchy, hyprland, troubleshooting, desktop-config, shell, terminal, systemd, waybar, neovim]
---

# Arch/Omarchy System Management

Unified class-level skill covering all Arch Linux and Omarchy system operations. Replaces 4 narrow skills: `arch-troubleshooting`, `linux-desktop-config`, `omarchy-shell-terminal-config`, `omarchy-system`.

## When to Use

- Boot/initramfs failures, Hyprland startup issues, pacman keyring/signature errors
- Changing fonts, themes, cursors, icons across the desktop
- Shell (zsh/bash) and terminal (kitty/alacritty/ghostty/foot) configuration
- Inspecting/editing Omarchy configs: Hyprland, Waybar, Neovim, systemd user units, themes
- Package management, updates, migrations, hooks

---

## Decision Guide

| Task | Section |
|------|---------|
| Boot failure, initramfs, EFI, hibernate | **Boot & Initramfs Recovery** |
| Hyprland won't start, blank/frozen screen | **Hyprland Startup Recovery** |
| `pacman` key errors, GPGME, unknown trust | **Pacman Keyring Recovery** |
| Partial/aborted `pacman -Syu` or `omarchy-update` | **Interrupted Update Recovery** |
| Fonts, themes, cursors, icons system-wide | **Desktop Configuration** |
| Shell aliases, terminal fonts, keybindings | **Shell & Terminal Configuration** |
| Inspect Hyprland, Waybar, Neovim, systemd configs | **System Inspection & Config Truth** |
| Per-monitor wallpapers (swaybg) | **Multi-Monitor Wallpaper** |
| Theme switching, hooks, migrations | **Theming & Migrations** |

---

## 1. Boot & Initramfs Recovery

### Verification Steps

```bash
# Confirm EFI entry and boot order
bootctl status
bootctl list

# Check initramfs
mkinitcpio -P
ls -la /boot/

# Verify boot loader
bootctl install
systemctl status systemd-boot-update.service
```

### Common Fixes

- Regenerate initramfs: `mkinitcpio -P`
- Reinstall bootloader: `bootctl install`
- Fix `/boot` vs `/efi` mount: check `findmnt /boot` and `lsblk -f`
- Hibernate resume UUID: ensure `RESUME=UUID=...` in `/etc/mkinitcpio.conf` matches swap UUID from `lsblk`

---

## 2. Hybrid Graphics / Hyprland Startup Recovery

### Detection Signals

- `journalctl -0 --grep -i "nvidia|amdgpu|drm|egl|gles"` shows delayed nvidia load
- `hyprland` fails with `Unable to initialize EGL` / `Failed to create backend`
- `lspci -k | grep -EA3 'VGA|3D'` shows wrong driver owning display
- `nvidia-smi` works from TTY but Hyprland shows no monitors

### Fix Sequence (AMD Primary)

```bash
# 1. Identify card slot order
lspci -k | awk '/VGA/{p=1} p && /Kernel driver in use/{print NR": "$0; p=0}'
lspci -k | awk '/3D/{p=1} p && /Kernel modules:/{print NR": "$0; p=0}'

# 2. Force AMD as DRM master if NVIDIA initialized first
cat >/etc/modprobe.d/amd-primary.conf <<'EOF'
options amdgpu drm_kms_helper=1
options nvidia NVreg_UsePageAttributeTable=0 NVreg_EnablePCIeGen3=0
EOF

# 3. Rebuild initramfs with explicit module order
mkinitcpio -P

# 4. Regenerate boot entries
bootctl update
# grub-mkconfig -o /boot/grub/grub.cfg  # if using GRUB

# 5. Verify firmware boot entry
bootctl list

# 6. Reboot and verify from TTY
nvidia-smi
glxinfo | grep "OpenGL renderer"
```

### Verification

- `amdgpu` as `Kernel driver in use` for display adapter
- No fatal DRM/KMS errors in `journalctl`
- `hyprctl devices` shows AMD as primary

---

## 3. Pacman Keyring Recovery

### Safe Rules

- Never run `pacman -Syu` blindly when signature errors appear; repair keys first
- Never edit `/etc/pacman.d/gnupg/gpg.conf` without recording the exact keyserver change

### Fix Sequence

```bash
# 1. Full keyring reset
rm -rf /etc/pacman.d/gnupg
pacman-key --init
pacman-key --populate archlinux

# 2. Optional: refresh keyserver trust
pacman-key --refresh-keys --keyserver hkps://keys.openpgp.org

# 3. Reinstall keyring package
pacman -S --asdeps archlinux-keyring
# Or from live ISO if local trust is broken

# 4. Verify key trust
pacman-key --list-sigs 'Arch Linux Automatic keyring'
pacman-key --list-keys | grep -C2 "ultimate\|full"
```

### Verification

- `pacman -Sy` completes without signature warnings
- `pacman-key --list-sigs` shows expected key IDs

---

## 4. Interrupted Update Recovery

### Pacman Partial Update

```bash
# 1. Remove lock if stuck
rm -f /var/lib/pacman/db.lck

# 2. Forward repair (preferred over downgrade)
pacman -Syu

# 3. If conflicting files, force overwrite
pacman -S --overwrite '*' <pkg>

# 4. Verify
pacman -Qk $(pacman -Qnq)  # no missing files
pacman -Syu  # completes cleanly
```

### Omarchy Update Interrupted

```bash
# 1. Finish update after clean boot
omarchy-update

# 2. If GUI packages interrupted, verify Hyprland recovery (Section 2)
# 3. If kernel/initramfs/bootloader interrupted
mkinitcpio -P && bootctl install
```

### Verification

- `omarchy-version` matches expected release
- `journalctl` clean for Hyprland/KWin/gdm
- `bootctl status` valid

---

## 5. Desktop Configuration (Fonts, Themes, Cursors, Icons)

### Core Principle

When user asks "can you do it for me", perform changes directly. Short CLI output preferred.

### Common Config Locations

- `~/.config/` — user configs
- `~/.config/omarchy/current/theme/` — Omarchy theme overrides
- `~/.local/share/fonts/` — user fonts
- `/usr/share/omarchy/themes/*` — Omarchy themes

### Font Changes

```bash
# System font (Omarchy)
omarchy-font-set "Mononoki Nerd Font"

# User font install
sudo pacman -S ttf-mononoki-nerd
fc-cache -fv
```

### Theme Packaging (for GitHub release)

```
repo/
├── theme/
│   ├── kitty/
│   ├── hypr/
│   ├── waybar/
│   └── ...
└── README.md  # preview, palette, dependencies, installation, quirks
```

Install: `omarchy-theme-install https://github.com/user/repo`

### Pitfalls

- Match existing quoting style (`font_family X` vs `family = "X"`)
- Restart apps after config changes
- AUR fonts need sudo; user fonts don't
- Don't teach manual `cp` when `omarchy-theme-install` exists
- Avoid spaces in theme repo directories

---

## 6. Shell & Terminal Configuration

### Bash vs Zsh Aliases

**Bash** (omarchy default): `~/.local/share/omarchy/default/bash/aliases`
```bash
alias ls='eza -lh --group-directories-first --icons=auto'
alias lsa='ls -a'
```

**Zsh** (no default aliases): Add to `~/.zshrc` after `source $ZSH/oh-my-zsh.sh`
```zsh
alias ls='eza -lh --group-directories-first --icons=auto'
alias lsa='ls -a'
alias ll='ls -l'
alias la='ls -a'
alias lt='eza --tree --level=2'
```

### Terminal Font Config

Omarchy manages font family via `omarchy-font-set`. Font size per-terminal:

| Terminal | Config File | Font Size Key |
|----------|-------------|---------------|
| kitty | `~/.config/kitty/kitty.conf` | `font_size 9.0` |
| alacritty | `~/.config/alacritty/alacritty.toml` | `size = 9` |
| ghostty | `~/.config/ghostty/config` | `font-size = 9` |
| foot | `~/.config/foot/foot.ini` | `font=Mononoki Nerd Font:size=9` |

### Font Resize Keybindings

- **kitty**: `Ctrl+Shift+=` / `Ctrl+Shift+-` / `Ctrl+Shift+Backspace` (default)
- **alacritty**: NONE by default — add to `keyboard.bindings` in `alacritty.toml`
- **ghostty**: `Ctrl+Shift+=` / `Ctrl+-` / `Ctrl+0` (default)
- **foot**: `Ctrl+Shift+Plus` / `Ctrl+Shift+Minus` / `Ctrl+Shift+0` (default)

### Oh My Posh

Only affects prompt. Does NOT set aliases, fonts, or keybindings. If aliases "lost" after installing Oh My Posh, they were never there — add manually.

### Restore Omarchy Defaults

```bash
omarchy-refresh-config zsh/zshrc
omarchy-refresh-config kitty/kitty.conf
omarchy-refresh-config alacritty/alacritty.toml
```

---

## 7. System Inspection & Config Truth

### Inventory First, Never Assume

```bash
# User configs
ls ~/.config/**

# Shipped defaults
ls /usr/share/omarchy/config/**
ls ~/.local/share/omarchy/config/

# Theming
ls /usr/share/omarchy/themes/*
ls ~/.config/omarchy/current/theme/*

# User services
systemctl --user list-units
ls ~/.config/systemd/user/*

# Omarchy commands
/usr/share/omarchy/bin/omarchy

# Installed packages
yay -Qq
cat /usr/share/omarchy/install/omarchy-base.packages
cat /usr/share/omarchy/install/omarchy-other.packages
```

### Reload/Restart Patterns

| Component | Reload Command |
|-----------|----------------|
| Hyprland | `hyprctl reload` |
| Waybar | `systemctl --user restart waybar` or kill + restart |
| swayosd | `systemctl --user restart swayosd-server.service` |
| mako | `mako` (restart) |
| User systemd | `systemctl --user daemon-reload && systemctl --user restart <unit>` |
| Full session | `uwsm-app restart` or logout/login |

### Config Formats

- **Hyprland**: Native blocks (`section { ... }`), composed from sourced files
- **Waybar**: JSONC (`config.jsonc`) + CSS (`style.css`). Theme = CSS import swap
- **Alacritty**: TOML
- **Kitty/Ghostty**: INI-ish
- **Foot**: INI
- **Lazygit**: YAML
- **OpenCode**: JSON
- **Wiremix/Walker/SwayOSD**: TOML
- **btop**: Self-documented INI
- **Mako**: mako-style INI
- **xournalpp**: XML
- **Typora themes**: CSS

### Terminal-Driven Theme Matching

Source of truth: `~/.config/omarchy/current/theme/kitty.conf`

Map to Waybar: copy Kitty `foreground/background/cursor/color0-15` → Waybar `@define-color base/surface/overlay/text/cursor/love/gold/rose/pine/foam/iris` in `~/.config/waybar/<name>.css`, then `@import` from `style.css`.

---

## 8. Multi-Monitor Wallpaper (swaybg)

### Working Pattern (One command per output)

```bash
killall swaybg 2>/dev/null
swaybg --output DP-1 --image PATH --mode fill
swaybg --output DP-2 --image PATH --mode fill
swaybg --output HDMI-A-1 --image PATH --mode fill
```

### Persistence

Add to `~/.config/hypr/autostart.conf` (one exec-once per monitor):
```bash
exec-once = swaybg --output DP-1 --image /path/img.jpg --mode fill
exec-once = swaybg --output DP-2 --image /path/img.jpg --mode fill
exec-once = swaybg --output HDMI-A-1 --image /path/img.jpg --mode fill
```

### Pitfalls

- `hyprpaper` may need more args; prefer `swaybg` in this setup
- Omarchy autostart ordering: defaults load first, then user `autostart.conf` — user lines can stomp defaults
- Verify: `ps aux | grep swaybg`, then `killall swaybg` and relaunch individually

### swaybg Modes

`stretch`, `fit`, `fill`, `center`, `tile`, `solid_color`

---

## 9. Theming, Hooks, Migrations

### Theme Switching

Omarchy theme = snippet overlays in `~/.config/omarchy/current/theme/*` (sourced/included into user configs).

Current applied theme: `~/.config/omarchy/current/theme/*`

Regenerate via theme switch, not direct edit of `~/.config/omarchy/current/theme/*`.

### App Theme Bundles

For themed apps (e.g., superfile):
- Config: `~/omarchy-rice/superfile/config.toml`
- Themes: `~/omarchy-rice/superfile/theme/*.toml`
- Reproduce: copy to `~/.config/superfile/`
- `theme` value in `config.toml` must match theme file basename

### Migrations

Omarchy migrations: `/usr/share/omarchy/migrations/*.sh` — sourced once.

### Pitfalls

- Don't edit `~/.config/omarchy/current/theme/*` directly for persistent changes
- `hypr.conf` composed from many sourced files; put overrides in `~/.config/hypr/*`
- `pacman -Qsq` / `yay -Qq` are right inventory tools; AppImages/flatpaks not captured
- Chromium config huge; use `~/.config/chromium-flags.conf` for user-facing flags
- Fish not installed; don't write fish onboarding

---

## Reference Files

| File | Source Skill |
|------|--------------|
| `references/arch-troubleshooting-entries.md` | arch-troubleshooting |
| `references/config-map.md` | linux-desktop-config |
| `references/session-2026-06-06-terminal-font-aliases.md` | omarchy-shell-terminal-config |
| `references/omarchy-config-catalog.md` | omarchy-system |
| `references/omarchy-config-cheat-sheet.md` | omarchy-system |

---

## Common Pitfalls

1. **Boot before keys** — Fix pacman keyring BEFORE `pacman -Syu`
2. **Wrong GPU primary** — AMD must be DRM master for Omarchy
3. **Partial update forward repair** — Prefer `pacman -S --overwrite '*'` over downgrade
4. **Theme override vs template** — Don't edit generated theme files directly
5. **Hyprland config composition** — Override in `~/.config/hypr/*`, not shared defaults
6. **swaybg per-output** — One command per output, not combined
7. **Oh My Posh ≠ aliases** — Add eza aliases manually for zsh
8. **Config format mismatch** — Match quoting style when replacing

---

## Verification Checklist

- [ ] Boot: `bootctl status` valid, `mkinitcpio -P` clean
- [ ] Hyprland: `hyprctl devices` shows AMD primary, `journalctl` clean
- [ ] Pacman: `pacman -Sy` no signature errors
- [ ] Desktop: `fc-cache -fv` after font changes, apps restarted
- [ ] Shell: `alias \| grep eza` shows expected aliases
- [ ] Terminal: font size correct, resize keys work
- [ ] Wallpaper: `ps aux \| grep swaybg` shows per-output instances
- [ ] Theme: `~/.config/omarchy/current/theme/kitty.conf` matches Waybar CSS