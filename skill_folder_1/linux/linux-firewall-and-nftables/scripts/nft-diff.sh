#!/usr/bin/env bash
# nft-diff.sh — Compare current ruleset with backup
# Part of the linux-firewall-and-nftables skill
# Usage: nft-diff.sh <backup-file>

set -euo pipefail
BACKUP="${1}"
CURRENT="/tmp/nft-current-$(date +%s).txt"

if [[ -z "$BACKUP" ]]; then
  echo "Usage: $0 <backup-file>"
  exit 1
fi

if [[ ! -f "$BACKUP" ]]; then
  echo "Backup file not found: $BACKUP"
  exit 1
fi

nft list ruleset > "$CURRENT"
diff -u "$BACKUP" "$CURRENT" | head -200