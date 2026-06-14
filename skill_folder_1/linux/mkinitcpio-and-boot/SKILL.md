# Mkinitcpio And Boot
Practical Arch mkinitcpio, initramfs, and boot recovery guidance for UEFI/systemd-boot and BIOS/GRUB setups.

## Core Concepts
- `mkinitcpio` builds the early-userspace initramfs from `/etc/mkinitcpio.conf` and presets in `/etc/mkinitcpio.d/`.
- The boot flow relevant to initramfs is: firmware -> bootloader -> kernel -> initramfs -> real root -> systemd.
- On Arch, initramfs generation is usually driven by presets, not by calling `mkinitcpio` directly.
- Unified kernel images (UKI) bundle the kernel, initramfs, and cmdline; they simplify UEFI Secure Boot and bootloader config.
- Regenerating initramfs is the right first step after changing storage layout, kernel modules, encryption, hooks, or key packages.

## Supported Scenarios
- Regenerate initramfs after mkinitcpio.conf or hook changes.
- Recover from broken boot caused by missing/mismatched initramfs.
- Add or fix hooks for `btrfs`, `lvm2`, `mdadm_udev`, `encrypt`, `sd-encrypt`, `zfs`, and `plymouth`.
- Diagnose why a kernel update or boot entry is not starting.
- Inspect preset config and autodetected modules.

## Procedure
1. Identify config
   ```bash
   cat /etc/mkinitcpio.conf
   ls -l /etc/mkinitcpio.d/
   ```
   Review `HOOKS`, `MODULES`, and preset-defined output paths.

2. Review preset
   ```bash
   cat /etc/mkinitcpio.d/linux.preset
   ```
   Presets call `mkinitcpio` with the actual image/uki paths.

3. Regenerate for all kernels
   ```bash
   mkinitcpio -P
   ```
   Use after changing hooks/modules or when in doubt.

4. Regenerate for one kernel only
   ```bash
   mkinitcpio -p linux
   ```
   Replace `linux` with the preset name.

5. Inspect what mkinitcpio will load
   ```bash
   mkinitcpio -M
   ```
   This prints autodetected modules and helps spot missing storage modules.

6. Inspect hooks
   ```bash
   mkinitcpio -L
   ```

7. For encrypted root with kernel keydisc
   - Prefer `sd-encrypt` on systems using systemd.
   - Add `rootflags=subvolid=...` or `rootfstype=btrfs` if needed.
   - Ensure `cryptdevice` / `rd.luks.name` matches `/etc/crypttab` entries.

8. Rebuild boot entries after regeneration
   ```bash
   bootctl update
   # or
   grub-mkconfig -o /boot/grub/grub.cfg
   ```

9. Verify outputs exist
   ```bash
   ls -l /boot/initramfs-*.img /boot/vmlinuz-*
   ```

## Common Pitfalls
- Forgetting to run `mkinitcpio -P` after editing `mkinitcpio.conf`; presets do not auto-run on config edits.
- Missing storage or filesystem hooks: if root is on USB, add `block` and `usb-storage` contributors; if using bcachefs/ZFS/btrfs, include the matching hook.
- Mismatched kernel and initramfs filenames after manual moves or partial upgrades.
- Generating initramfs without `--kernelimage` / correct `_kimage` when creating a UKI.
- Editing hooks order without understanding dependencies; install hooks are often required before filesystem-specific hooks.
- Stale fallback initramfs after manual regeneration without a reboot.

## Recovery
- Boot an Arch install/live ISO, mount the root and boot partitions, `arch-chroot`, then rebuild initramfs and bootloader entries.
- For `systemd-boot`, confirm `/boot` is mounted and contains the loader entries.
- If using Secure Boot with UKI, ensure the image is signed or enrolled; unsigned images will not boot.
- If the firmware drops to UEFI shell, check that `\\EFI\\systemd\\systemd-bootx64.efi` or the UKI loader path exists.

## Interrupted Update / Partial Upgrade Triage
Use when the system was interrupted during `pacman -Syu` and now fails to boot, drops to `initramfs` emergency shell, or reports missing modules/vmlinuz mismatches.
These symptoms often come from a partial upgrade breaking kernel/module/initramfs compatibility.

1. Recover into the installed system first
   - From live ISO: mount root and boot, `arch-chroot /mnt`, then `arch-chroot -F /mnt` if needed.
   - Confirm `/boot` is mounted and readable.

2. Match kernel / modules / initramfs
   - List packages with mismatches:
     ```bash
     pacman -Qk | grep -E 'linux|linux-lts|linux-zen'
     grep MISSING /var/log/pacman.log | tail -n 200
     ```
   - If the running chroot has multiple kernels, ensure the current and fallback entries all exist:
     ```bash
     ls -l /boot/vmlinuz-* /boot/initramfs-*.img
     ```

3. Force-complete or roll back the partial upgrade
   - Option A: finish the interrupted upgrade:
     ```bash
     pacman -S --needed --overwrite='*'
     ```
     If dependency resolution fails, use:
     ```bash
     pacman -Syu --overwrite='*'
     ```
   - Option B: downgrade to the last working kernel set (requires `downgrade` from AUR):
     ```bash
     downgrade linux linux-headers
     ```
     Or switch to an alternate kernel temporarily:
     ```bash
     pacman -S --needed linux-lts linux-lts-headers
     ```

4. Regenerate initramfs and boot entries
   - ```bash
     mkinitcpio -P
     bootctl update
     ```

5. Verify kernel package consistency
   - ```bash
     pacman -Q linux linux-headers mkinitcpio
     ```
   - Reboot and select the kernel version in the bootloader if using `systemd-boot` multiple entries.

## Pitfall Summary
- Interrupted `Syu` is more dangerous than a normal misconfig because module/kernel headers may no longer match; treat it as a partial-upgrade emergency, not just an initramfs regen.
- Running `mkinitcpio -P` alone does not fix mismatched kernel packages; align package versions first.
- If the installer ISO kernel differs from installed modules, use an LTS fallback or chroot package downgrade rather than booting the live kernel against the installed root.

## Verification
After regeneration, confirm:
- Boot entry is present:
  ```bash
  bootctl list
  ```
- Initramfs and kernel files match the selected entry.
- If available, test with `kexec -l /boot/vmlinuz-... --initrd=/boot/initramfs-... --command-line="..."` only in a safe environment.

## References
- https://wiki.archlinux.org/title/Installation_guide#Initramfs
- https://wiki.archlinux.org/title/Mkinitcpio
- https://wiki.archlinux.org/title/Systemd-boot
- https://wiki.archlinux.org/title/Unified_kernel_image
- https://wiki.archlinux.org/title/Arch_boot_process
