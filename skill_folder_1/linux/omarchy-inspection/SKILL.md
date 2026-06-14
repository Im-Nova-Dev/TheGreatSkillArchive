---
name: omarchy-inspection
description: Inspect the local Omarchy installation state, environment, and relevant config.
triggers:
  - omarchy inspection
  - omarchy setup
  - inspect omarchy
---

# Omarchy Setup Inspection

Use this procedure to inspect the user's Omarchy/Arch environment from `/home/nova`.

## Inspect Omarchy

```bash
command -v omarchy || true
ls -ld ~/.local/share/omarchy /etc/omarchy 2>/dev/null || true
sed -n '1,80p' ~/.local/share/omarchy/AGENTS.md 2>/dev/null | head -40 || true
```

## Inspect System + Environment

```bash
cat /etc/os-release 2>/dev/null | head -12
uname -a
id
grep "^$(id -un):" /etc/passwd || true
grep -v '^#' /etc/shells | grep -v nologin || true
command -v bash zsh fish 2>/dev/null || true
which pacman yay paru 2>/dev/null || true
printf 'EDITOR=%s\n' "${EDITOR:-}"
printf 'VISUAL=%s\n' "${VISUAL:-}"
git config --global user.name 2>/dev/null || true
git config --global user.email 2>/dev/null || true
which kitty ghostty alacritty foot wezterm 2>/dev/null || true
which fastfetch eza bat zoxide fzf zellij starship 2>/dev/null || true
```

## Inspect Dotfiles

```bash
for f in /home/nova/.bashrc /home/nova/.zshrc /home/nova/.zprofile /home/nova/.zlogin /home/nova/.profile; do
  [ -f "$f" ] && echo "[$f]"
done
```

## Inspect Services

```bash
systemctl --user list-unit-files --type=service --state=enabled 2>/dev/null | head -30 || true
```

## Inspect Omarchy Capture Tools

```bash
omarchy capture --help 2>/dev/null | head -40 || true
command -v grim slurp 2>/dev/null || true
```

## Save to Memory

Use `memory(action='add')` to record OS, kernel, shell, Omarchy path, desktop/themes, user name/email, active services, and obvious toolchain preferences. Keep entries under 2 KB total.