---
name: terminal-shell-repair
description: Diagnose why a command doesn't launch from a terminal emulator by inspecting shell chain, config files, login behavior, and shell location before editing anything.
triggers:
  - terminal not launching command
  - shell not autostarting
  - terminal emulator config
  - terminal uses wrong shell
---

# Terminal / Shell Autostart Repair

Use when the user reports:

- something should start on terminal launch but doesn't
- a terminal emulator seems to use the wrong shell

## Fixed Assumptions

- Default user: `nova` on Arch with Omarchy
- Kitty is common in this setup
- Default shell may be `/usr/bin/bash` while user expects `/usr/bin/zsh`

## Investigate Before Editing

Run these before changing any config.

```bash
# User identity and shell assignment
id
grep "^$(id -un):" /etc/passwd

# Valid shells
grep -v '^#' /etc/shells | grep -v nologin || true

# Where shells actually are
command -v bash zsh fish 2>/dev/null || true
ls -la /bin/zsh /usr/bin/zsh /usr/local/bin/zsh 2>/dev/null || true

# User dotfiles present
for f in /home/nova/.bashrc /home/nova/.zshrc /home/nova/.zprofile /home/nova/.zlogin /home/nova/.profile; do
  [ -f "$f" ] && echo "[$f]"
done

# Terminal emulator config paths/keys
grep -E '^(shell|login_shell)' /home/nova/.config/kitty/kitty.conf 2>/dev/null || true
```

## Diagnosis Mode

Run these checks in order and look for failures instead of guessing.

### Visual/no-output fallback

Sometimes the shell is launching but the terminal shows nothing. Check:

- terminal font present in `fc-list`
- terminal cursor visible (`kitty +kitten cursor` or similar probe)
- shell outputs early non-tty text in.dots that breaks drawing
- GPU driver or Hyprland output assertion contradicts find output

### Keyboard input fallback

When shell launches but keystrokes are ignored, check kitty input mappings:

- map keys collide with window manager bindings
- compose key or input method defaults override expected layout
- special keys faked by existing `.XCompose` or fcitx/ibus config

### Slow startup / session timeout

When headers appear but prompts never show, check shell extension load path:

- NVM, pyenv, Rustup, rbenv slowpath from `.zprofile` or `.bash_profile`
- ssh-agent pinentry hang in headless session
- hybrid login shells initiated by `.bashrc` instead of profile equivalents

## Common Causes

- Terminal emulator inherits `$SHELL`
- `.zshrc` is skipped when zsh starts as a login shell
- Shell binary path differs from assumed path
- `shell /usr/bin/zsh` in kitty.conf when `/usr/bin/zsh` doesn't exist
- `chsh` not run; default still `/usr/bin/bash`

## Common Rendering Fallbacks

These apply alongside shell-autostart issues when the terminal starts but either appears blank, shows wrong glyphs, or does not display UI correctly:

- cached PGO or asan runtimes left in profile dotfiles after X11 session cleanup
- locale mismatch outputs CJK escape sequences while terminal expects UTF-8
- graphical console reused without clearing framebuffer buffers
- duplicated `Window` rules in Hyprland targeting terminal class by pid instead of class string
- Pixi Rust source file indentation doubling plugin errors in shell prompts after intentional edits

## Pitfalls

- Do not assume `/etc/shells` contains every installed shell. On Arch, `/usr/bin/zsh` can exist even if `/etc/shells` doesn't list it yet for `chsh`.
- When removing a broken config line, verify the bad line is actually gone before adding the replacement; otherwise both can coexist.
- `sed` can mis-fire on similarly-named keys like `shell_integration`; prefer checking with `grep -E '^shell '` first.
- Do not set `shell /usr/bin/zsh` in kitty.conf unless zsh is confirmed installed at that exact path.

- Read config first
- Confirm exact line/setting to change
- Only then add or replace setting
- Always verify by re-reading the file after edit

Do not hardcode `/usr/bin/zsh` if that location hasn't been proven to exist. If not, run a file existence check first.