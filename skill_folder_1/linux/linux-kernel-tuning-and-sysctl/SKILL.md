---
name: linux-kernel-tuning-and-sysctl
description: Tune Linux kernel behavior with sysctl on Arch-based systems, with concrete hints for storage, network, virtualization, and desktop workloads.
---

# Linux Kernel Tuning And Sysctl

Use sysctl to make targeted, verifiable kernel changes on Arch/Omarchy. Favor persistence through `/etc/sysctl.d/*.conf` and validate with actual commands instead of guessing from docs.

## Core Concepts

- sysctl exposes `/proc/sys/...` tunables; `sysctl -a` lists them, `sysctl -w key=value` applies ephemerally, and `sysctl --system` loads persistent config.
- Config precedence: `/run/sysctl.d/*.conf`, `/etc/sysctl.d/*.conf`, `/usr/lib/sysctl.d/*.conf`, then `/etc/sysctl.conf`. Later files override earlier ones; drop-ins avoid editing global files.
- Keys use the path under `/proc/sys/` with `/` replaced by `.`, dots separated, and values are numeric or text booleans (`0`, `1`, `yes`, `no`).

## Practical Workflows

1. Auditor: find current effective values
```bash
sysctl -a --pattern '^(fs\.inotify|net\.core|vm\.swappiness|kernel\.sched|fs\.file)' | sort | head -120
uname -r; journalctl --since '10 min ago' -p 3..3 -o short-iso | tail -120
```

2. Apply a small change and verify
```bash
sudo sysctl -w fs.inotify.max_user_watches=524288
sysctl fs.inotify.max_user_watches
# restart relevant services and observe behavior, not just the sysctl line
```

3. Make it persistent as a drop-in
```bash
sudo tee /etc/sysctl.d/99-local-tuning.conf <<'EOF'
# flat-file overrides go here
fs.inotify.max_user_watches = 524288
EOF
sudo sysctl --system
```

4. Measure before/after
Use one concrete signal per change. Examples:
- file watcher saturation: `watch -n1 "cat /proc/sys/fs/inotify/max_user_watches"`
- syscall/event latency: `ioping -c 10 -s 4k /tmp`
- throughput baseline: `fio --name=baseline --rw=randread --bs=4k --numjobs=4 --size=1g --runtime=20 --time_based --group_reporting`
- scheduler noise: `perf stat -e task-clock,context-switches,cpu-migrations sleep 5`

## Key Tuning Areas

- File watching/Qt/Wayland/IDE users: increase `fs.inotify.max_user_watches` and `fs.inotify.max_user_instances` when editors, JetBrains IDEs, or browsers report watcher exhaustion.
- Desktop responsiveness: tuning `kernel.sched_rt_runtime_us` and `vm.swappiness` helps laptops under memory pressure, but heartbeat and battery behavior matter more than raw numbers.
- Storage and databases: align `vm.dirty_ratio`, `vm.dirty_background_ratio`, and `vm.dirty_bytes` with workload bursts to avoid latency spikes.
- Network services and containers: `net.core.somaxconn`, `net.ipv4.tcp_keepalive_*`, and `net.ipv4.ip_local_port_range` are practical for servers and port-heavy environments.
- Virtualization: `vm.max_map_count`, `kernel.pid_max`, and `net.core.rmem_default`/`wmem_default` become load-bearing when running nested VMs or WdP-style desktops.

## Verification Steps

- `sysctl --system` must end with “Applying /etc/sysctl.d/...”
- List a specific key after reboot: `sysctl -n key`
- Confirm boot loader still works after mkinitcpio regeneration if kernel modules or initramfs are changed.
- If a change breaks boot, boot an older kernel from the systemd-boot/GRUB menu and revert the offending file.

## Common Pitfalls

- Editing `/etc/sysctl.conf` directly and layering `/etc/sysctl.d/` overrides later, then getting surprised by precedence.
- Forgetting reload is not needed for most `sysctl -w` changes, but some subsystems require a service restart or module reload.
- Setting extreme values without a baseline: bad tuning is indistinguishable from no tuning.
- Treating tuning as a substitute for diagnosis: find the real bottleneck before changing scheduler knobs.
- On Arch, kernel upgrades invalidate module assumptions; if DKMS-built modules break after upgrade, rebuild them before tweaking sysctl.
