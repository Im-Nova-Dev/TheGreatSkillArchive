---
name: defender-edr-toctou-junction-abuse
description: Teach TOCTOU-based EDR/Defender privilege escalation via opportunistic locks and NTFS junctions. Use when analyzing or demonstrating Windows remediation-engine flaws, building red-team tooling for SYSTEM write primitive abuse, or training on CVE-2026-33825 / BlueHammer / RedSun-family primitives.
---

# Teaching: EDR/Defender TOCTOU and Junction Op-Lock Abuse

This skill covers offensive security education on leveraging TOCTOU race conditions in Windows Defender/EDR remediation paths to escalate privileges and bypass security product trust boundaries.

## Learning Objectives
- Understand how EDR remediation flows operate under elevated privileges.
- Recognize how opportunistic locks and NTFS junctions create path-validation gaps.
- Build or analyze PoC flows that turn detection-triggered cleanup into SYSTEM code execution.
- Identify detection and mitigation strategies for defenders.

## Prerequisites
- Windows internals: EDR/AMSI architecture, SYSTEM vs user privilege contexts, opportunistic lock semantics.
- Familiarity with Windows I/O, reparse points, NTFS junctions, oplock testing tools (e.g. `Filesystem Filter` analysis or custom harnesses).
- Basic C/Rust/Python development for race harness construction.

## Core Concepts

1. EDR Remediation Trust Boundary
Windows Defender removes or quarantines detected files using a privileged anti-malware service. If the file path used during cleanup is attacker-controlled at the critical write step, the cleanup becomes a write primitive with SYSTEM privileges.

2. Race Building Pattern
- Trigger detection of attacker-placed content.
- Initiate remediation; observe privileged handle creation path.
- Use batch oplock to pause at intermediate state.
- Replace original target with NTFS junction pointing to attacker-controlled file in System32 or another sensitive location.
- Release oplock; wait for privileged write.
- Result: attacker-controlled binary is written as SYSTEM.

3. Alternate Cloud-Tagged Rollback Path
Some threat remediation paths additionally use Windows Cloud Files API placeholders and rollback logic. Even when the primary path is fixed, secondary rollback code paths may still trust path identity, enabling post-patch exploitation (e.g., RedSun post-CVE-2026-33825).

## Teaching Exercises
1. Static Code Review Exercise
- Audit an EDR agent's file-write or quarantine code for missing repeat `GetFinalPathNameByHandle` / reparse-point resolution at the time of write.
- Identify handles opened with `FILE_FLAG_OPEN_REPARSE_POINT` vs strict resolution.

2. Differential Testing Exercise
- Create a benign trigger file in a temp directory.
- Use an oplock harness to pause a simulated remediation flow and swap junctions mid-race.
- Validate whether the privileged write lands in System32 instead of the temp directory.

3. Detection Engineering Exercise
- Draft Splunk/Sigma rules for EDR remediation anomaly:
  - EDR child process creating junctions outside `%TEMP%`.
  - Elevated service writing to unexpected file paths after a detected malicious file.
  - Image load from System32 after suspicious oplock-related I/O patterns.

4. Patch Validation Exercise
- Given a patch description that adds path revalidation, identify if rollback or alternate path handling still contains the same bug class.
- Propose defense-in-depth improvements.

## Mapping to CVE-2026-33825 / BlueHammer / RedSun
- BlueHammer: primary repair flow TOCTOU via opportunistic lock + NTFS junction.
- RedSun: secondary cloud-tagged rollback TOCTOU retaining effective exploitability after primary patch.
- Defensive lesson: remediation engines must resolve full paths inside a single kernel transaction tied to the privileged handle, not trust cached user-space path strings across async rollback flows.

## Parallel Plateau Cases to Study
- Dirty Frag / CopyFail2 (CVE-2026-43284): page-cache write primitive chains versus kernel path-validation weaknesses.
- Dirty Pipe (CVE-2022-0847): unprivileged pipe page-cache overwrite and the mitigation lineage.
- Windows ALPC exploitation: IOCTL dispatcher trust boundary abuse across handle duplication.

## Detection Difficulty Calibration
- Low: junction creation in temp paths, repeated remediation failures.
- Medium-hish: timing correlation between file modification and privileged write.
- High: cloud-tagged rollback flows where cloud placeholder filesystem events are not correlated with local write attempts.
