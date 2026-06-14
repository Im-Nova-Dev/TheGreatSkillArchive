---
name: arch-pacman-keyring-repair
description: Fix pacman keyring issues: invalid/corrupted/missing PGP signatures, GPGME errors, unknown trust, and ARM/Pi fresh install failures. Covers quick fix, emergency repair via live ISO/pacstrap, and keyring reinitialization.
category: linux-arch-boot-recovery
---

# Arch Linux Pacman Keyring Repair

**Problem:** `pacman` fails with `GPGME error: No public key` or `invalid or corrupted package (PGP signature)` errors, preventing package installation and system updates. The system keyring is often out of sync with the master keyserver or got corrupted.

**Core principle:** Update the keyring package directly to restore trust, then verify. If pacman itself is broken, use a live ISO or `pacstrap` to bypass it.

## Troubleshooting Procedure

### 1. Diagnosis
Confirm the issue is keyring-related:
```sh
pacman -Syu --info archlinux-keyring
```
Look for errors like:
- `GPGME error: No public key`
- `error: archlinux-keyring: signature from ... is unknown trust`
- `invalid or corrupted package (PGP signature)`

### 2. Quick Fix (if pacman still partially works)
Attempt to force-update just the keyring package:
```sh
sudo pacman -Sy archlinux-keyring --noconfirm
```
If this succeeds, immediately follow with a full sync:
```sh
sudo pacman -Syu --noconfirm
```

### 3. Emergency Repair (pacman is completely blocked)
If step 2 fails, use a live Arch ISO or a recovery shell. Boot from the ISO, mount your root partition to `/mnt`, then:

```sh
# Option A: Update only the keyring via pacstrap
sudo pacstrap -K /mnt archlinux-keyring

# Option B: Reinitialize the keyring from scratch
sudo arch-chroot /mnt pacman-key --init
sudo arch-chroot /mnt pacman-key --populate archlinux
```

**Note for Raspberry Pi/ARM users:** The `-K` flag in `pacstrap` is crucial; it skips existing keyring checks and installs a fresh one.

### 4. Finalize
After any repair, always refresh keys and verify the system:
```sh
sudo pacman-key --refresh-keys
sudo pacman -Syu
```

## Common Pitfalls

- **Partial upgrades are dangerous:** Do not run `pacman -Sy` on its own. Always pair it with `-u` (`-Syu`) after an interrupted sync.
- **Mirror sync delays:** If a mirror is out of date, switch to a different one in `/etc/pacman.d/mirrorlist` before retrying.
- **ARM-specific issues:** For ARM boards, use `arm.pipeurl` or community mirrors if the official pipe is slow.

## Verification
Run `pacman -Qi archlinux-keyring` and ensure the installation date is recent. Run `sudo pacman -Syu` again — it should complete without PGP errors.
