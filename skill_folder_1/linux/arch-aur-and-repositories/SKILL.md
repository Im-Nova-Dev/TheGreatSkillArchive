{
  "name": "arch-aur-and-repositories",
  "description": "Teach Arch User Repository (AUR): PKGBUILD anatomy, building safely with yay, repo priorities, and common AUR failure modes."
}

# Arch Aur And Repositories

Teach Arch User Repository (AUR): PKGBUILD anatomy, building safely with yay/paru, repo priorities, and common AUR failure modes.

## Core Concepts
- AUR workflow is: fetch AUR package -> resolve deps -> build PKGBUILD in clean chroot/environment -> install built binaries.
- AUR helpers are not official; use them to automate fetch/build, not to replace understanding of PKGBUILD.
- Building still requires the base development toolchain (`base-devel`) and a GPG setup that can verify sources.

## Procedure
1. Identify the practical scenario.
2. Apply one focused approach that solves it.
3. Verify success with a simple command or check.

## Practical Troubleshooting Workflow

### 0. Diagnose repo and database health first
If `pacman -Syu` fails, check local and remote package state before blaming the AUR.
```bash
sudo pacman -Syy                              # refresh databases only
sudo pacman -Su --print 2>&1 | tail -n +1     # show pending upgrade transactions
pactree -r <package>                          # show reverse dependency chain for a package
paccheck --quiet || paccheck                   # audit local package consistency (requires pacman-contrib)
```
Common repo/db signals:
- `target not found` after `-Syy` means the package moved repos or was dropped, not usually a mirror issue.
- `conflicting files` or `exists in filesystem` indicates a database or filesystem collision; check with `sudo pacman -Qk <package>` before `--overwrite`.
- `PGP signature` or `invalid or corrupted package` means refresh keys / mirrors / `pacman-key --init` / `pacman-key --populate archlinux` or check `pacman.log`.

### 1. Pick or detect an AUR helper
```bash
paru --version || yay --version || echo no-aur-helper
```
- If neither paru nor yay is installed, install one explicitly (these commands just detect first):
```bash
# paru
git clone https://aur.archlinux.org/paru.git /tmp/paru
cd /tmp/paru && makepkg -si --noconfirm && cd -
```
```bash
# yay
git clone https://aur.archlinux.org/yay.git /tmp/yay
cd /tmp/yay && makepkg -si --noconfirm && cd -
```
Do **not** build random AUR packages as root directly. Use a regular user.

### 2. Verify build prerequisites exist
```bash
pacman -Qk base-devel >/dev/null 2>&1 || pacman -S --needed --noconfirm base-devel
git --version >/dev/null 2>&1 || pacman -S --needed --noconfirm git
gpg --version >/dev/null 2>&1 || pacman -S --needed --noconfirm gnupg
```
If any needed group is missing, reinstall it:
```bash
pacman -S --needed base-devel
```

### 3. Resolve repository and AUR ordering conflicts
When a package exists in both official repos and AUR:
- Prefer official repo version unless you explicitly need AUR features.
- If the AUR version is newer but official package would still be pulled as a dependency, either wait for the official update or use the AUR version for that dependency chain intentionally.
Check what would be installed before confirming:
```bash
# paru
paru -Si <package>
# yay
yay -Si <package>
```

### 4. Confirm an AUR build cleanly instead of blindly installing
Use the helper’s print flag or fall back to manual makepkg:
```bash
paru -Sp --print <package> | less
yay -Sp <package> | less
```
Or manually:
```bash
git clone https://aur.archlinux.org/<package>.git /tmp/<package>
cd /tmp/<package>
makepkg -si --noconfirm
cd -
```
Manual makepkg gives the strongest signal: if it fails, you see the failing source/build step directly.

### 5. Handle common AUR failure modes
- **Missing source / upstream moved**: check upstream URL, update PKGBUILD `source=` accordingly, preserve provided checksums by rerunning updpkgsums.
- **Signature / checksum mismatch**: upstream release changed after AUR snapshot. Run `updpkgsums` then rebuild. If GPG sig is required and missing, import the correct key instead of disabling verification.
- **Dependency name changed**: official package renamed, but AUR PKGBUILD still expects old name. Patch `depends=` or file a PKGBUILD update.
- **Build fails after kernel/glibc update**: some AUR packages need rebuild. Remove stale build artifacts in `/tmp/<package>` and rebuild.

### 6. Clean up after AUR builds
AUR helpers cache built `.pkg.tar.zst` files under `~/.cache/<helper>/pkg` or build directories under `/tmp`.
```bash
paru -Sc
yay -Sc
```

## Common Pitfalls
- Using `makepkg -si` as root without `--noconfirm` and without reading PKGBUILD is unsafe. Read PKGBUILD first if you don’t know the maintainer.
- Relying on an AUR helper to paper over missing `base-devel`. Fix `base-devel` first; many AUR build failures trace back to missing `fakeroot`, `patch`, `diffutils`, or `autoconf`.
- Forgetting that AUR packages are user-produced content. Prefer well-maintained PKGBUILDs with recent activity, and inspect `pkgver`, `source`, and `sha512sums` before building.
- Keeping stale cloned AUR repos under `/tmp` from previous failed builds; they often mask fetcher failures.

## References
- https://wiki.archlinux.org/title/Arch_User_Repository
- https://wiki.archlinux.org/title/AUR_helpers
- https://wiki.archlinux.org/title/PKGBUILD
