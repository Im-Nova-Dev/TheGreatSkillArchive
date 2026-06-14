---
name: windows-ntquerysysteminformation-class-abuse
description: Teach Windows kernel exploitation via NtQuerySystemInformation information-class handling, focusing on class 253 CVE-2026-40369 and related queryinfo-driven memory corruption primitives.
---

# Windows NtQuerySystemInformation Class Abuse

## 1) Concept

`NtQuerySystemInformation` is a general-purpose syscall for querying kernel-managed system state. Each information class selects a different kernel data structure and serialization routine. Microsoft’s implementation mixes user-mode argument validation, probe behavior, and copy-back semantics across dozens of classes.

The offensive principle is:
- Identify an information class whose copy-back path accepts a buffer/size pair where the validation can be weakened by trivially crafted inputs.
- Force the kernel to treat a user-controlled pointer as a kernel write destination even when the call indicates an undersized buffer.
- Convert that write into a privilege escalation or sandbox escape primitive.

## 2) Canonical Example: CVE-2026-40369

Target: `SystemProcessInformationExtension` (information class 253)
Routine: `nt!ExpGetProcessInformation`
Root cause: Untrusted pointer dereference via zero-length output buffer
Primitive: Deterministic kernel address increment at attacker-controlled address plus fixed offsets

Write primitive:
- `addr+0` += process count
- `addr+4` += thread count
- `addr+8` += handle count

Exploitation pattern:
1. Leak or calculate a reliable kernel target address (e.g., via a confusion primitive with another information class).
2. Invoke class 253 with a zero-length buffer and the target address in the output buffer pointer.
3. Use the increment primitive to corrupt token privilege fields, `EPROCESS` fields, or other security-critical kernel objects.
4. Re-trigger or chain to achieve SYSTEM or sandbox escape.

## 3) Teaching Objective

Students should learn:
- How to enumerate information classes from kernel metadata, headers, and ReactOS/WinBFR sources.
- What probe semantics Windows applies and how zero-length or misaligned length arguments change behavior.
- How to build a minimal crash reproducer before building an exploit primitive.
- How to derive kernel addresses from confusion/data leaks when KASLR is enabled.
- How to chain token manipulation into privilege escalation or browser sandbox escape.
- How to instrument syscall behavior for detection and defense.

## 4) Step-by-Step Lab Exercises

### Exercise A — Syscall Reconnaissance
1. Enumerate documented and undocumented `System*Information` classes.
2. Map classes to routines using kernel symbols or ReactOS sources.
3. Identify classes whose copy-back paths use `ProbeForWrite` followed by write loops.

### Exercise B — Minimal Crash PoC
1. Write a small C/C++ program that dynamically resolves `NtQuerySystemInformation` from `ntdll.dll`.
2. Call with class 253 and a zero-length buffer while pointing the output buffer at a known kernel address.
3. Observe bugcheck/crash behavior and validate reproducibility.
4. Use a VM with kernel debugging enabled to validate the crash path and confirm write size.

### Exercise C — Primitive Characterization
1. With a controlled kernel address, record the exact increments after each syscall.
2. Repeat across system load states to quantify variability.
3. Determine whether the primitive can overwrite adjacent fields deterministically enough for exploitation.

### Exercise D — Address Derivation
1. Use another information class or kernel object leak to derive `ntoskrnl.exe` base.
2. Use that base to compute target RVA/offsets for `EPROCESS` and token fields.
3. Translate offsets into an absolute candidate target address.

### Exercise E — Token Manipulation Chain
1. Locate the current process `EPROCESS`.
2. Read the process token and mask `EX_FAST_REF`.
3. Apply the increment primitive at token offsets that enlarge or enable privileges.
4. Spawn a privileged child process to verify elevation.

### Exercise F — Detection and Hardening Thought Experiment
1. Design ETW/syscall monitor rules to detect class 253 zero-length calls.
2. Add memory-integrity or CFG-related heuristics that would raise alert.
3. Discuss kernel mitigations that could break or harden this class of bug.

## 5) Pitfalls and Anti-Patterns

- Assuming all information classes behave identically: validation rules vary widely.
- Ignoring KASLR/CFG: address derivation failure often breaks the chain.
- Treating BSOD as harmless: reliability requires controlled target selection or pre-validation.
- Forgetting user-mode pointer expectations: many classes require aligned or initialized structures beyond buffer/size.
- Missing sandbox restrictions: renderer sandbox may restrict syscalls via brokering or policy.

## 6) Defensive Recommendations

- Patch affected Windows builds promptly.
- Monitor for anomalous `NtQuerySystemInformation` usage with class 253 and zero-length buffer patterns.
- Enable browser sandbox hardening to reduce reachability even if LPE exists.
- Consider Integrity Control / ACG improvements that limit post-exploitation.
