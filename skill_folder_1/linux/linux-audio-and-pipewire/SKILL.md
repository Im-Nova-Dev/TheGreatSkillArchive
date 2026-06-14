# PipeWire/WirePlumber Audio Troubleshooting on Arch

Practical debugging and repair for PipeWire, WirePlumber, and PipeWire-Pulse on Arch/Hyprland. Covers no-audio, crackling, device switching, Bluetooth, and microphone issues.

## Core Concepts

**PipeWire** is the multimedia server replacing PulseAudio/JACK. **WirePlumber** is the session/policy manager. **pipewire-pulse** provides PulseAudio compatibility. On Arch, these run as user services via systemd --user.

Key files:
- `/usr/share/pipewire/` - system defaults (don't edit)
- `~/.config/pipewire/` - user overrides (edit here)
- `/usr/share/wireplumber/` - system WirePlumber configs
- `~/.config/wireplumber/` - user WirePlumber overrides

## Quick Diagnostics

```bash
# 1. Check if services are running
systemctl --user status pipewire wireplumber pipewire-pulse

# 2. List audio devices and their state
pw-cli list-objects | grep -E "(device|node|port)"
wpctl status

# 3. Check default sink/source
wpctl get-default-sink
wpctl get-default-source

# 4. Inspect PipeWire logs
journalctl --user -u pipewire -u wireplumber -u pipewire-pulse -f
```

## Common Issues & Fixes

### No Audio Output

```bash
# Check if sink exists and is not suspended
wpctl status | grep -A 20 "Sinks:"

# Force resume suspended sink
wpctl set-mute @DEFAULT_AUDIO_SINK@ 0
wpctl set-volume @DEFAULT_AUDIO_SINK@ 50%

# If no sink: check alsa devices
wpctl inspect @DEFAULT_AUDIO_SINK@
# Or list all: pw-cli list-objects | grep -A 5 "alsa"
```

**Root cause**: Often the ALSA device isn't claimed. Fix by creating a WirePlumber rule:

```lua
# ~/.config/wireplumber/main.lua.d/99-force-alsa.lua
rule = {
  matches = {
    { "device.name", "matches", "alsa_card.*" }
  },
  apply_properties = {
    ["api.alsa.use-ucm"] = true,
  }
}
table.insert(alsa_monitor.rules, rule)
```

Then restart: `systemctl --user restart wireplumber`

### Crackling / Static / Buffer Underruns

```bash
# Check quantum/buffer settings
pw-cli info 0 | grep -E "quantum|rate|clock"

# Increase quantum (default 1024)
# Edit ~/.config/pipewire/pipewire.conf.d/99-quantum.conf
context.properties = {
  default.clock.quantum = 2048
  default.clock.min-quantum = 256
  default.clock.max-quantum = 8192
}
```

Restart: `systemctl --user restart pipewire`

### Bluetooth Headset Issues

```bash
# 1. Verify bluez + pipewire-pulse + libspa-bluetooth installed
pacman -Qs bluez libspa-bluetooth pipewire-pulse

# 2. Check bluetooth service
systemctl status bluetooth

# 3. Pair/connect via bluetoothctl, then:
wpctl status  # Should show bluez_output.* sink

# 4. If no HSP/HFP (mic): ensure ofono or pipewire 1.0+ with native HSP
# Check: pw-cli info <bluez_node_id> | grep -i hfp
```

**Profile switching** (A2DP vs HSP):
```bash
# List profiles
pactl list cards | grep -A 20 "bluez_card"

# Set profile
pactl set-card-profile bluez_card.XX_XX_XX_XX_XX_XX a2dp-sink
# or for mic:
pactl set-card-profile bluez_card.XX_XX_XX_XX_XX_XX headset-head-unit
```

### Microphone Not Working

```bash
# Check default source
wpctl get-default-source
wpctl status  # Look at Sources section

# Check if input is muted
wpctl set-mute @DEFAULT_AUDIO_SOURCE@ 0

# Verify permissions (pipewire-media-session uses portal)
# On Hyprland/Wayland: ensure xdg-desktop-portal and xdg-desktop-portal-hyprland running
systemctl --user status xdg-desktop-portal*
```

### Device Not Switching Automatically

Create WirePlumber policy for priority-based switching:

```lua
# ~/.config/wireplumber/main.lua.d/99-device-priority.lua
alsa_monitor.rules = {
  {
    matches = {
      { "device.name", "matches", "alsa_card.usb-*" },
    },
    apply_properties = {
      ["priority.session"] = 2000,
      ["priority.driver"] = 1000,
    }
  },
  {
    matches = {
      { "device.name", "matches", "alsa_card.pci-*" },
    },
    apply_properties = {
      ["priority.session"] = 1000,
      ["priority.driver"] = 500,
    }
  },
}
```

### Hyprland-Specific: No Audio After Wake/Suspend

```bash
# Add to hyprland.conf exec-once:
exec-once = systemctl --user restart pipewire wireplumber pipewire-pulse

# Or create a systemd user service for resume:
# ~/.config/systemd/user/pipewire-resume.service
[Unit]
Description=Restart PipeWire after suspend
After=suspend.target hibernate.target hybrid-sleep.target

[Service]
Type=oneshot
ExecStart=systemctl --user restart pipewire wireplumber pipewire-pulse

[Install]
WantedBy=suspend.target hibernate.target hybrid-sleep.target

# Enable:
systemctl --user enable --now pipewire-resume.service
```

## Verification Commands

```bash
# Full health check
wpctl status && echo "---" && pactl info && echo "---" && pw-cli info 0

# Test playback
speaker-test -c 2 -t wav  # or: pw-play /usr/share/sounds/freedesktop/stereo/complete.oga

# Test recording
pw-record --target=@DEFAULT_AUDIO_SOURCE@ /tmp/test.wav --duration=3
pw-play /tmp/test.wav
```

## Common Pitfalls

- **Editing system files in `/usr/share/`** — always use `~/.config/` overrides
- **Forgetting to restart user services** after config changes: `systemctl --user restart pipewire wireplumber pipewire-pulse`
- **Missing `libspa-bluetooth`** for Bluetooth audio
- **Conflicting PulseAudio instances** — ensure `pulseaudio` package is NOT installed (pipewire-pulse replaces it)
- **Wayland portal permissions** — microphone needs `xdg-desktop-portal` + backend (hyprland/gtk/kde)
- **Sample rate mismatch** — check `default.clock.rate` in pipewire.conf matches hardware (usually 48000)

## References

- Arch Wiki: PipeWire, WirePlumber, Bluetooth headset
- `man pipewire.conf`, `man wireplumber.conf`, `man wpctl`
- `/usr/share/pipewire/` and `/usr/share/wireplumber/` for default config examples