---
name: linux-networking-troubleshooting
description: Practical Arch/Omarchy network recovery: wired, Wi-Fi, resolv.conf and DNS, connectivity checks, and common breakage patterns.
tags: [linux, arch, networking, wifi, dns, troubleshooting]
---

# Linux Networking Troubleshooting

Reproducible recovery for LAN, Wi-Fi, and DNS issues on Arch / Omarchy / Hyprland systems. Use when the network is down, flaky, DNS breaks, or Wi-Fi fails after suspend/update/reboot.

## Quick decision tree

1. Show current interfaces/IP and default route.
2. Determine link type: wired vs Wi-Fi.
3. Fix link.
4. Fix DNS.
5. Verify.

## 1. Inspect state

```bash
ip -brief addr
ip route
resolvectl status 2>/dev/null || true
cat /etc/resolv.conf 2>/dev/null || true
```

If `systemd-networkd` or `NetworkManager` is running, prefer their status:
```bash
systemctl is-active NetworkManager
systemctl is-active systemd-networkd
journalctl -u NetworkManager --since '20 min ago' --no-pager
```

## 2. Wired LAN

If link is down:
```bash
ip link set eth0 up
dhcpcd -q eth0          # optional
```

If IPed but no default route:
```bash
ip route add default via 192.168.1.1 dev eth0
```

If static config is desired, prefer `/etc/systemd/network/` profiles over raw `networkctl` configuration so it survives reboot.

## 3. Wi-Fi

### iwctl (most Arch installs)
```bash
iwctl station list
iwctl station wlan0 scan
iwctl station wlan0 get-networks
iwctl station wlan0 connect SSID
```

After connect, retry `ip route` and `resolvectl`.

### NetworkManager CLI
```bash
nmcli device wifi list
nmcli device wifi connect SSID password PASS
nmcli connection show
```

### Post-suspend Wi-Fi flakiness
Suspend often drops the killswitch state on laptops.
```bash
rfkill unblock wifi
rfkill list
iwctl station wlan0 show
iwctl station wlan0 reconnect
```

If `wlan0` is missing:
```bash
rfkill unblock all
ip link set wlan0 up
```

## 4. DNS

### Symptom: ping IP works, names do not resolve.

If using systemd-resolved:
```bash
resolvectl flush-caches
resolvectl status
resolvectl domain lo # expect localhost
resolvectl domain <iface>
```

Quick test:
```bash
dig heise.de +short +timeout=2 || host heise.de || nslookup heise.de
```

### resolv.conf fix
Do not write arbitrary resolvers manually if systemd-resolved is active. Either:
- symlink `/etc/resolv.conf` to `/run/systemd/resolve/stub-resolv.conf`, or
- set `systemd-resolved` with system `/etc/systemd/resolved.conf`:
  ```ini
  [Resolve]
  DNS=1.1.1.1 8.8.8.8
  FallbackDNS=9.9.9.9
  ```

After modifying:
```bash
systemctl restart systemd-resolved
resolvectl flush-caches
```

If resolver keeps getting overwritten by DHCP, set `systemd-resolved` or `NetworkManager` to ignore DHCP-provided DNS servers.

### No local DNS
When VPN/DNS-over-HTTPS conflicts break name resolution, disable the extra resolver temporarily and rely on one source at a time.

## 5. Verify

```bash
ip route
ping -c3 1.1.1.1
getent hosts heise.de || dig heise.de +short +timeout=2
```

If both succeed, layer services back on one at a time (VPN, proxy, firewall rules).

## Common pitfalls

- Editing `/etc/resolv.conf` directly when systemd-resolved or NetworkManager is active. The file is often a symlink or symlink conflict.
- Assuming wireless interface is `wlan0`. On modern kernels it can be `wlp2s0`, `wlan1`, etc. Use `ip link`.
- Forgetting VPN DNS takes precedence. Flush `resolvectl` caches after reconnecting or disabling VPN.
- `nmcli` forgetting connections after reinstall/update: use `nmcli connection export` and re-import.
- `systemd-networkd` and NetworkManager simultaneously managing the same interface. Disable one per interface.
- IPv6-only tunnels combined with broken `rfc3307` networkd configs on some installs; fallback to IPv4 DNS or native RA.

## References

- Arch Wiki: Network configuration
- Arch Wiki: systemd-networkd
- Arch Wiki: NetworkManager
- Arch Wiki: Wi-Fi troubleshooting
- Arch Wiki: Domain name resolution
