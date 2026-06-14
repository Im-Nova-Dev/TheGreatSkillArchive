{
  "name": "hardware-and-driver-troubleshooting",
  "description": "Teach Linux hardware troubleshooting on Arch: lspci/lsmod, firmware packages, GPU drivers (NVIDIA/AMD/Intel), input, and USB."
}

# Hardware And Driver Troubleshooting

Practical hardware and driver troubleshooting on Arch Linux: detection, firmware, GPU/input/USB diagnostics, and recovery.

## Core Concepts
- `lspci` / `lsusb` identify hardware; `dmesg | tail` shows kernel-side detection and firmware load status.
- Arch splits firmware into `linux-firmware`, `linux-firmware-git`, `intel-ucode`, `amd-ucode`, and vendor repos like `nvidia-dkms`.
- Open drivers are in `mesa`/`xf86-video-*`; proprietary drivers use `nvidia-dkms`, `nvidia-340xx-dkms`, `nvidia-470xx-dkms`, or `amdgpu-pro` (AUR/custom).
- DKMS rebuilds modules automatically on kernel updates if `dkms` is installed.

## Procedure
1. Identify what the hardware is supposed to be and what the kernel sees.
2. Fix firmware or driver state.
3. Verify with the same diagnostic command you started with.

## Practical Workflow

### 1. Take a snapshot before changing anything
```bash
sudo dmesg | tail -200 | grep -iE 'firmware|error|fail|unknown|ucode' || true
sudo lspci -knn  # shows kernel driver in use
sudo lsusb
```

### 2. GPU not working or falling back to llvmpipe
```bash
# Check Mesa and loaded driver
pacman -Qs '^mesa$|^xf86-video-|^nvidia'
glxinfo | grep "OpenGL renderer"
```
**NVIDIA**
- Proprietary: install `nvidia-dkms` + `nvidia-utils` + `lib32-nvidia-utils`, then `mkinitcpio -P` and reboot.
- Open (Nouveau): `xf86-video-nouveau` from extra.
- If nouveau keeps a laptop hybrid setup from switching, install ` envycontrol ` (AUR) or enable PRIME offloading in `nvidia` driver settings.
**AMD**
- Modern: `mesa` is sufficient; `radeon` or `amdgpu` is built-in.
- Old GCN1/2: may need `mesa-amber` (AUR) or adjust kernel parameters.
**Intel**
- `mesa` + `intel-ucode` + `xf86-video-intel` (optional; modesetting is default).
- Tiger Lake+ uses `xe` kernel driver (`modprobe xe`).

### 3. Firmware not loaded / device missing
```bash
# Check missing firmware in journal
dmesg | grep -i 'firmware'
journalctl -b | grep -i 'firmware'
```
- Install `linux-firmware` and CPU-specific microcode (`intel-ucode` / `amd-ucode`).
- Rebuild initramfs after adding/updating ucode: `sudo mkinitcpio -P`.
- If firmware was manually placed in `/lib/firmware/`, confirm permissions and ownership.

### 4. USB / input / webcam not detected
```bash
# List devices
lsusb
# Kernel messages for USB
dmesg | grep -i usb
# Input devices visible
cat /proc/bus/input/devices
```
- USB resets / errors often mean power/cable issues or `usbcore.autosuspend=-1` kernel param.
- A device recognized as `hid-generic` but not working may need vendor-specific quirks or a newer `linux-firmware`.
- Unclaimed devices: check `lspci -k` for PCI USB controllers, ensure `xhci_hcd` or `ehci_pci` is loaded.

### 5. Keyboard / mouse / trackpad not working in Hyprland
```bash
# Verify libinput sees the device
sudo libinput list-devices
```
- If nothing appears, the kernel may not see it; check `dmesg` for i2c-hid or hid-multitouch.
- For laptops with I2C touchpads on 6.x kernels, ensure `hid-multitouch` and `i2c-hid` are not blacklisted.
- Test with `evtest` to rule out userspace.

### 6. Driver fails after kernel update (DKMS / external module)
```bash
sudo pacman -Qk $(pacman -Qm | awk '{print $1}') 2>/dev/null | grep -i dkms
dkms status
```
- If the module is not built for the current kernel, reinstall the package to trigger DKMS.
- DKMS failures need `sudo dkms autoinstall` and a log in `/var/lib/dkms/*/build/make.log`.

### 7. Reverting or switching drivers safely
- Boot an older kernel from systemd-boot/GRUB to confirm the regression is driver-related.
- Remove old drivers before switching to avoid Xorg/Wayland config conflicts:
```bash
sudo pacman -Rns nvidia nvidia-utils
sudo pacman -S --needed mesa xf86-video-nouveau
```

## Common Pitfalls
- Forgetting `mkinitcpio -P` after installing CPU microcode or early firmware.
- Mixing NVIDIA `dkms` with `nvidia-utils` from different package repos or versions.
- Assuming a missing device is a driver problem; if `lspci` or `lsusb` does not show it at all, suspect firmware/ACPI before the OS.
- Removing `linux-firmware` by accident during cleanup; many devices disappear silently.
- Building DKMS modules on systems without `linux-headers` installed.

## References
- https://wiki.archlinux.org/title/NVIDIA
- https://wiki.archlinux.org/title/AMDGPU
- https://wiki.archlinux.org/title/Intel_graphics
- https://wiki.archlinux.org/title/DKMS
- https://wiki.archlinux.org/title/Hardware_detection
- https://wiki.archlinux.org/title/Kernel_mode_setting
