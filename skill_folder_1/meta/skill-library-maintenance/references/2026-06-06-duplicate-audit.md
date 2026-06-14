# 2026-06-06 Duplicate Audit & Cleanup

## Summary
Ran a full library audit for duplicate/near-duplicate skills. Found and resolved 5 duplicate pairs/groups.

## Duplicates Resolved

| # | Duplicate Pair | Primary Kept | Secondary Removed | Notes |
|---|----------------|--------------|-------------------|-------|
| 1 | `ambient-pressure-nickelate-superconductivity` (root) + `science/ambient-pressure-nickelate-superconductivity` | `science/ambient-pressure-nickelate-superconductivity` | Root | Category version identical + complete; root was exact duplicate |
| 2 | `arch-pacman-keyring-repair` + `arch-pacman-keyring-troubleshooting` | `arch-pacman-keyring-repair` | `arch-pacman-keyring-troubleshooting` | Repair skill already claimed "removed duplicate" but both existed; cleaned self-referential description |
| 3 | `go-cli-development` (root) + `university-cs/go-cli-development` | `go-cli-development` (recreated with full content) | `university-cs/go-cli-development` | Root had comprehensive content; university-cs was skeleton. Had to delete + recreate to clear collision |
| 4 | `ion-trap-quantum-computing` (root) + `physics/ion-trap-quantum-computing` | Root `ion-trap-quantum-computing` | `physics/ion-trap-quantum-computing` | Root had more detail (teaching exercises, DOE 2026 milestone, cryo-ASIC pitfalls) |
| 5 | `muon-g-2-and-anomalous-magnetic-moment-precision-physics` (physics/) + `physics-and-science-teaching/` | `physics-and-science-teaching/muon-g-2-and-anomalous-magnetic-moment-precision-physics` | `physics/muon-g-2-and-anomalous-magnetic-moment-precision-physics` | Teaching version had pedagogical modules, exercises, evaluation checklist |

## Patterns Discovered

### Pattern: Root vs Category content asymmetry
- Sometimes root has MORE content than category (go-cli-development, ion-trap-quantum-computing)
- Sometimes category has more (ambient-pressure-nickelate-superconductivity, muon-g-2)
- **Rule**: Always diff both before deciding; don't assume category is primary by default

### Pattern: Self-referential "already removed" descriptions
- `arch-pacman-keyring-repair` claimed it had removed the duplicate but both existed
- After deleting the actual duplicate, the description became inaccurate
- **Action**: Clean up descriptions after duplicate resolution

### Pattern: `absorbed_into` requires target to exist
- `skill_manage(action='delete', absorbed_into='...')` fails if target skill doesn't exist
- Must ensure primary skill exists before deleting secondary with absorption declaration
- Workaround: delete without `absorbed_into` if primary already exists, or create primary first

### Pattern: Three-way collision resolution
- `go-cli-development` existed at root AND in university-cs, then I recreated at root
- Had to: delete university-cs → delete root → recreate root with full content
- **Lesson**: Check for ALL locations before creating

### Pattern: Skill collision error is ambiguous
- "Ambiguous skill name: 2 skills match..." doesn't tell you the full paths
- Must use `skill_view` with path to disambiguate
- **Tool tip**: `skill_view` on bare name with collision tells you the matching paths

## Verification Steps Applied
1. `skill_view` both candidates to compare content
2. Diff content mentally/manually for unique sections
3. Keep stronger/more complete version
4. Delete weaker with `skill_manage(action='delete')`
5. Clean up description of kept skill if it referenced the deleted one
6. Verify no more collisions with bare name lookup

## Files Modified
- Deleted 5 skill directories
- Patched 1 skill description (`arch-pacman-keyring-repair`)
- Recreated 1 skill (`go-cli-development` with full content)

## Remaining Complementary Skills (Not Duplicates)
- `arch-interrupted-upgrade-recovery`, `linux-arch-omarchy-boot-recovery`, `linux-arch-hyprland-startup-recovery`, `arch-troubleshooting` — different failure modes
- `linux/hyprland-logging-and-evidence`, `linux/omarchy-hyperland-post-update-fix` — complementary diagnostics
- `iouring-bpf-filter-internals` + `io_uring-bpf-filter-internals` — cBPF filter vs BPF event-loop (different focus)