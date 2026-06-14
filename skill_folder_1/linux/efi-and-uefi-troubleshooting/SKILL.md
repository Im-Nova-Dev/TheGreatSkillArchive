---
name: efi-and-uefi-troubleshooting
description: Practical EFI/UEFI boot troubleshooting on Arch/Linux: verify UEFI mode, ESP mount/health, efivarfs, efibootmgr, boot order, fallback paths, Secure Boot (sbctl/shim/own keys), and recovery from common breakage.
---

# EFI/UEFI Boot Troubleshooting

Practical EFI/UEFI boot troubleshooting on Arch/Linux: verify UEFI mode, ESP mount/health, efivarfs, efibootmgr, boot order, fallback paths, Secure Boot (sbctl/shim/own keys), and recovery from common breakage.

## Core Concepts

- **UEFI vs BIOS/CSM**: UEFI is the modern firmware interface replacing legacy BIOS. Booting in UEFI mode requires an ESP (EFI System Partition) formatted as FAT32.
- **ESP (EFI System Partition)**: Typically mounted at `/efi` or `/boot/efi`. Must be FAT32. Contains boot loaders (`EFI/BOOT/BOOTX64.EFI`, `EFI/arch/`, etc.) and kernel/initramfs for UKI setups.
- **efivarfs**: Virtual filesystem at `/sys/firmware/efi/efivars` exposing UEFI variables to the OS. Required for `efibootmgr`, `bootctl`, and Secure Boot tools. Mounted automatically when kernel boots in UEFI mode with `CONFIG_EFI=y` and no `noefi` parameter.
- **Boot entries**: Stored in UEFI NVRAM via variables `BootXXXX`. Managed with `efibootmgr` or UEFI Shell `bcfg`.
- **Secure Boot**: Cryptographic chain of trust for boot components. Can use Microsoft-signed shim/PreLoader or user-owned keys (PK/KEK/db/dbx). Arch's installer does not support Secure Boot out of the box.
- **Fallback paths**: UEFI spec defines `EFI/BOOT/BOOTX64.EFI` (x64) as the default fallback bootloader — used when no NVRAM entry exists or for removable media.

```

```bash
# 1. Confirm UEFI boot mode
cat /sys/firmware/efi/fw_platform_size   # 64 = x64 UEFI, 32 = IA32, missing = BIOS/CSM

# 2. Check efivarfs is mounted
mount | grep efivarfs
ls /sys/firmware/efi/efivars/ 2>/dev/null | head -5

# 3. Find ESP and verify mount
findmnt /efi /boot/efi /boot  # shows ESP mount point, device, fstype

# 4. List UEFI boot entries
efibootmgr --unicode

# 5. Secure Boot status
bootctl
# or: od -An -tu1 /sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c | awk '{print $NF}'
```

## efivarfs Issues

### Symptoms
- `efibootmgr` fails: `Could not prepare Boot variable: No such file or directory`
- `efivar --list` returns `Function not implemented`
- `bootctl` shows `EFI variables not supported`

### Fixes (try in order)

**1. Mount efivarfs manually (inside and outside chroot)**
```bash
mount -t efivarfs efivarfs /sys/firmware/efi/efivars
```

**2. Kernel parameter: `efi=runtime`** (for realtime kernels or when efivarfs fails)
Add to kernel command line in bootloader config, then reboot.

**3. Clear stuck variable dump files**
```bash
rm -f /sys/firmware/efi/efivars/dump-*
reboot
```

**4. Kernel parameter: `efi_no_storage_paranoia`** (last resort — disables NVRAM fullness safeguard)
Add to kernel command line, reboot. **Use only when needed, not permanently.**

### Verify fix
```bash
efivar --list | head -5
efibootmgr --unicode
```

## efibootmgr — Manage UEFI Boot Entries

### Prerequisites
```bash
# Find ESP disk and partition number
findmnt /efi /boot/efi
# Example output: /efi /dev/nvme0n1p1 vfat ...
# → Disk: /dev/nvme0n1, Partition: 1
```

### Common Operations

**View current boot order and entries**
```bash
efibootmgr --unicode
```

**Create a new boot entry (systemd-boot example)**
```bash
efibootmgr --create --disk /dev/nvme0n1 --part 1 \
    --loader '\EFI\systemd\systemd-bootx64.efi' \
    --label 'Arch Linux (systemd-boot)' --unicode
```
> Path separators: UEFI uses `\` but `efibootmgr` auto-converts `/` to `\`.

**Set boot order**
```bash
efibootmgr --bootorder 0001,0000,0002 --unicode
# Numbers from efibootmgr output (Boot0001, Boot0000, etc.)
```

**Delete an entry**
```bash
efibootmgr --delete-bootnum --bootnum 0002 --unicode
```

**Boot to firmware setup (UEFI settings menu) on next reboot**
```bash
systemctl reboot --firmware-setup
# or: efibootmgr --bootnext 0000  # if 0000 points to firmware setup
```

### When efibootmgr Fails

| Issue | Workaround |
|-------|------------|
| `Could not prepare Boot variable` | Fix efivarfs first (see above) |
| EDD 3.0 detection bug | Wrapper script: `#!/bin/sh\nexec /usr/bin/efibootmgr -e 3 "$@"` |
| NVRAM full / write protected | Try `efi_no_storage_paranoia` kernel param |
| Virtual machine (no NVRAM) | Use UEFI Shell `bcfg` or fallback path |

### Alternative: UEFI Shell `bcfg`
1. Boot UEFI Shell (from firmware menu or `Shell.efi` on ESP)
2. `bcfg boot dump` — list entries
3. `bcfg boot add 0 FS0:\EFI\arch\vmlinuz-linux.efi "Arch Linux"` — add entry
4. `bcfg boot mv 0 0` — move to first position

## ESP (EFI System Partition) & Fallback Paths

### Verify ESP Health
```bash
# Check mount point, fstype, space
findmnt -T /efi /boot/efi
df -h /efi /boot/efi

# Verify FAT32
blkid /dev/nvme0n1p1 | grep vfat

# List ESP contents
ls -la /efi/EFI/
```

### Common ESP Issues

| Problem | Fix |
|---------|-----|
| ESP not mounted | `mount /dev/nvme0n1p1 /efi` → add to `/etc/fstab` |
| Wrong fstype (not FAT32) | Reformat: `mkfs.fat -F32 /dev/nvme0n1p1` (backup first!) |
| Full / no space | Clean old kernels, expand partition, or move to larger ESP |
| Missing fallback `EFI/BOOT/BOOTX64.EFI` | Copy bootloader: `cp /efi/EFI/systemd/systemd-bootx64.efi /efi/EFI/BOOT/BOOTX64.EFI` |

### Fallback Boot Path (Removable Media / NVRAM Missing)
UEFI spec requires `EFI/BOOT/BOOTX64.EFI` on the ESP for default boot.
```bash
# Install systemd-boot fallback
cp /efi/EFI/systemd/systemd-bootx64.efi /efi/EFI/BOOT/BOOTX64.EFI

# For GRUB
cp /efi/EFI/grub/grubx64.efi /efi/EFI/BOOT/BOOTX64.EFI

# For rEFInd
cp /efi/EFI/refind/refind_x64.efi /efi/EFI/BOOT/BOOTX64.EFI

# UKI (Unified Kernel Image) — place directly
cp /efi/EFI/Linux/arch-linux.efi /efi/EFI/BOOT/BOOTX64.EFI
```

### Repair ESP from Live USB / Chroot
```bash
# Boot Arch ISO (UEFI mode!)
# Find ESP
lsblk -f | grep vfat

# Mount
mkdir /mnt/esp
mount /dev/nvme0n1p1 /mnt/esp

# If chrooting into installed system:
mount /dev/nvme0n1p2 /mnt  # root partition
mount /dev/nvme0n1p1 /mnt/efi
arch-chroot /mnt

# Inside chroot: reinstall bootloader
bootctl install  # systemd-boot
# grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=grub  # GRUB
```

## Secure Boot

### Check Status
```bash
bootctl
# Secure Boot: enabled (user)  ← active enforcement
# Secure Boot: disabled (setup)  ← Setup Mode (no PK enrolled)
# Secure Boot: disabled (disabled)  ← feature off
# Secure Boot: disabled (unsupported)  ← firmware lacks Secure Boot
```

### Approach 1: sbctl (User-Owned Keys — Recommended for Arch)

**Install & setup**
```bash
pacman -S sbctl
sbctl create-keys  # generates PK, KEK, db keys in /etc/secureboot/keys/
sbctl enroll-keys -m  # enroll to firmware (requires UEFI Setup Mode)
```

**Sign boot components**
```bash
# Sign kernel(s)
sbctl sign -s /efi/EFI/Linux/arch-linux.efi  # UKI
sbctl sign -s /efi/EFI/systemd/systemd-bootx64.efi  # systemd-boot

# Auto-sign on kernel updates (pacman hook included with sbctl)
# Verify: sbctl verify
```

**Verify enrollment**
```bash
sbctl verify
efivar -l | grep -iE 'pk|kek|db'
```

### Approach 2: Shim / PreLoader (Microsoft-Signed — Dual Boot Friendly)

**Use case**: Dual-boot with Windows, can't enroll own PK (vendor OpROMs signed with Microsoft CA).

```bash
# Install shim-signed and PreLoader from AUR or use distribution packages
# Copy to ESP:
cp /usr/share/shim-signed/shimx64.efi /efi/EFI/BOOT/BOOTX64.EFI
cp /usr/share/shim-signed/mmx64.efi /efi/EFI/BOOT/mmx64.efi

# Create boot entry pointing to shim
efibootmgr --create --disk /dev/nvme0n1 --part 1 \
    --loader '\EFI\BOOT\BOOTX64.EFI' --label 'Arch (shim)' --unicode

# On first boot: shim launches MOK Manager → enroll MOK (hash of your kernel/initramfs)
# Or: mokutil --import /path/to/key.der
```

### Approach 3: Disable Secure Boot (If All Else Fails)
```bash
# Via firmware setup (F2/Del/Esc on boot) → Security → Secure Boot → Disabled
# Or from Windows:
# Settings → Update & Security → Recovery → Advanced startup → UEFI Firmware Settings
```

### Critical Warning: OpROM Bricking Risk
Before enrolling own PK (Approach 1), **check device OpROM signatures**:
```bash
# List devices with Option ROMs
find /sys/devices -name rom

# For each, dump and check signature
echo 1 > /sys/devices/pci0000:00/.../rom
cat /sys/devices/pci0000:00/.../rom > /tmp/device.rom
# If signed with Microsoft 3rd Party UEFI CA → keep Microsoft certs in db
# Otherwise enrolling own PK may brick GPU/SSD/firmware
```

## Common Pitfalls

| Pitfall | Prevention / Fix |
|---------|------------------|
| Booting Arch ISO in BIOS/CSM mode on UEFI system | Disable CSM in firmware; boot ISO in UEFI mode |
| Forgetting `mkinitcpio -P` after installing microcode (`intel-ucode`/`amd-ucode`) | Always rebuild initramfs: `mkinitcpio -P` |
| `efibootmgr` fails because efivarfs not mounted | Fix efivarfs first (see efivarfs Issues section) |
| Mixing NVIDIA `dkms` with `nvidia-utils` from different versions/repos | Install both from same repo; `pacman -Syu` before DKMS rebuild |
| Installing CPU microcode but not adding to initramfs | `pacman -S intel-ucode` → `mkinitcpio -P` (auto via hook) |
| ESP mounted at `/boot` instead of `/efi` or `/boot/efi` (Secure Boot risk) | Mount ESP at `/efi`; keep `/boot` on root or separate partition |
|Secure Boot: enrolling own PK without checking OpROM signatures | Always run OpROM check before `sbctl enroll-keys` |
| Secure Boot: Arch ISO doesn't boot with Secure Boot enabled | Disable Secure Boot for install, or use Archboot |
| NVRAM full / boot entries not persisting | `efi_no_storage_paranoia` kernel param (last resort) |
| Deleting `linux-firmware` package by accident | `pacman -Ql linux-firmware` shows many device firmware files |
| UKI not signed for Secure Boot | Use `sbctl sign` or `objcopy --sign` with your db key |

## References

- **Arch Wiki — Unified Extensible Firmware Interface**: https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface
- **Arch Wiki — UEFI Secure Boot**: https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface/Secure_Boot
- **Arch Wiki — systemd-boot**: https://wiki.archlinux.org/title/Systemd-boot
- **Arch Wiki — GRUB (UEFI)**: https://wiki.archlinux.org/title/GRUB#UEFI_systems
- **Arch Wiki — efibootmgr**: https://wiki.archlinux.org/title/Efibootmgr
- **Arch Wiki — mkinitcpio**: https://wiki.archlinux.org/title/Mkinitcpio
- **sbctl documentation**: https://github.com/Foxboron/sbctl
- **UEFI Specification**: https://uefi.org/specifications
