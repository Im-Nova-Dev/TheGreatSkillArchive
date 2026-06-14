---
name: linux-logs-and-journald
description: "Practical systemd journal (journald) troubleshooting on Arch/Omarchy: query, filter, export, correlate, and persist logs for boot failures, service crashes, and mysterious issues. Covers journalctl patterns, persistent storage, log rotation, and integration with coredumpctl."
tags: [linux, arch, systemd, journald, logging, troubleshooting, journalctl]
related_skills: [systemd-administration, arch-troubleshooting, linux-audio-and-pipewire]
---

# Linux Logs And Journald

Practical systemd journal troubleshooting on Arch/Omarchy. Use when a service fails, boots hang, you need to trace crashes across reboots, or journalctl output is overwhelming.

## Quick reference

```bash
# Current boot, errors only
journalctl -xb -p err

# Last 30 minutes, all units
journalctl --since "30 minutes ago"

# Follow live
journalctl -f

# Specific unit, current boot
journalctl -xb -u hyprland
journalctl -xb -u NetworkManager

# User session units
journalctl --user -u hyprland -u waybar -u wireplumber

# Export for bug reports
journalctl -xb -u hyprland > /tmp/hyprland-boot.log
```

## Boot and startup diagnostics

```bash
# Current boot, all messages
journalctl -xb

# Previous boot (requires persistent storage)
journalctl -xb -1

# List available boots
journalctl --list-boots

# Kernel messages only, current boot
journalctl -xb -k

# Show boot duration breakdown
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
```

## Service failure triage

```bash
# Failed units
systemctl --failed
systemctl --user --failed

# Full failure context (expands unit, shows exec, PID, exit code)
journalctl -xeu <unit>

# Last 80 lines of a failing service
journalctl -xeu <unit> -n 80

# Search for specific failure patterns
journalctl -xb | rg -i "failed|error|timeout|segfault|kill|oom"
```

## User session (Hyprland, Wayland, PipeWire)

```bash
# User journal for graphical session
journalctl --user -u hyprland -u waybar -u wireplumber -u pipewire -u xdg-desktop-portal

# Since session start
journalctl --user -u hyprland --since "1 hour ago"

# Combine with grep for config errors
journalctl --user -u hyprland --since "30 minutes ago" | rg -i "config|syntax|windowrule|layerrule|does not exist|invalid"
```

## Persistence and retention

By default Arch uses volatile storage (logs lost on reboot). Enable persistent:

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
```

Verify:

```bash
journalctl --list-boots  # should show multiple boots
journalctl -xb -1        # previous boot should work
```

Configure retention in `/etc/systemd/journald.conf`:

```ini
[Journal]
Storage=persistent
SystemMaxUse=500M
SystemMaxFileSize=50M
RuntimeMaxUse=100M
MaxRetentionSec=2week
Compress=yes
ForwardToSyslog=no
```

Apply:

```bash
sudo systemctl restart systemd-journald
journalctl --disk-usage
```

## Correlating with coredumpctl

When a service crashes:

```bash
coredumpctl list
coredumpctl info <pid>
coredumpctl debug <pid>   # launches gdb
coredumpctl dump <pid> > /tmp/core.dump
```

Cross-reference with journal:

```bash
# Find the crash in journal
journalctl -xb | rg -i "coredump|segfault|killed|signal"
```

## Advanced filtering

```bash
# By priority (0=emerg .. 7=debug)
journalctl -p 3           # errors and above
journalctl -p 0..3        # emerg..err

# By time range
journalctl --since "2024-01-15 10:00" --until "2024-01-15 11:00"
journalctl --since "1 hour ago" --until "30 minutes ago"
journalctl --since yesterday

# By executable
journalctl /usr/bin/hyprland
journalctl /usr/lib/systemd/systemd

# By unit with time
journalctl -u NetworkManager --since "1 hour ago"

# JSON output for parsing
journalctl -o json -u hyprland | jq 'select(.MESSAGE | contains("error"))'

# Reverse (newest first)
journalctl -r
```

## Common Arch/Omarchy scenarios

### Hyprland won't start
```bash
journalctl --user -u hyprland -xb
# Look for: "Failed to create backend", "Invalid parameters", "does not exist", "EGL", "KMS"
```

### NetworkManager/Wi-Fi issues
```bash
journalctl -xb -u NetworkManager
journalctl -xb -u systemd-resolved
```

### Audio/PipeWire silent
```bash
journalctl --user -xb -u pipewire -u wireplumber -u pipewire-pulse
```

### Boot hangs / slow boot
```bash
systemd-analyze blame
systemd-analyze critical-chain
journalctl -xb | rg -i "timeout|start.*[0-9]+s|waiting"
```

### Suspend/resume failures
```bash
journalctl -xb -1 | rg -i "suspend|resume|sleep|hibernate|PM:"
journalctl -xb -1 -u systemd-suspend
```

## Exporting for bug reports

```bash
# Full current boot
journalctl -xb > /tmp/full-boot.log

# Specific unit + context
journalctl -xb -u hyprland --no-pager > /tmp/hyprland.log

# Compress
tar czf /tmp/journal-report.tgz -C /tmp *.log
```

## Log rotation manual trigger

```bash
sudo journalctl --vacuum-time=1d
sudo journalctl --vacuum-size=100M
sudo journalctl --vacuum-files=10
```

## Common pitfalls

- Assuming logs persist across reboots without enabling persistent storage
- Using `grep` on raw journal files instead of `journalctl` filters
- Forgetting `--user` for user-session services (Hyprland, PipeWire, Waybar)
- Not checking previous boot (`-1`) when debugging post-reboot issues
- Overlooking `coredumpctl` for service crashes that leave no journal trace
- Filtering by `-p err` too early; warnings (`-p 4`) often contain the root cause
- Editing `/etc/systemd/journald.conf` without restarting `systemd-journald`

## Verification checklist

- [ ] `journalctl --list-boots` shows multiple entries (persistence works)
- [ ] `journalctl -xb -1` shows previous boot logs
- [ ] `journalctl --disk-usage` reports reasonable size (< 1GB typical)
- [ ] `coredumpctl list` shows recent crashes if any
- [ ] `journalctl -xb -u <failing-unit>` shows actionable error lines
- [ ] User session logs accessible: `journalctl --user -u hyprland` works

## References

- `man journalctl`, `man journald.conf`, `man coredumpctl`
- Arch Wiki: systemd/Journal, systemd/Coredump
- Related skills: `systemd-administration`, `arch-troubleshooting`, `omarchy-hyprland-post-update-fix`, `hyprland-logging-and-evidence`
