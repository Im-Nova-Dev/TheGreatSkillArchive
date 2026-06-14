---
name: modern-csrf-bypass-techniques
description: "Teach modern cross-site request forgery defense bypass techniques: cookie-scoped SameSite bypasses, POST-to-GET downgrades, header cloning, token stealing, mutation-based attacks, JSON-based CSRF, DOM clobbering, and detection."
---

# Modern CSRF Bypass Techniques

Use this skill to learn how modern CSRF defenses are bypassed in real engagements, beyond textbook examples. Each section covers the bypass, why it works, how to verify it safely, and defensive changes.

## Why classic CSRF is evolving
- Browsers now default to stricter cookie handling, but application-layer assumptions remain weak.
- API-style clients treat CSRF as a non-issue while browser clients remain vulnerable.
- Defense-in-depth is often missing: one broken token check still fails the app.

## Core Bypass Families
- Cookie-scoped SameSite bypass via first-party subdomain takeover, JSONP response smuggling, or URL-based cookie overwrite.
- Token stealing: client-side exposure via XSS-adjacent sinks, leaky abstractions, metadata reflection.
- Header cloning and forbidden-content-type swaps: `multipart/form-data` or `text/plain` requests sidestep strict application JSON parsing while browsers still send cookies.
- Mutation-based attacks: PUT/PATCH replacement, alternative HTTP methods, parameter pollution for token mismatch.
- CSRF + CORS misconfiguration: trusted-origin permissions with network-position reachability.
- CSRF + tabnabbing / postMessage: same-origin trust, window.opener misuse.
- CSRF via service workers: intercepting fetch to bypass custom-header token checks.

## Abstracted Attack Tree
- SameSite bypass
  - First-party subdomain control -> `document.cookie` overwrite -> SameSite cookies treated as same-site under attacker control.
  - JSONP callback response shape -> attacker-crafted JS runs in victim context and sends cookies cross-origin.
  - URL-fragment credential reflection -> `history.pushState` cookie load + postMessage exfil -> forged same-origin submit.
- Token stealing
  - Leaky abstraction: `meta[name=csrf-token]`, hidden form field, or response body reflection observable from attacker-origin fetch.
  - Cross-site script inclusion: attacker-assembled DOM in isolated browsing context exposes token through iframe clone or postMessage listener.
  - CSRF with partial DOM clobbering: attacker creates global named properties or custom elements that shadow same-origin data structures and disclose tokens.
- Content-type downgrade
  - Browser switches `Content-Type: application/xml` / `text/xml` / `multipart/form-data` automatically when `FormData` is attached; server tolerates these parsings but ignores CSRF tokens.
  - Form submissions via old-style login endpoints force token-less authorization due to bypassed JSON middleware.
- Mutation-based
  - Parameter pollution: `csrftoken=a&csrftoken=b` -> single-token lookup by server-side or framework token consumption mismatch.
  - Method override: `X-HTTP-Method-Override` to bypass strict POST CSRF enforcement.
- Service worker interception
  - SW from subdomain with fetch listener rewrites headers to inject tokens or strips `Content-Type: application/json` to bypass preflight assumptions.

## Browser Assumptions to Verify
- User is logged into the target application.
- User's browser supports and enforces SameSite cookie restrictions used by target application.
- Attacker can deliver content via HTTPS, HTTP, or file:// depending on target.
- Target application checks CSRF token synchronously and does not revalidate origin-derived data.

## Common Detection Signals
- Same-site navigation from attacker host into first party origin, then cross-origin POST/XHR within seconds.
- New cookie values under attacker-controlled subdomain coincident with token theft.
- `fetch()` with `credentials: include` toward attacker domain with non-zero body payload size from victim page.
- Cross-origin iframe creation followed by rapid `postMessage` from same frame pair.
- Service worker install activation in parent context from first-party subdomain.
- Set-cookie with same domain but from attacker origin IDN or alternate port.
- Unusual login/update POST requests using unusual content types or legacy endpoints.

## Teaching Steps
1. Reproduce with a local vulnerable app in Burp / OWASP ZAP.
2. Map defenses: SameSite, CSRF token, custom headers, CORS, Origin checks.
3. Test one bypass at a time to attribute failure cause.
4. Document required network position and browser behavior assumptions.
5. Show defensive fixes per family and generic effective controls.

## Defensive Controls Worth Teaching
- SameSite=Strict/Lax with nonce-bounded sessions and short token validity.
- Verify CSRF token state server-side on every state-changing request.
- Require `application/json` requests to use preflight-aware clients with Authorization headers rather than cookie-based auth.
- Harden CORS and Origin validation rather than relying on a single control.
- Review third-party JS, JSONP endpoints, and service worker integrations.

## Pitfalls and Limitations
- Some payloads fail outside browser contexts (fetch clients, curl).
- Browser same-site classifications depend on PSL and registrable domain boundaries.
- Defenses like token-on-header can still fail if another sink re-sends cookies silently.
