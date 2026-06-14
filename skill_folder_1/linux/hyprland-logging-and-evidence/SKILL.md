---
name: hyprland-logging-and-evidence
description: Capture reliable Hyprland debug evidence, identify common failure signals, and save logs/frames reproducibly.
---

# Hyprland Logging and Evidence Capture

## Platform
Linux, Arch-based, Arch, Hyprland, Omarchy

## Overview
When Hyprland regresses after an update, theme change, or config edit, the fastest repair path is good evidence: start logs, capture keywords, and save artifacts before the session ends. This skill documents where logs live, which patterns matter, and how to package them for later debugging or issue reports.

## When to use
- Hyprland dies immediately or shows a blank desktop with no obvious config edit
- You need a reproducible log before asking for help or filing an Omarchy/Hyprland issue
- You want before/after evidence around an update, theme switch, or config rewrite
- A bug report needs screenshots, logs, and config snapshots attached

## Log Sources

### Primary sources
- user journal for the current graphical session
  text
  bash
  journalctl --user -u hyprland --since "10 minutes ago"
  ```
- Compositor file log if configured in hyprland.conf
  text
  bash
  # Check whether a file log is enabled:
  hyprctl keyword -p | rg -i "logfile" || true
  # Default candidate:
  tail -n 200 /tmp/hyprland.log 2>/dev/null || true
  ```
- systemd user environment
  text
  bash
  systemctl --user status hyprland
  systemctl --user list-units --type=service --state=failed
  ```
- Hyprland protocol logs
  text
  bash
  hyprctl clients
  hyprctl monitors
  hyprctl workspaces
  hyprctl devices
  hyprctl keyword -p
  ```
- config and asset directories
  text
  bash
  ls -la ~/.config/hypr
  ls -la ~/.local/share/omarchy
  ```

### Secondary sources
- XDG runtime logs and Helvum/Wayland debug output
  text
  bash
  ls -lt /run/user/1000 2>/dev/null | head
  ```
- GPU and compositor diagnostics
  text
  bash
  glxinfo 2>/dev/null | head
  vulkaninfo 2>/dev/null | head
  ```
- Audio sink state when mixer appears silent
  text
  bash
  pactl list sinks short
  pactl info
  ```
- Display manager fallback session logs
  text
  bash
  journalctl -u gdm --since "20 minutes ago" --no-pager 2>/dev/null | tail -n 80
  journalctl -u sddm --since "20 minutes ago" --no-pager 2>/dev/null | tail -n 80
  ```

## Keyword patterns to surface fast
- config syntax drift: `does not exist|Invalid parameters|suppress_event_maximize|mscon_focus_under_fullscreen|no_focus on|opacity 0.97 0.9`
- rule migration gaps: `windowrule = |layerrule = `
- partial updates or missing files: `cannot open|No such file|ENOENT|missing theme|stale`
- GPU/auth blockers: `EGL|GLX|KMS|Failed to create backend|Permission denied`
- audio mixer mismatch: `card not found|no sinks|no active sink`

## Evidence capture workflow

### 1. Start from a clean capture baseline
  text
  bash
  mkdir -p ~/hyprland-evidence
  journalctl --user -u hyprland --since "-30 minutes" > ~/hyprland-evidence/journal.txt
  ```

### 2. Capture Hyprland runtime state
  text
  bash
  {
    echo === monitors ===
    hyprctl monitors
    echo === workspaces ===
    hyprctl workspaces
    echo === clients ===
    hyprctl clients
    echo === devices ===
    hyprctl devices
    echo === keywords ===
    hyprctl keyword -p
  } > ~/hyprland-evidence/hypr-runtime.txt
  ```

### 3. Save a screenshot or region capture
Requires grim + slurp. Run from TTY if the Wayland session is broken.
  text
  bash
  grim ~/hyprland-evidence/screenshot.png
  ```
Region capture:
  text
  bash
  grim -g "$(slurp)" ~/hyprland-evidence/region.png
  ```

### 4. Snapshot the relevant configs
  text
  bash
  {
    echo === hypr configs ===
    ls -la ~/.config/hypr
    for f in ~/.config/hypr/*.conf; do
      echo "--- $f ---"
      sed -n '1,220p' "$f"
    done
    echo === omarchy theme assets ===
    ls -la ~/.local/share/omarchy
  } > ~/hyprland-evidence/config-snapshot.txt
  ```

### 5. Package ready-to-attach artifacts
  text
  bash
  tar czf ~/hyprland-evidence.tgz -C ~ hyprland-evidence
  ```

## Recovery-oriented evidence
If the desktop is unusable:
1. Switch to TTY: `Ctrl+Alt+F2`
2. Capture logs from TTY before restarting or editing:
   text
   bash
   journalctl --user -u hyprland --since "-30 minutes" > ~/hyprland-evidence/journal.txt
   ```
3. Only then edit configs or restart the compositor.

## Troubleshooting decision tree
1. Is the journal full of `does not exist|Invalid parameters` after an update?
   yes => Capture `config-snapshot.txt`, then migrate `windowrule`/`layerrule` to `windowrulev2`/`layerrulev2`, reload, recapture.
2. Are monitors duplicated or workspace bindings wrong?
   yes => Capture `hypr-runtime.txt` from `hyprctl`, then normalize monitors/workspaces, reload, recapture.
3. Does audio appear silent with no sink activity?
   yes => Capture `pactl list sinks short`, fix mixer selector state, verify, recapture.
4. Does the log end at launch with no Hyprland service unit lines?
   yes => Check `systemctl --user status hyprland`, look for failed units or KMS/EGL backend failure, capture service output.

## Reusable Capture Script

Create a standalone script at `~/bin/hyprland-capture-evidence.sh` (or invoke from the skill directory):

```bash
#!/usr/bin/env bash
# hyprland-capture-evidence.sh — reproducible Hyprland evidence capture
# Usage: hyprland-capture-evidence.sh [--output-dir DIR] [--no-screenshot] [--compare-with PREV_DIR]

set -euo pipefail

OUTPUT_DIR="${1:-$HOME/hyprland-evidence}"
NO_SCREENSHOT=false
COMPARE_WITH="${2:-}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --no-screenshot) NO_SCREENSHOT=true; shift ;;
    --compare-with) COMPARE_WITH="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

mkdir -p "$OUTPUT_DIR"
TS=$(date '+%Y%m%d-%H%M%S')
ARCHIVE="$HOME/hyprland-evidence-$TS.tgz"

echo "=== Capturing evidence to $OUTPUT_DIR ==="

# 1. Journal (last 30 min by default; user can extend with JOURNAL_SINCE)
JOURNAL_SINCE="${JOURNAL_SINCE:--30 minutes}"
journalctl --user -u hyprland --since "$JOURNAL_SINCE" > "$OUTPUT_DIR/journal.txt"
echo "  journal: $(wc -l < "$OUTPUT_DIR/journal.txt") lines"

# 2. Runtime state
{
  echo "=== hyprctl monitors ==="; hyprctl monitors
  echo "=== hyprctl workspaces ==="; hyprctl workspaces
  echo "=== hyprctl clients ==="; hyprctl clients
  echo "=== hyprctl devices ==="; hyprctl devices
  echo "=== hyprctl keyword -p ==="; hyprctl keyword -p
} > "$OUTPUT_DIR/hypr-runtime.txt"
echo "  runtime: $(wc -l < "$OUTPUT_DIR/hypr-runtime.txt") lines"

# 3. Config snapshot
{
  echo "=== hypr config files ==="
  ls -la ~/.config/hypr 2>/dev/null || true
  for f in ~/.config/hypr/*.conf; do
    [ -f "$f" ] || continue
    echo "--- $f ---"
    sed -n '1,300p' "$f"
  done
  echo "=== omarchy theme assets ==="
  ls -la ~/.local/share/omarchy 2>/dev/null || true
  echo "=== active theme symlink ==="
  readlink -f ~/.config/omarchy/active 2>/dev/null || true
} > "$OUTPUT_DIR/config-snapshot.txt"
echo "  config snapshot: $(grep -c '^--- ' "$OUTPUT_DIR/config-snapshot.txt" || echo 0) files"

# 4. Screenshot (optional; requires grim; run from TTY if session broken)
if [[ "$NO_SCREENSHOT" != "true" ]] && command -v grim >/dev/null 2>&1; then
  grim "$OUTPUT_DIR/screenshot.png" 2>/dev/null && echo "  screenshot: captured" || echo "  screenshot: failed (session may be broken)"
fi

# 5. GPU/backend diagnostics
{
  echo "=== glxinfo ==="; glxinfo 2>/dev/null | head -30 || true
  echo "=== vulkaninfo ==="; vulkaninfo 2>/dev/null | head -30 || true
  echo "=== hyprctl devices (detailed) ==="; hyprctl devices -j 2>/dev/null || true
} > "$OUTPUT_DIR/gpu-backend.txt"

# 6. Package/version coherence
{
  echo "=== omarchy version ==="; omarchy --version 2>/dev/null || true
  echo "=== hyprland version ==="; hyprctl version 2>/dev/null || true
  echo "=== pacman omarchy ==="; pacman -Q omarchy 2>/dev/null || true
  echo "=== pacman hyprland ==="; pacman -Q hyprland 2>/dev/null || true
} > "$OUTPUT_DIR/versions.txt"

# 7. Optional: compare with previous capture
if [[ -n "$COMPARE_WITH" && -d "$COMPARE_WITH" ]]; then
  echo "=== DIFF vs $COMPARE_WITH ===" > "$OUTPUT_DIR/diff-report.txt"
  diff -u "$COMPARE_WITH/journal.txt" "$OUTPUT_DIR/journal.txt" 2>/dev/null | head -100 >> "$OUTPUT_DIR/diff-report.txt" || true
  diff -u "$COMPARE_WITH/hypr-runtime.txt" "$OUTPUT_DIR/hypr-runtime.txt" 2>/dev/null | head -100 >> "$OUTPUT_DIR/diff-report.txt" || true
  diff -u "$COMPARE_WITH/config-snapshot.txt" "$OUTPUT_DIR/config-snapshot.txt" 2>/dev/null | head -200 >> "$OUTPUT_DIR/diff-report.txt" || true
  echo "  diff report written"
fi

# 8. Package archive
tar czf "$ARCHIVE" --sort=name --mtime='' -C "$(dirname "$OUTPUT_DIR")" "$(basename "$OUTPUT_DIR")"
sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"
echo "=== Archive: $ARCHIVE ==="
echo "=== SHA256: $(cat "$ARCHIVE.sha256") ==="
```

Make it executable: `chmod +x ~/bin/hyprland-capture-evidence.sh`

## Bug Report Template (Hyprland / Omarchy)

When filing an issue upstream, include this template with your `hyprland-evidence-*.tgz`:

```
## Environment
- Distro: Arch / Omarchy (version: `omarchy --version`)
- Hyprland: `hyprctl version`
- Kernel: `uname -r`
- GPU: `glxinfo | grep -i renderer` / `vulkaninfo | grep -i deviceName`
- Compositor backend: Wayland (Hyprland)

## Steps to Reproduce
1.
2.
3.

## Expected vs Actual
- Expected:
- Actual:

## Evidence
- Attached: `hyprland-evidence-<timestamp>.tgz` (contains journal, runtime state, configs, versions, GPU info)
- Key log lines (paste from journal.txt):
```
<grep -i "error|fail|invalid|does not exist" journal.txt | head -20>
```

## Config Notes
- Active theme: `readlink -f ~/.config/omarchy/active`
- Custom configs in ~/.config/hypr/:
```
<list any non-stock files>
```

## Workarounds Tried
- [ ] `hyprctl reload`
- [ ] Reboot
- [ ] `omarchy-update`
- [ ] Rule migration (`windowrule` → `windowrulev2`, `layerrule` → `layerrulev2`)
- [ ] Theme switch via `omarchy-menu`

## Checklist
- [ ] Evidence tarball attached
- [ ] Steps to reproduce are minimal
- [ ] Config snapshot included (config-snapshot.txt)
- [ ] Version coherence checked (versions.txt)
```

Place this template at `~/templates/hyprland-bug-report.md` for quick reuse.

## Automated Before/After Comparison

After applying a fix (e.g., from `omarchy-hyprland-post-update-fix`), recapture and compare:

```bash
# 1. Capture pre-fix baseline
hyprland-capture-evidence.sh --output-dir ~/hyprland-evidence-pre

# 2. Apply fix (rule migration, theme repair, full update, etc.)

# 3. Capture post-fix state and diff against baseline
hyprland-capture-evidence.sh --output-dir ~/hyprland-evidence-post --compare-with ~/hyprland-evidence-pre

# 4. Review the diff
cat ~/hyprland-evidence-post/diff-report.txt
```

Key things to verify in the diff:
- **Config syntax errors disappear**: Lines containing `does not exist`, `Invalid parameters`, `suppress_event_maximize` should be absent in post-fix journal
- **Monitor/workspace state stabilizes**: `hyprctl monitors` output consistent, no duplicates
- **Theme assets resolve**: Active theme symlink points to valid directory with `hypr/` subfolder
- **No new fatal errors in last 60s** of post-fix journal

## Omarchy-Specific Failure Pattern Detection

Add these patterns to your evidence scan (`rg` against `journal.txt` and `hypr-runtime.txt`):

| Pattern | Meaning | Likely Fix Skill |
|---------|---------|------------------|
| `config option .* does not exist` | Config syntax drift | `omarchy-hyprland-post-update-fix` Fix 2 |
| `Invalid parameters.*windowrule\|layerrule` | Old rule keyword | `omarchy-hyprland-post-update-fix` Fix 2 |
| `opacity [0-9.]+ [0-9.]+` without `match:` | Pre-0.53 opacity format | `omarchy-hyprland-post-update-fix` Fix 2 |
| `windows\.conf\|looknfeel\.conf.*missing\|not found` | Theme assets missing | `omarchy-hyprland-post-update-fix` Fix 3 |
| `Picture\.{0,1}in\.{0,1}` | Bad regex quantifier | `omarchy-hyprland-post-update-fix` Fix 4 |
| `active.*theme.*broken\|symlink.*ENOENT` | Active theme link broken | `omarchy-hyprland-post-update-fix` Fix 3b |
| `EGL\|GLX\|KMS.*Failed to create backend` | GPU backend failure | Check drivers, `mkinitcpio-and-boot` |
| `no sinks\|no active sink\|card not found` | Audio mixer selector drift | `wayland-hyprland-desktop` §2 |
| `surprise.*generator` | Animation fallback | `wayland-hyprland-desktop` §4 |
| `workspace = [0-9]+` without `monitor:` | Workspace rule conflict | `wayland-hyprland-desktop` §1 |

Quick scan one-liner:

```bash
rg -n \
  -e "config option .* does not exist" \
  -e "Invalid parameters.*(windowrule|layerrule)" \
  -e "opacity [0-9.]+ [0-9.]+" \
  -e "(windows|looknfeel)\.conf.*(missing|not found)" \
  -e "Picture\.\\{0,1\\}in\.\\{0,1\\}" \
  -e "active.*theme.*broken|symlink.*ENOENT" \
  -e "(EGL|GLX|KMS).*Failed to create backend" \
  -e "no sinks|no active sink|card not found" \
  -e "surprise.*generator" \
  -e "workspace = [0-9]+$" \
  ~/hyprland-evidence/journal.txt ~/hyprland-evidence/hypr-runtime.txt 2>/dev/null
```

## Verification

- `~/hyprland-evidence.tgz` exists and contains `journal.txt`, `hypr-runtime.txt`, `config-snapshot.txt`, `gpu-backend.txt`, `versions.txt`
- Capture script `~/bin/hyprland-capture-evidence.sh` runs without errors from TTY or broken session
- Tarball is complete: `tar tzf ~/hyprland-evidence-*.tgz | sort`
- After fix, recapture with `--compare-with` shows no new fatal config errors in `diff-report.txt`
- Bug report template at `~/templates/hyprland-bug-report.md` used for upstream issues

## Repro Packaging Checklist

1. Confirm artifacts before archive:
```bash
ls -l ~/hyprland-evidence/journal.txt ~/hyprland-evidence/hypr-runtime.txt ~/hyprland-evidence/config-snapshot.txt ~/hyprland-evidence/gpu-backend.txt ~/hyprland-evidence/versions.txt
```
2. Rebuild the archive deterministically:
```bash
tar czf ~/hyprland-evidence.tgz --sort=name --mtime='' -C ~ hyprland-evidence
```
3. Verify the archive entry list:
```bash
tar tzf ~/hyprland-evidence.tgz | sort
```
4. Optional checksum for transfer:
```bash
sha256sum ~/hyprland-evidence.tgz
```
5. Optional readable summary for reports:
```bash
echo 'journal lines:'; wc -l ~/hyprland-evidence/journal.txt
echo 'runtime state:'; wc -l ~/hyprland-evidence/hypr-runtime.txt
echo 'config snapshot files captured:'; grep -c '^--- ' ~/hyprland-evidence/config-snapshot.txt
```

## Related Skills
- `omarchy-hyprland-post-update-fix` — targeted fixes for captured failure patterns
- `wayland-hyprland-desktop` — monitor/workspace/audio/input troubleshooting
- `arch-troubleshooting` — boot, pacman, systemd umbrella
- `hyprland-config-migration` (if exists) — systematic windowrulev2/layerrulev2 migration
- `mkinitcpio-and-boot` — GPU backend / initramfs recovery when EGL/KMS fails
