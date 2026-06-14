name: linux-arch-boot-recovery

# Overview
This skill covers the most common Arch Linux boot failures caused by interrupted or broken `-Syu` upgrades. Typical symptoms include reaching a `switch_root` or `dracut-initqueue` failure prompt, dropping into an `emergency mode` shell, or failing to find the root partition.

Scope is specifically:
  • Interrupted `pacman -Syu` leaving the package database or initramfs inconsistent
  • systemd boot loops or failed boot entries
  • Kernel/bootloader mismatch after updates

Assumptions:
  • EFI system with systemd-boot is the primary context, but GRUB paths are included.
  • The user still has a live USB or TTY access via Ctrl+Alt+F2 from the recovery shell.

# Diagnostics

1. Inspect journal logs on the broken system or from a live environment
   • If emergency shell is reachable:
       journalctl -xb --no-pager -p err..crit
   • If chrooting from live USB, bind-mount and inspect:
       mount /dev/<esp> /mnt/boot
       arch-chroot /mnt
       journalctl --since "10 minutes ago"

2. Check pacman database integrity
   From a chroot or if pacman still responds:
       pacman -Qk 2>&1 | grep -E "missing|error"
       pacman -Dk
       ls -l /var/lib/pacman/local/ | head

   Red flags:
     • Partial /var/lib/pacman/local entries for linux/mkinitcpio/systemd
     • "could not open /var/lib/pacman/local/.../desc"

3. Check initramfs and kernel image status
       ls -l /boot/*.img /boot/vmlinuz-*
       ls -l /boot/loader/entries/*.conf

   Verify that the running entry in `/boot/loader/entries/*.conf` points to existing files.

4. Check for missing or rejected filesystem modules (common after mkinitcpio changes)
       lsmod | grep -E "<your_fs>|<your_raid>|<your_luks>"
       blkid /dev/<root_partition>

   For Btrfs systems, also confirm presence of /usr subvolume if using one.

# Fixes

A. Emergency chroot workflow

  On an Arch live USB:

    # 1. Identify and mount the root partition
    cryptsetup open <dev> <name>        # if LUKS
    mount /dev/<root> /mnt
    mount /dev/<esp> /mnt/boot            # same mountpoint as normal system
    arch-chroot /mnt

  If LVM/LUKS+root-on-LVM:
    vgscan
    lvchange -ay <vg>/<lv>
    mount ...

B. Repair pacman database and regenerate sync databases

    # Mark partially installed base packages if needed
    pacman -Qk >/tmp/pkgcheck.txt 2>&1
    # If incomplete, re-download and reload local DB
    pacman-db-check
    pacman -Syu --needed base linux mkinitcpio systemd

  If mkinitcpio warns about missing modules, regenerate:
    mkinitcpio -P

C. Rebuild initramfs and regenerate boot loader entry

    mkinitcpio -P

  systemd-boot:
    bootctl update

  GRUB:
    grub-mkconfig -o /boot/grub/grub.cfg

D. Handle crypttab or fstab mismatches after UUID changes

    blkid
    nano /etc/fstab
    nano /etc/crypttab
    grep -R "<old_uuid>" /etc /boot

  Regenerate initramfs again after edits:
    mkinitcpio -P

E. Reinstall the kernel and boot chain if still broken

    pacman -S --needed linux linux-headers systemd mkinitcpio
    # For Intel:
    pacman -S --needed intel-ucode
    # For AMD:
    pacman -S --needed amd-ucode

  Then:
    bootctl update  # or grub-mkconfig

F. Rollback with snapshots (highly recommended if Btrfs + snapper)

  From chroot or live environment:

    # List snapshots
    snapper list

  Rollback to pre-update snapshot:
    snapper rollback <number>
    # Then reboot. If the rollback creates a new read-only snapshot,
    # follow the distribution's documented post-rollback mount steps.

# Verification

1. Confirm kernel and initramfs pair match

       ls -lh /boot/vmlinuz-linux /boot/initramfs-linux.img
       ls -lh /boot/amd-ucode.img /boot/intel-ucode.img 2>/dev/null

2. Confirm boot loader sees the entry

   systemd-boot:
       bootctl list

   GRUB:
       grep -E "menuentry |submenu " /boot/grub/grub.cfg | head

3. Confirm systemd can resolve root and emergency targets are gone

   Reboot, then immediately after login:
       systemctl is-system-running
       systemctl list-units --failed

   Expected:
     • `running` is printed
     • 0 failed units in the list

4. Verify no held packages requiring full reinstall
       pacman -Qm | wc -l
       pacman -Qdt
       pacman -Suu 2>/dev/null        # downgrade orphaned packages if needed

# References

• ArchWiki: https://wiki.archlinux.org/title/General_recommendations#Maintenance
• ArchWiki systemd-boot: https://wiki.archlinux.org/title/systemd-boot
• ArchWiki GRUB: https://wiki.archlinux.org/title/GRUB
• ArchWiki Btrfs snapshots: https://wiki.archlinux.org/title/Snapper
• mkinitcpio manual: https://man.archlinux.org/man/mkinitcpio.8
• pacman database repair guidance from ArchWiki: https://wiki.archlinux.org/title/Pacman/Restore_local_database
