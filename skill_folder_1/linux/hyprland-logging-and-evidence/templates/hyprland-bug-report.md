## Environment
- Distro: Arch / Omarchy (version: `omarchy --version`)
- Hyprland: `hyprctl version`
- Kernel: `uname -r`
- GPU: `glxinfo | grep -i renderer` / `vulkaninfo | grep -i deviceName`
- Compositor backend: Wayland (Hyprland)

## Steps to Reproduce
1.
2.
3.

## Expected vs Actual
- Expected:
- Actual:

## Evidence
- Attached: `hyprland-evidence-<timestamp>.tgz` (contains journal, runtime state, configs, versions, GPU info)
- Key log lines (paste from journal.txt):
```
<grep -i "error|fail|invalid|does not exist" journal.txt | head -20>
```

## Config Notes
- Active theme: `readlink -f ~/.config/omarchy/active`
- Custom configs in ~/.config/hypr/:
```
<list any non-stock files>
```

## Workarounds Tried
- [ ] `hyprctl reload`
- [ ] Reboot
- [ ] `omarchy-update`
- [ ] Rule migration (`windowrule` → `windowrulev2`, `layerrule` → `layerrulev2`)
- [ ] Theme switch via `omarchy-menu`

## Checklist
- [ ] Evidence tarball attached
- [ ] Steps to reproduce are minimal
- [ ] Config snapshot included (config-snapshot.txt)
- [ ] Version coherence checked (versions.txt)