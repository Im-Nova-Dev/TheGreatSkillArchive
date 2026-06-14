---
name: linux-firewall-and-nftables
description: Practical nftables firewall troubleshooting on Arch/Linux: rule inspection, debugging dropped packets, table/chain debugging, common breakage patterns, and recovery procedures.
---

# Linux Firewall and Nftables Troubleshooting

Practical workflow for debugging nftables rulesets on Arch-based systems. Focuses on live inspection, packet tracing, and common breakage patterns rather than teaching nftables syntax.

## When to use

- Connectivity works on some ports but not others after a ruleset change
- `nft list ruleset` output doesn't match expectations or shows duplicates
- Service (SSH, Docker, VPN, libvirt, podman) stops accepting connections after update
- Need to trace a specific packet flow through chains
- Docker/podman CNI conflicts with manual nftables rules
- Boot fails or hangs at "Starting nftables" due to syntax error in `/etc/nftables.conf`
- Want to verify ruleset persistence across reboots

## Platform

Arch Linux, Omarchy, any systemd-based distro using nftables (the iptables legacy backend)

## Core Concepts

- **Tables**: Containers for chains (families: `ip`, `ip6`, `inet`, `arp`, `bridge`, `netdev`)
- **Chains**: Ordered rule lists attached to Netfilter hooks (`input`, `output`, `forward`, `prerouting`, `postrouting`, `ingress`)
- **Rules**: Match criteria + action (`accept`, `drop`, `reject`, `jump`, `goto`, `return`, `queue`, `continue`, `log`, `counter`, `limit`, `meter`, `nat`, `tproxy`, `dup`, `fwd`)
- **Sets/Dictionaries/Meters**: Dynamic data structures for IP lists, port sets, rate limiting, connection tracking
- **Hooks & Priority**: Each chain has a hook type and priority; lower numbers run first. Standard priorities: `-300` (filter), `-150` (mangle), `-100` (security), `0` (raw), `100` (nat)
- **Base chains vs regular chains**: Base chains attach to Netfilter hooks; regular chains are jump targets only
- **Atomic ruleset replacement**: `nft -f` replaces atomically; partial `nft add` commands are not atomic

## Practical Troubleshooting Workflow

### 0. Baseline: capture current state before any changes

```bash
# Full ruleset (human-readable)
nft list ruleset > ~/nft-backup-$(date +%Y%m%d-%H%M%S).txt

# JSON for programmatic diff
nft -j list ruleset > ~/nft-backup-$(date +%Y%m%d-%H%M%S).json

# Per-table
for t in $(nft list tables | awk '{print $2}'); do
  nft list table inet "$t" 2>/dev/null || nft list table ip "$t" 2>/dev/null || nft list table ip6 "$t" 2>/dev/null
done
```

### 1. Verify ruleset loads without errors

```bash
# Dry-run validation (exits non-zero on syntax error, no changes applied)
nft -c -f /etc/nftables.conf

# Load with verbose output
nft -f /etc/nftables.conf
# If it fails, the error points to line/col in the file
```

**Common load-time failures:**
- Missing `flush ruleset` at top (old rules persist, duplicates accumulate)
- Duplicate table/chain definitions
- Invalid hook/priority combination
- Reference to undefined set/dictionary/map
- Using `ip` family keywords in `inet` table (or vice versa) without proper syntax

### 2. Inspect live ruleset structure

```bash
# All tables
nft list tables

# All chains in a table with handles
nft -a list table inet filter

# Specific chain with rule handles (critical for deletion/insertion)
nft -a list chain inet filter input

# Show rules with packet/byte counters
nft list chain inet filter input
nft list chain inet filter forward

# Show sets/maps with elements
nft list set inet filter myset
nft list map inet filter mymap
```

### 3. Trace a specific packet flow (the single most useful debug tool)

```bash
# Enable tracing for a specific chain (requires kernel 5.10+)
nft add rule inet filter input meta mark set 0x1 ip saddr 192.0.2.1 meta nftrace set 1
# Or trace all packets in a chain temporarily
nft add rule inet filter input meta nftrace set 1

# Watch traces in kernel log
journalctl -k -f | grep -i nftrace
# Or
dmesg -w | grep -i nftrace
```

**Trace output decodes to:**
- `trace id X rule Y` — rule number in chain
- `verdict accept/drop/continue/jump/goto/return` — action taken
- `mark`, `iif`, `oif`, `proto`, `sport`, `dport` — packet metadata
- `chain X` — chain entered/exited

**Remove trace rule after debugging:**
```bash
nft delete rule inet filter input handle <handle-from-nft-a-list>
```

### 4. Debug dropped connections (SYN sent, no SYN-ACK)

```bash
# 1. Confirm packet arrives at interface
tcpdump -ni any -c 5 'tcp[tcpflags] & tcp-syn != 0 and dst port 22'

# 2. Check conntrack state
conntrack -L -p tcp --dport 22

# 3. Trace in nftables (see step 3)
nft add rule inet filter input tcp dport 22 meta nftrace set 1
journalctl -k -f | grep -i nftrace

# 4. Common causes:
#    - Rule order: drop rule before accept in same chain
#    - Missing CT established/related rule before new connection rules
#    - Wrong interface match (iifname vs iif)
#    - IPv6 vs IPv4 table mismatch (service listening on :: but rule only in ip table)
#    - Docker/podman inserting rules in FORWARD chain that conflict
```

### 5. Debug NAT / port forwarding failures

```bash
# List nat table chains
nft list table ip nat
nft list table ip6 nat

# Check prerouting (DNAT) and postrouting (SNAT/MASQUERADE) chains
nft -a list chain ip nat prerouting
nft -a list chain ip nat postrouting

# Trace a forwarded packet
nft add rule ip nat prerouting ip daddr 203.0.113.10 tcp dport 80 meta nftrace set 1
journalctl -k -f | grep -i nftrace
```

**Common NAT breakage:**
- Missing `masquerade`/`snat` in postrouting for outbound
- DNAT rule in prerouting but no matching filter rule in forward chain
- Conntrack zones mismatch (Docker uses zones)
- `tcp dport` match before DNAT vs after DNAT (use `dnat to` then filter on real destination)

### 6. Debug Docker / podman / CNI conflicts

```bash
# Show all tables (Docker creates DOCKER, DOCKER-USER, etc. in filter/nat)
nft list tables

# Docker typically uses iptables-nft (legacy API over nftables)
# Check for duplicate/conflicting rules
nft list chain ip filter FORWARD
nft list chain ip nat POSTROUTING

# If using podman with CNI, it may create its own tables
nft list table cni-*

# Best practice: put custom rules in a dedicated table with higher priority base chains,
# or use DOCKER-USER chain (filter) which Docker preserves
```

### 7. Debug ruleset persistence across reboots

```bash
# Arch: systemd service is nftables.service
systemctl status nftables

# Check what it loads
cat /usr/lib/systemd/system/nftables.service
# ExecStart=/usr/bin/nft -f /etc/nftables.conf

# Verify file exists and is valid
nft -c -f /etc/nftables.conf

# Test reload
systemctl reload nftables
nft list ruleset | head -50
```

**Persistence failure modes:**
- `/etc/nftables.conf` missing or not readable by service user
- Syntax error in file (service fails, old ruleset stays active)
- `flush ruleset` missing → each reboot accumulates duplicates
- Service not enabled: `systemctl enable nftables`
- Conflict with firewalld/ufw/iptables services also managing rules

### 8. Debug performance / rule evaluation cost

```bash
# Enable per-rule counters (add `counter` keyword to rules)
# Then view hit counts
nft -a list chain inet filter input

# For high-traffic chains, use `meter` for rate tracking
nft add rule inet filter input meter mymeter { ip saddr limit rate 100/second } drop

# Profile with perf (requires debug kernel)
perf record -g -e nftables:* sleep 10
perf report
```

## Common Breakage Patterns & Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `nft -f` fails with "Could not process rule: No such file or directory" | Set/map referenced before defined | Define sets/maps before rules that use them; order matters in file |
| SSH works from LAN but not WAN | Missing `iifname "eth0"` or wrong interface match | Use `iifname` for input, `oifname` for output; verify with `ip link` |
| IPv6 connections silently fail | Rules only in `ip` table, not `ip6` or `inet` | Use `inet` family for dual-stack; or duplicate in `ip6` |
| Docker containers can't reach internet | `POSTROUTING` MASQUERADE missing or wrong subnet | Ensure `ip saddr != 172.17.0.0/16 masquerade` in nat postrouting |
| Ruleset works but resets on reboot | `nftables.service` not enabled or `/etc/nftables.conf` missing | `systemctl enable nftables`; ensure file has `flush ruleset` |
| `nft list ruleset` shows duplicates after reload | No `flush ruleset` at top of config | Add `flush ruleset` as first line |
| `conntrack -L` shows INVALID state packets dropped | Missing `ct state established,related accept` early in input chain | Add `ct state established,related accept` as first rule in input |
| VPN (WireGuard/OpenVPN) handshake fails | UDP port not allowed in input chain before CT | Allow UDP port for VPN before ct state rules |
| `nft add rule` works but disappears after reload | Not persisted to `/etc/nftables.conf` | Edit config file, then `systemctl reload nftables` |

## Recovery Procedures

### Recover from broken ruleset locking you out (console access required)

```bash
# 1. Flush all rules (nuclear option - allows all traffic)
nft flush ruleset

# 2. Minimal safe ruleset for remote access
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input iifname "lo" accept
nft add rule inet filter input tcp dport 22 ct state new accept
nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; }
nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; }

# 3. Persist
nft list ruleset > /etc/nftables.conf
systemctl reload nftables
```

### Recover from syntax error in `/etc/nftables.conf` preventing boot

```bash
# From emergency shell or chroot
nft -c -f /etc/nftables.conf  # shows error line
# Fix the error
# Or temporarily replace with minimal config:
cat > /etc/nftables.conf <<'EOF'
flush ruleset
table inet filter {
  chain input { type filter hook input priority 0; policy drop; }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output { type filter hook output priority 0; policy accept; }
}
EOF
systemctl reload nftables
```

### Rollback to known-good ruleset

```bash
# If you keep timestamped backups (see step 0)
nft -f ~/nft-backup-20250601-143000.txt
nft list ruleset > /etc/nftables.conf
systemctl reload nftables
```

## Verification Checklist

After any change, run this sequence:

```bash
# 1. Config validates
nft -c -f /etc/nftables.conf

# 2. Service reloads cleanly
systemctl reload nftables && systemctl is-active nftables

# 3. Ruleset matches intent
nft list ruleset | grep -E '(table|chain|hook|priority|policy)'

# 4. Critical ports accessible
ss -ltn | grep -E ':(22|80|443|51820)\b'
# Test from another host
# nc -zv <host> 22

# 5. Counters increment on test traffic
nft -a list chain inet filter input | grep -E '(counter|packets|bytes)'

# 6. No INVALID conntrack drops in logs
journalctl -k --since "5 min ago" | grep -i "invalid\|drop\|nftables"
```

## Reusable Scripts

### `~/bin/nft-trace.sh` — Quick packet trace for a port/IP

```bash
#!/usr/bin/env bash
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
```

### `~/bin/nft-diff.sh` — Compare current ruleset with backup

```bash
#!/usr/bin/env bash
# Usage: nft-diff.sh <backup-file>

set -euo pipefail
BACKUP="${1}"
CURRENT="/tmp/nft-current-$(date +%s).txt"

nft list ruleset > "$CURRENT"
diff -u "$BACKUP" "$CURRENT" | head -200
```

## Related Skills

- `arch-troubleshooting` — boot, pacman, systemd umbrella
- `linux-networking-troubleshooting` — wired, Wi-Fi, DNS, connectivity
- `systemd-administration` — service debugging, journalctl patterns
- `wayland-hyprland-desktop` — if using Hyprland with custom firewall rules for apps

## References

- `man nft` — authoritative reference
- https://wiki.nftables.org/ — nftables wiki (examples, debugging, migration)
- https://wiki.archlinux.org/title/Nftables — Arch-specific service, config paths
- `man 8 nftables.service` — systemd service details
- https://netfilter.org/projects/nftables/ — upstream project