---
name: vercel-oss-bounty-entry-2026
description: Use when a technical professional wants to enter, prepare for, or monetize the Vercel Open Source Bug Bounty Program launched February 2026 on HackerOne. Provides exact scope, target surfaces, workflow, cost-adjusted effective rates, and retainer conversion steps.
---

# Vercel OSS Bug Bounty Entry — 2026

## Purpose
Convert the new public Vercel OSS Bug Bounty program into a concrete income stream, lead-gen channel, or premium positioning playbook.

## When to Use
- You know JavaScript/TypeScript, React, Vue, Svelte, build tooling, or AI SDK surfaces.
- You want short-cycle, payout-based work alongside broader OSS or contract revenue.
- You are targeting high-impact CVEs/public CVEs that prove domain expertise.

---

## 1. Opportunity Summary

| Fact | Value |
|------|-------|
| Program | Vercel Open Source |
| Hosted on | HackerOne |
| Public launch | February 3, 2026 |
| Goal | Crowdsource vulnerability discovery across Vercel OSS |
| Reference payout | Prior WAF/React2Shell program paid **>$1M** across dozens of researchers |

This is not a low-volume maintenance charity: the prior program produced multiple findings with coordinated disclosure + CVE publication.

---

## 2. Prioritized Attack Surface

Focus on these in-scope projects. They are ordered by deployment frequency and impact radius:

1. **Next.js** — React framework for production web applications
2. **AI SDK** — TypeScript AI app toolkit
3. **Nuxt** — Vue.js framework
4. **Svelte** — UI framework
5. **Turborepo** — High-performance monorepo build system
6. **SWR** — React Hooks data fetching
7. **vercel (CLI)** — Command-line interface
8. **workflow** — Durable workflow execution engine
9. **flags** — Feature flags SDK
10. **nitro** — Universal server engine
11. Smaller util libs — `ms`, `async-sema`, `skills` (lower volume; lower payout expectation)

---

## 3. Effective Rate / Time Model

| Scenario | Assumed Time | Expected Payout | Effective Rate |
|----------|--------------|-----------------|----------------|
| Low-to-mid tier | 8 hours | $1,000–$3,000 | $125–$375/hr |
| High-impact OSS | 16 hours | $3,000–$10,000 | $187–$625/hr |
| Multi-affected CVE | 24+ hours | $10,000–$30,000+ | $416–$1,250+/hr |

Do not anchor to Opire's general $30–$2,780 ceiling. Infra tier bounties (Next.js, AI SDK, Nitro) have materially higher implied caps. Use the $1M payout history as a calibrated ceiling expectation, not an average.

---

## 4. Practical Entry Workflow

1. **Read the policy**
   - https://hackerone.com/vercel-open-source
   - Note in-scope assets, out-of-scope boundaries, response SLA, responsible-disclosure expectations.
2. **Select one target surface**
   - Prefer AI SDK or Next.js: highest commercial exposure and employer-citeable CVEs.
3. **Clone + instrument**
   - Build the project; enable verbose logging; trace auth, routing, injection points, cache boundaries, SSR hydration, middleware, and build pipeline.
4. **Reproduce with minimum steps**
   - Write step-by-step reproduction; keep runtime config minimal.
5. **Report with impact statement**
   - Include: affected versions, business impact, disclosure timeline.
6. **Track payout + CV citation**
   - Public CVE + bounty ≠ one-time payment. It is structural qualification evidence.

---

## 5. Retainer Conversion (High-Leverage Play)

Vercel's OSS is dependency-heavy across enterprise. Each bounty submission is lead-gen.

- After disclosure, extract reporter contact on approved companies using the affected repo as prod dependency.
- Offer: remediation + architecture review + pre-commit rollout plan.
- Anchor: $150–$350/hr for emergency review; $3,000–$12,000 fixed-fee for hardening sprint.

---

## 6. Adjacent Monetization: Vercel OSS Program (Cohort-Based)

**Spring 2026 cohort applications open until June 3, 2026** — https://open-source-program.vercel.app/

| Benefit | Details |
|---------|---------|
| Platform Credits | **$3,600** over 12 months |
| OSS Starter Pack | Third-party service credits (oss-starter-pack.vercel.com) |
| Community Support | Priority guidance from Vercel team |

**Eligibility (ALL required):**
- ✅ Active open source project — actively developed and maintained
- ✅ Hosted on (or intended for) Vercel
- ✅ Measurable impact or growth potential
- ✅ Code of Conduct defining community standards
- ✅ Credits used exclusively for open source work and the project itself

**Winter 2026 cohort (35 projects)** includes: PyTorch, nivo, PixiJS, KDE Connect, KDE/kdeconnect-kde, Element Plus, LobeChat, Valibot, Analog, NativeWind, Electerm, Memos, Milkdown, jsPDF.

**Play:** If you maintain a qualifying project (framework, tooling, AI/ML lib), apply. The $3,600 credits + starter pack reduce infra burn while you build portfolio. Bounty findings on Vercel projects + OSS Program acceptance = compounding credibility signal.

---

## 7. Ecosystem-Wide Signal: $12.5M Alpha-Omega / OpenSSF Grants (March 2026)

**Funders:** Anthropic, AWS, GitHub, Google, Google DeepMind, Microsoft, OpenAI
**Focus:** Maintainer-centric AI security assistance — tooling for triaging AI-generated vulnerability reports
**Signal:** Major tech companies funding OSS maintainer tooling directly

**Opportunity:** Projects building AI-assisted security tooling for maintainers are getting funded. If your bounty work reveals gaps in automated triage/remediation workflows, that's a fundable product direction.

---

## 8. Market Context: AI Premium Anchors Bounty Value

Per HeroHunt.ai (Mar 2026) and Arc.dev (May 2026):
- **AI/ML Engineering freelance rates: $110–190/hr** (senior)
- **AI Infrastructure/MLOps: $120–200/hr**
- **Vercel AI SDK** is a Tier-1 project — vulnerabilities here map directly to the highest-paying specialization
- **Next.js + AI SDK chain findings** = citeable evidence for AI implementation contract premiums

---

## 9. Decision Tree

```
Need quick cash / portfolio win?
  → Pick Next.js or AI SDK
  → Focus auth/routing/cache/SSR vulnerabilities
  → Accept 8–16 hour hunt window

Want premium contracting evidence?
  → Pick multi-surface chain (e.g., Next.js + AI SDK + workflow)
  → Prioritize unique, reproducible findings
  → Convert disclosure into retainer outreach

Have qualifying OSS project?
  → Apply to Vercel OSS Program (deadline June 3, 2026)
  → Stack: bounty CVEs + program acceptance = compounding signal
  → Use credits to fund infra for deeper research
```

---

## Outcome Targets
- **First 30 days:** 1 submission accepted; 1 retainer outreach sent.
- **90 days:** ≥1 bounty accepted + ≥1 short remediation retainer or upgrade offer.
- **12 months:** Public CVE evidence used to justify elevated contract rates for Next.js/Nitro/AI SDK work; OSS Program membership (if eligible) providing ongoing infra credits and visibility.
