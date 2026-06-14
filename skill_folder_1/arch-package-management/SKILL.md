---
name: arch-package-management
description: >
  Practical Arch Linux package management debugging: diagnose pacman failures,
  AUR/helper issues, package database corruption, stale locks, signature/keyring,
  mirror/DNS problems, partial upgrades, and space-related failures with concrete
  terminal commands. Use when pacman, yay, paru, or package workflows misbehave.
---

# Arch Package Management Troubleshooting

Use when `pacman`, AUR helpers, or package-related workflow breaks on Arch/Omarchy.

## 1. Immediate Checks
```bash
# Stale pacman lock
sudo rm -f /var/lib/pacman/db.lck

# Disk space
df -h /
df -h /var/cache/pacman
```

## 2. Database Integrity
```bash
sudo pacman -Dk
sudo pacman -Qk
sudo pacman-db-check
```

## 3. Force Refresh + Resume
```bash
sudo pacman -Syy
sudo pacman -Syu
```

## 4. Signature / Keyring Repair
```bash
sudo pacman -Sy archlinux-keyring
sudo pacman-key --init
sudo pacman-key --populate archlinux
```

## 5. Mirror / DNS
```bash
reflector --country 'United States' --age 12 --protocol https --sort rate \
  --save /etc/pacman.d/mirrorlist
sudo pacman -Syy
cat /etc/resolv.conf
```

## 6. Partial or Interrupted Upgrade
```bash
sudo pacman -Syu
# If dependency errors, rarely:
sudo pacman -Suu
```

## 7. AUR Helpers
```bash
yay -Syua
yay -S --aur --rebuild yay
sudo pacman -S --needed base-devel git
```

## 8. Broken / Held Packages
```bash
pacman -Qm
paccache -r
sudo pacman -S --overwrite '*' <pkg>
```

## 9. Diagnostic Snapshot
```bash
uname -a
pacman -Q pacman
pacman -Dk
```
