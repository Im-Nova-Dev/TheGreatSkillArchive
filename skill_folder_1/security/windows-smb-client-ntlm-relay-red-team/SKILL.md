---
name: windows-smb-client-ntlm-relay-red-team
description: >
  Teach Windows SMB client red-team exploitation including NTLM reflection, coercion-based relay, and privilege escalation chains.
  Covers CVE-2025-33073, intercepting/relaying SMB authentication, coerced authentication via MS-RPC/SMB tools,
  detection strategies, and lab/CTF-style exercises.
tags: [security, windows, smb, ntlm-relay, red-team, privilege-escalation]
---

# Windows SMB Client & NTLM Relay Red Team Tradecraft

## When to use
Use when teaching offensive techniques against Windows domain environments, preparing for red team engagements, or building detection playbooks for SMB client abuse.

## Learning objectives
- Understand why SMB client-side bugs like CVE-2025-33073 are high impact
- Learn NTLM reflection and relay mechanics over SMB/RPC
- Build coercible authentication chains to privileged identities
- Apply detection and mitigation controls from a blue-team perspective

## Prerequisites
- Windows domain lab with Domain Controller and member hosts
- Familiarity with Responder, ntlmrelayx, Impacket, and Rubeus
- Understanding of NTLM, Kerberos, SMB signing, and SID filtering

---

## 1. Core concepts

### SMB client attack surface
- SMB client initiates connections; bugs in client validation/redirect handling let attackers provoke unintended authentication flows.
- CVE-2025-33073: improper access control in SMB client processing allows remote attackers to coerce privileged authentication and reflect credentials.

### NTLM reflection vs relay
- **Reflection**: attacker captures NTLM challenge from victim A and replays it back to A, causing A to authenticate to itself.
- **Relay**: attacker forwards authentication credentials from victim A to target B in real time.

### Coerced authentication
- Force a high-value machine or service to initiate outbound authentication to attacker-controlled receiver.
- Common methods: MS-RPC coercion (MS-EFSRPC, MS-FSRVP), mailbox/print spooler coercion, HTTP-to-SMB file fetching.

---

## 2. Attack chain walkthrough

### Simplified CVE-2025-33073 style chain
1. **Authenticated foothold**: Attacker has domain user credentials or a low-privilege session.
2. **Coercion**: Attacker coerces a privileged service or member machine to initiate SMB/RPC authentication to attacker.
3. **Relay/Reflection**: Using the SMB client access-control flaw, attacker reuses or redirects authentication so SYSTEM or privileged account credentials are passed to attacker-controlled endpoint.
4. **Privilege escalation**: Attacker now possesses privileged credentials/tokens or can replay to member host for SYSTEM access.
5. **Lateral movement / domain impact**: With SYSTEM/privileged access, attacker can export secrets, pivot to DC, or perform pass-the-hash/ticket.

### Tool-driven workflow
- `Responder` / `ntlmrelayx.py` for NTLM capture and relay
- `Rubeus` for Kerberos+SMB interaction, coercing authentication
- `Impacket` for RPC/SMB session handling
- `LDAPfragger` or custom SMB responder to trigger SMB filename coercion

---

## 3. Lab exercise concepts

### Exercise A: SMB client coercion relay
1. Setup: Domain member host, attacker machine with ntlmrelayx configured against a high-value server.
2. Trigger: use an `MS-RPC` coercion helper to force member host to authenticate.
3. Capture/relay ntlm session into privileged session.
4. Validate: open elevated session and execute controlled command.

### Exercise B: Detection validation
1. Emit the attack in a monitored lab environment with Sysmon + EDR.
2. Document events that indicate coercion/relay: unexpected outbound SMB on member hosts, unusual RPC connection patterns, repeated NTLM Type1/Type3.
3. Create detection rule snippets and tune false positives.

---

## 4. Detection & hardening

### Indicators
- SMB client connections to non-standard SMB ports/hosts
- Unusual NTLM SSO / challenge patterns
- RPC bind requests followed by SMB inbound authentication
- Abnormal process trees: `svchost.exe`, `lsass.exe` spawning unexpected network connections

### Mitigations
- Enforce SMB signing and disable SMBv1
- Disable NTLM where possible; require Kerberos with AES
- Implement SMB client firewall restrictions on member hosts
- Use admin approval/workstation restriction for high-value accounts
- Harden against coercion: apply updates, restrict MS-RPC interfaces, disable print spooler/bits if unused

---

## 5. References & further reading
- https://nvd.nist.gov/vuln/detail/CVE-2025-33073
- https://attackerkb.com/topics/IGyaSbSz1Z/cve-2025-33073
- https://www.praetorian.com/blog/cve-2025-33073-ntlm-reflection-one-hop/
- https://op-c.net/blog/cve-2025-33073-windows-smb-client-improper-access-control-cisa-kev/
- https://github.com/fortra/impacket
- https://github.com/GhostPack/Rubeus

---

## 6. Classroom / CTF tips
- Combine with Kerberoasting and credential dumping exercises for full chain impact.
- Include defensive debriefs: produce detection rules, hunting queries, and incident response steps.
- Vary difficulty: allow NTLM relay to LDAP vs SMB vs HTTP to show different post-exploitation outcomes.
