---
name: linux-arch-omarchy-boot-recovery
description: Diagnose and fix broken boot by inspecting BIOS/UEFI entry, ESP mount, and selected Arch/Omarchy bootloader. Use this when the system drops to emergency shell, loader entry not found, or EFISTUB fails.
tags:
  - linux
  - arch
  - omarchy
  - boot
  - systemd-boot
  - grub
  - efistub
  - recovery
---

# Linux Arch/Omarchy Boot Recovery

## Overview
This skill targets broken boot on Arch Linux and Omarchy caused by:
- Expired or corrupted UEFI boot entries
- Missing `/boot` or EFI Partition (ESP) contents
- systemd-boot loader entries pointing to wrong kernel/initramfs
- GRUB after kernel/initramfs rebuild
- EFISTUB entry pointing to a removed or renamed kernel

Goal: recover boot from live media without reinstalling.

## Quick Diagnosis
```bash
# From live USB
lsblk -f
cat /etc/fstab
```

## Step 1 — Find and Mount Root and ESP
```bash
# Identify the root partition and the ESP (small EFI partition, usually vfat)
lsblk
blkid

# Example: root is /dev/nvme0n1p3, ESP is /dev/nvme0n1p1
mount /dev/nvme0n1p3 /mnt
mkdir -p /mnt/boot
mount /dev/nvme0n1p1 /mnt/boot
```

## Step 2 — Chroot
```bash
mount -t proc proc /mnt/proc
mount -t sysfs sys /mnt/sys
mount -t devtmpfs dev /mnt/dev
mount -t devpts devpts /mnt/dev/pts
cp /etc/resolv.conf /mnt/etc/
chroot /mnt /usr/bin/env bash
```

## Step 3 — Repair Bootloader

### A. systemd-boot (Omarchy/Arch default)
```bash
# Reinstall boot loader to current ESP
bootctl install

# Check loader entries
ls /boot/loader/entries/

# Check current entries
bootctl list
```

Fix missing or stale loader entries:
```bash
# Regenerate entries for installed kernels
KVER=$(pacman -Q linux | awk '{print $2}')
mkdir -p /boot/loader/entries
cat > /boot/loader/entries/arch.conf <<EOF
title   Arch Linux
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options root=UUID=$(findmnt -n -o UUID /) rw
EOF

# Update boot order
bootctl set-default arch.conf
```

### B. GRUB
```bash
grub-mkconfig -o /boot/grub/grub.cfg
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```

### C. EFISTUB
```bootctl
# Show current order
efibootmgr -v

# Recreate entry
KVER=$(ls /lib/modules/)
efibootmgr -c -d /dev/nvme0n1 -p 1 \
  -L "Arch Linux" \
  -l '\vmlinuz-linux' \
  -u 'root=UUID=$(findmnt -n -o UUID /) rw initrd=\initramfs-linux.img'
```

## Step 4 — Update Microcode
```bash
pacman -S --noconfirm intel-ucode || pacman -S --noconfirm amd-ucode
# Rebuild initramfs after microcode change
mkinitcpio -P
```

## Step 5 — Unmount and Reboot
```bash
exit
umount -R /mnt
reboot
```

## Common Pitfalls
- If `/boot` is missing, recreate ESP mount at `/boot` before running `bootctl`.
- If kernel renamed by package upgrade, regenerate `/boot/loader/entries/*.conf`.
- For Omarchy, UEFI boot entry sometimes points to `Limine` instead of the OS. Change boot order in firmware settings or with `efibootmgr`.

## Verification
From the fixed system:
```bash
# Confirm loader entries and current default
bootctl list
journalctl -b -p err -n 50
# Confirm kernel booted matches installed
uname -r
pacman -Q linux | awk '{print $2}'
```

## References
- https://wiki.archlinux.org/title/Systemd-boot
- https://wiki.archlinux.org/title/GRUB
- https://wiki.archlinux.org/title/EFISTUB
