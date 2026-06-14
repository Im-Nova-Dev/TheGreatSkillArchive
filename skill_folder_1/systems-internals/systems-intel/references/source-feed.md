# Systems Intelligence Source Feeds

## Primary Kernel & Subsystem Feeds

### LWN.net (Kernel Coverage)
- **Kernel index**: https://lwn.net/Kernel/Index/
- **Articles**: https://lwn.net/Articles/
- **Search**: `site:lwn.net "Linux" "block" OR "scheduler" OR "bpf" OR "filesystem" OR "memory"`
- **Slack/Discord alerts**: LWN has RSS for kernel articles

### Linux Kernel Mailing List (LKML)
- **Main**: https://lore.kernel.org/lkml/
- **Block layer**: https://lore.kernel.org/linux-block/
- **BPF**: https://lore.kernel.org/bpf/
- **io_uring**: https://lore.kernel.org/io-uring/
- **Filesystems**: https://lore.kernel.org/linux-fsdevel/
- **Memory management**: https://lore.kernel.org/linux-mm/
- **Scheduler**: https://lore.kernel.org/kernel-sched/
- **SCSI/NVMe**: https://lore.kernel.org/linux-scsi/ https://lore.kernel.org/linux-nvme/

### Kernel.org & Git Direct
- **Changelogs**: https://cdn.kernel.org/pub/linux/kernel/v6.x/ChangeLog-6.X.Y
- **Git log**: `git log --oneline --since="2 weeks ago" -- kernel/block/ fs/ mm/ kernel/sched/`
- **Merge window tracking**: https://kernelnewbies.org/Linux_6.X

## Security & Vulnerability Feeds

### CVE & Advisory Sources
- **NVD**: https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all&cve_start_date=2026-01-01
- **Linux kernel CVE tracking**: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/HEAD?h=security
- **Distro advisories**:
  - Red Hat: https://access.redhat.com/security/cve
  - Ubuntu: https://ubuntu.com/security/notices
  - Debian: https://security-tracker.debian.org/tracker/
  - Arch: https://security.archlinux.org/
  - SUSE: https://www.suse.com/security/cve/

### Security Research Blogs
- **Google Project Zero**: https://googleprojectzero.blogspot.com/
- **GRSEC / Brad Spengler**: https://grsecurity.net/
- **Qualys**: https://blog.qualys.com/
- **SentinelOne**: https://www.sentinelone.com/labs/
- **Microsoft Security**: https://msrc.microsoft.com/blog/

## Scheduler & BPF Specialized

### sched-ext / scx
- **GitHub**: https://github.com/sched-ext/scx
- **Releases**: https://github.com/sched-ext/scx/releases
- **Discord/Slack**: sched-ext community channels

### eBPF / BPF
- **bpf.io**: https://bpf.io/
- **Cilium blog**: https://cilium.io/blog/
- **eBPF Summit recordings**: https://www.youtube.com/c/ebpffoundation
- **IOVisor**: https://iovisor.org/

## Filesystem & Storage

### Btrfs
- **Wiki**: https://btrfs.wiki.kernel.org/
- **Mailing list**: https://lore.kernel.org/linux-btrfs/
- **btrfs-progs**: https://github.com/kdave/btrfs-progs

### XFS
- **Mailing list**: https://lore.kernel.org/linux-xfs/
- **xfsprogs**: https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/

### ext4
- **Mailing list**: https://lore.kernel.org/linux-ext4/
- **e2fsprogs**: https://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git/

### NVMe / Block Layer
- **NVM Express org**: https://nvmexpress.org/
- **linux-nvme**: https://lore.kernel.org/linux-nvme/
- **NVMe spec**: https://nvmexpress.org/specifications/

### Atomic Writes & Untorn I/O
- **LWN 1009298**: Support for atomic block writes in 6.13
- **Kernel docs**: `filesystems/ext4/atomic_writes.html`

## Database Internals

### PostgreSQL
- **Buffer manager evolution**: Postgres buffer manager locking history (8.1→9.5→14+)
- **Source**: https://git.postgresql.org/gitweb/?p=postgresql.git
- **commitfest**: https://commitfest.postgresql.org/

### MySQL / InnoDB
- **Source**: https://github.com/mysql/mysql-server
- **InnoDB internals**: https://dev.mysql.com/doc/internals/en/

### LMDB / Embedded
- **Source**: https://github.com/LMDB/lmdb
- **LMDB buffer rings + WAL**: University-cs/database-internals/lmdb-buffer-rings-wal

## Networking & Hardware

### AF_XDP / io_uring / XSK
- **io_uring**: https://kernel.dk/io_uring.pdf (Jens Axboe's design doc)
- **AF_XDP**: https://www.kernel.org/doc/html/latest/networking/af_xdp.html
- **xdp-newbies**: https://lore.kernel.org/bpf/

### NIC Offload & RDMA
- **Mellanox/NVIDIA**: https://docs.nvidia.com/networking/
- **RDMA Core**: https://github.com/linux-rdma/rdma-core
- **NetDev conference**: https://netdevconf.org/

## Memory Management

### MGLRU / Page Cache
- **MGLRU thread**: "Multi-gen LRU" on linux-mm
- **Yu Zhao's talks**: LSFMM 2024/2025/2026 presentations

### CXL / Memory Disaggregation
- **LSFMM 2026**: https://linuxplumbersconf.org/2026/
- **CXL consortium**: https://www.computeexpresslink.org/

## Aggregators & Monitor Tools

### RSS / Feed Readers
- **LWN RSS**: https://lwn.net/headlines/rss
- **Kernel Planet**: https://planet.kernel.org/rss20.xml
- **Phoronix**: https://www.phoronix.com/rss.php

### Change Detection
- **Visualping / Distill.io**: For changelog pages
- **GitHub watches**: sched-ext/scx, torvalds/linux (kernel/block, fs/btrfs, mm/, kernel/sched/)
- **GitHub release webhooks**: All major kernel subsystems

## Search Queries for Weekly Sweep

```bash
# LWN search
site:lwn.net (atomic OR untorn OR sched_ext OR bpf OR io_uring OR mglru OR cxl) "2026"

# LKML search
site:lore.kernel.org (CVE OR "regression" OR "fix" OR "patch") "2026" linux-(block|mm|sched|fs|bpf)

# GitHub search
repo:torvalds/linux path:kernel/block OR path:fs/btrfs OR path:mm/ OR path:kernel/sched/ pushed:>2026-06-01

# NVD search
CVE-2026-* linux kernel
```

## Feed Maintenance Notes

- **Review monthly**: Remove dead feeds, add new ones
- **Priority**: LWN > LKML > distro advisories > security blogs > GitHub watches
- **Automation**: Consider GitHub Actions / cron jobs to auto-fetch changelog diffs
- **Alert thresholds**: Any CVE in kernel block/mm/sched/bpf/fs = immediate collect