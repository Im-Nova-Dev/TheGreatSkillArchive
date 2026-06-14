#!/usr/bin/env bash
# nft-trace.sh — Quick packet trace for a port/IP
# Part of the linux-firewall-and-nftables skill
# Usage: nft-trace.sh [inet|ip|ip6] <table> <chain> <match-expression>
# Example: nft-trace.sh inet filter input "tcp dport 22"
# Example: nft-trace.sh ip nat prerouting "ip daddr 203.0.113.10"

set -euo pipefail
FAMILY="${1:-inet}"
TABLE="${2:-filter}"
CHAIN="${3:-input}"
MATCH="${4}"

if [[ -z "$MATCH" ]]; then
  echo "Usage: $0 <family> <table> <chain> <match>"
  exit 1
fi

HANDLE=$(nft -a add rule "$FAMILY" "$TABLE" "$CHAIN" "$MATCH" meta nftrace set 1 2>&1 | grep -oP 'handle \K\d+' || true)
if [[ -z "$HANDLE" ]]; then
  echo "Failed to add trace rule"
  exit 1
fi

echo "Trace rule added (handle $HANDLE). Watching kernel log (Ctrl+C to stop)..."
journalctl -k -f -o cat | grep --line-buffered -i nftrace

# Cleanup on exit
trap "nft delete rule '$FAMILY' '$TABLE' '$CHAIN' handle '$HANDLE' 2>/dev/null || true" EXIT