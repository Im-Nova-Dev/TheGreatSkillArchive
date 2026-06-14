#!/usr/bin/env bash
# hyprland-capture-evidence.sh — reproducible Hyprland evidence capture
# Part of the hyprland-logging-and-evidence skill
# Usage: hyprland-capture-evidence.sh [--output-dir DIR] [--no-screenshot] [--compare-with PREV_DIR]

set -euo pipefail

OUTPUT_DIR="${1:-$HOME/hyprland-evidence}"
NO_SCREENSHOT=false
COMPARE_WITH=""

# Parse args
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