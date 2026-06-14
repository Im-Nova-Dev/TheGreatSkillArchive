---
name: access-control-bypass-techniques
description: Teach modern access-control bypass patterns, focusing on client-side trust issues, role tampering, higher-order API abuse, and server-side verification failures observed in red team engagements and CVE research.
---

# Access Control Bypass Techniques

## Core Concept
Many trust-boundary failures happen because the server trusts client-supplied authorization metadata instead of recalculating roles from authenticated identity and backend policies.

## Common Bypass Categories

1. **Client-Supplied Roles / Claims Tampering**
   - Vulnerable pattern: API or session response includes roles/claims/authorities that clients can intercept and modify.
   - Example: CVE-2025-43712 (JHipster before 8.9.0), where modifying the `authorities` array in the login response from `ROLE_USER` to `ROLE_ADMIN` bypassed all backend role enforcement.

2. **Vertical Escalation via Higher-Order / Alternate Endpoints**
   - Calling an endpoint meant for lower-privilege users with an alternate entity identifier.
   - Typical with missing authorization on `by-id` lookups, GraphQL batching, or REST `?id=` parameters.

3. **Horizontal Escalation via Insecure Direct Object Reference (IDOR)**
   - Object ownership checks missing; attackers access other tenants' records by changing IDs or keys.

4. **Endpoint Parameter Smuggling**
   - Accepting deprecated/alternate parameter names or multiple representations of the same field with inconsistent enforcement.

5. **State Confusion in CAS / OAuth / JWT**
   - OAuth `iss/sub` mismatch, audience drift, token replay, or using untrusted signature algorithms (`alg=none`).

## Detection and Mitigation
- Always derive roles on the server from the user identity and a canonical role store; never accept client-provided arrays as definitive.
- Enforce per-request authorization on API routes, not just UI route guards.
- Prefer opaque session identifiers; avoid storing mutable trusted claims in JWT unless properly signed and validated.
- Add unit/CI tests for role escalation paths and CI checks for role policy consistency.
- Log effective user context server-side; detect role transitions that cannot be traced to an authorized role assignment workflow.