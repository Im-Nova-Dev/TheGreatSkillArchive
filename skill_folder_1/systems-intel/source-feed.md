# Systems Intelligence Source Feeds

Curated list of high-signal sources for systems internals, kernel development, database internals, networking, and storage systems content.

## Kernel & OS Internals

### Primary Sources
- **LWN.net (Kernel section)** - https://lwn.net/Kernel/ - Weekly kernel development summaries, deeply technical
- **Linux Kernel Mailing List (LKML)** - https://lore.kernel.org/lkml/ - Raw patch discussions, design debates
- **Kernel Newbies** - https://kernelnewbies.org/ - Linux kernel changelogs, feature explanations
- **Linux Plumbers Conference proceedings** - https://linuxplumbersconf.org/ - Deep-dive talks on kernel subsystems

### eBPF & Tracing
- **eBPF.io** - https://ebpf.io/ - Official eBPF project, tutorials, news
- **Cilium Blog** - https://cilium.io/blog/ - eBPF in production, networking, security
- **Brendan Gregg's Blog** - https://www.brendangregg.com/blog/ - Performance analysis, BPF tools, FlameGraphs
- **Facebook/Metherlands Engineering** - https://engineering.fb.com/ - BPF at scale, kernel patches

### Scheduler & Memory Management
- **Kernel.org Scheduler docs** - https://www.kernel.org/doc/html/latest/scheduler/ - CFS, EEVDF, sched_ext
- **MM (Memory Management) subsystem docs** - https://www.kernel.org/doc/html/latest/mm/ - Page cache, reclaim, MGLRU
- **LKML "mm" and "sched" tags** - Filter LKML for memory/scheduler threads

## Storage & Filesystems

### Filesystem Development
- **Linux FS mailing lists** - https://lore.kernel.org/linux-fsdevel/ - ext4, btrfs, xfs, f2fs patches
- **Btrfs Wiki** - https://btrfs.wiki.kernel.org/ - Design docs, status pages
- **XFS Docs** - https://xfs.org/ - XFS internals, scalability
- **F2FS Papers** - Flash-Friendly File System design papers

### Storage Hardware & Controllers
- **NVMe Specification** - https://nvmexpress.org/specifications/ - Command set, features
- **SPDK (Storage Performance Development Kit)** - https://spdk.io/ - User-space NVMe, storage acceleration
- **Linux Block Layer docs** - https://www.kernel.org/doc/html/latest/block/ - request_queue, blk-mq, io_uring

## Database Internals

### PostgreSQL
- **PostgreSQL Internals** - https://www.interdb.jp/pg/ - Buffer manager, WAL, planner, executor
- **PostgreSQL Wiki** - https://wiki.postgresql.org/wiki/ - Development, internals pages
- **PGConf talks** - Conference videos on internals

### Storage Engines
- **RocksDB Wiki** - https://github.com/facebook/rocksdb/wiki - LSM trees, compaction, WAL
- **InnoDB Internals** - MySQL documentation, Percona blog
- **LMDB Design** - https://lmdb.tech/ - B+tree, MVCC, zero-copy

## Networking & Protocol Internals

### Linux Networking Stack
- **Linux Networking Documentation** - https://www.kernel.org/doc/html/latest/networking/ - netfilter, tc, XDP, AF_XDP
- **Netdev mailing list** - https://lore.kernel.org/netdev/ - Network stack patches, discussions
- **XDP/eBPF Networking** - https://xdp-project.io/ - eXpress Data Path

### Protocol Implementations
- **QUIC Working Group** - https://datatracker.ietf.org/wg/quic/ - RFC 9000, implementations
- **TCP Congestion Control** - BBR, CUBIC, Vegas kernel implementations
- **DPDK** - https://www.dpdk.org/ - Userspace packet processing

### Hardware Offload
- **Mellanox/NVIDIA Networking** - RDMA, RoCE, GPUDirect
- **Intel DPDK/FPGA** - Programmable NICs, flow steering

## Concurrency & Synchronization

### Kernel Primitives
- **RCU (Read-Copy-Update)** - https://www.kernel.org/doc/html/latest/RCU/ - internals, usage
- **lockref, seqlock, completion** - Kernel synchronization docs
- **percpu, atomics** - Per-CPU data, atomic operations

### Userspace
- **io_uring** - https://kernel.dk/io_uring.pdf - Original paper, kernel implementation
- **liburing** - https://github.com/axboe/liburing - Userspace library
- **folly, concurrency kits** - Facebook, Facebook/folly, mozilla/rr

## Real-Time & Timer Subsystems

- **PREEMPT_RT** - https://wiki.linuxfoundation.org/realtime/start - Real-time patch set
- **High-Resolution Timers** - hrtimer subsystem, tickless kernels
- **sched_ext** - https://github.com/sched-ext/scx - Extensible scheduler class

## Hardware & Architecture

### CPU & Memory
- **Intel SDM** - Software Developer Manuals - Microarchitecture, optimization
- **ARM Architecture Reference** - ARMv8/9, SVE, SME
- **RISC-V Specs** - Privileged/Unprivileged ISA, vector extension

### GPU Compute
- **CUDA Programming Guide** - NVIDIA - PTX, SASS, tensor cores
- **ROCm Documentation** - AMD - HIP, CDNA architecture
- **Vulkan Compute** - Cross-vendor compute shaders

## Research & Conference Proceedings

### Systems Conferences
- **OSDI / SOSP** - USENIX - Operating systems research
- **FAST** - USENIX - File and Storage Technologies
- **ATC** - USENIX - Annual Technical Conference
- **EuroSys** - European systems conference
- **ASPLOS** - Architectural support for programming languages and OS
- **ISCA / MICRO / HPCA** - Computer architecture

### ArXiv Categories
- **cs.OS** - Operating Systems
- **cs.DB** - Databases
- **cs.NI** - Networking and Internet Architecture
- **cs.DC** - Distributed, Parallel, and Cluster Computing
- **cs.AR** - Hardware Architecture

## Vendor Engineering Blogs (High Signal)

- **Cloudflare Blog** - https://blog.cloudflare.com/ - Kernel, eBPF, networking, QUIC
- **Dropbox Tech Blog** - https://dropbox.tech/ - Storage, kernel, performance
- **Netflix Tech Blog** - https://netflixtechblog.com/ - Linux tuning, BPF, chaos
- **Uber Engineering** - https://www.uber.com/blog/engineering/ - Storage, scheduling
- **Figma Engineering** - WebAssembly, Rust, performance
- **Discord Engineering** - Elixir, Rust, kernel tuning
- **Redpanda Data** - https://redpanda.com/blog - Kafka-compatible, Seastar, io_uring

## Newsletter Aggregators

- **Kernel Weekly** - https://kernelweekly.com/ - LWN summaries
- **Systems @ Scale** - Newsletter on distributed systems
- **The Morning Paper** - https://blog.acolyer.org/ - Academic paper summaries

---

## Maintenance Notes

- Review quarterly for dead links
- Add new sources when discovering high-signal content
- Tag sources by topic area for targeted searches
- Note access restrictions (some LWN content is subscriber-only after 2 weeks)