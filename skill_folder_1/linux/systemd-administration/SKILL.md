---
name: systemd-administration
description: >
  Troubleshoot systemd units and follow-on failures fast on Arch.
  Use when a service fails, will not start, masks misbehave, or
  journalctl output is overwhelming. Focused, scannable steps.
platform: Linux (Arch-based, systemd)
related_skills:
  - arch-troubleshooting
  - linux-logs-and-journald
---

# Systemd Administration

Practical systemd troubleshooting for broken services, dependency loops,
masked units, timer issues, and journal archaeology.

## Quick failure triage

```bash
systemctl status <unit>
systemctl list-units --state=failed
journalctl -xeu <unit> -n 80
```

When the exact unit is unknown, search recent failure fingerprints:

```bash
journalctl -xb -p err -n 120 | rg -n "dependency|failed|timeout|masked|start"
```

Use `-x` to expand failed-unit logs, `-b` to scope to the current boot,
and `-p err` to cut noise from the unrelated info/debug flood.

## Dependency / ordering loops

If `systemctl start <unit>` reports a dependency loop:

```bash
systemctl show -p Requires,Wants,After,Before,Conflicts <unit>
systemd-analyze critical-chain <unit>
```

Break the loop by loosening ordering or moving a one-shot require
to an `ExecCondition` or `ExecStartPre` where failure is safe.

## Masked units

A masked unit will not start and prints a confusing "unit is masked" error.

```bash
systemctl is-enabled <unit>
```

If `masked`, unmask, then reenable or start:

```bash
sudo systemctl unmask <unit>
sudo systemctl reenable <unit> || sudo systemctl enable --now <unit>
```

Do not mask units to “stop” them permanently; use `disable` or a drop-in
override with `ExecStart=` set to `/usr/bin/true`.

## Bad ExecStart / timeout / crashloop

If a unit exits immediately after start:

```bash
journalctl -xeu <unit> -n 40
sudo systemctl show <unit> -p Result,NRestarts,ExecMainStatus,SubState
```

Common fixes:
- `Restart=` too aggressive: add `StartLimitIntervalSec=` and
  `StartLimitBurst=` in a drop-in.
- `TimeoutStartSec=` too small for first-run work: raise it in
  `/etc/systemd/system/<unit>.service.d/override.conf`.
- Missing runtime dirs: add `RuntimeDirectory=` or a `tmpfiles.d` entry.

```bash
sudo systemctl edit <unit>
```

```ini
[Service]
Restart=on-failure
StartLimitIntervalSec=60s
StartLimitBurst=5
TimeoutStartSec=120s
```

## Socket-activated or user-units failing after boot

Check activation order and user manager state:

```bash
systemctl list-units --type=socket --state=inactive
systemctl --user status <user-unit>
loginctl show-user "$USER" -p Display,State,DefaultTarget
```

For user units that must follow graphical login, set `After=graphical-session.target`
or wrap in a small systemd user service with `WantedBy=default.target`.

## Boot target repair

If `systemctl get-default` points to a non-graphical target after breakage:

```bash
sudo systemctl get-default
sudo systemctl set-default graphical.target
```

If `graphical.target` is fine but display manager still fails, verify it
is wanted by the target:

```bash
systemctl list-dependencies graphical.target | rg -n "gdm|sddm|hyprland|wayland"
```

## Practical Arch fallback notes

- Use `arch-chroot` from live media only after confirming root
  mount, pacman keyring, and `mkinitcpio -P` on the chroot.
- `pacman -Syu` before debugging masked units if package database
  is stale; partial updates can leave units broken.
- For Omarchy/Hyprland post-update breakage, see `omarchy-hyprland-post-update-fix`.

## Verification

- `systemctl status <unit>` shows active or inactive-dead, not failed/masked.
- `journalctl -xeu <unit> -n 40` shows no repeating fatal error for 2+ minutes.
- `systemctl is-enabled <unit>` returns the expected state.
- Boot reaches expected target: `systemctl get-default` matches `graphical.target`.

## References

- `man systemd.unit`, `man systemd.service`, `man systemctl`
- Arch Wiki: systemd, systemd/User services
- Related skills: `arch-troubleshooting`, `omarchy-hyprland-post-update-fix`
