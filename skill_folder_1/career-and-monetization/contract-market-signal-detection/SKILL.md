---
name: contract-market-signal-detection
description: Detect, validate, and act on career and monetization market signals for technical professionals. Use when scanning for freelance niches, contract rate shifts, AI automation impacts, hiring trend changes, open-source income, platform shifts, or side-project monetization patterns.
---

# Contract Market Signal Detection

## Purpose
Provide a repeatable process for identifying high-quality career/monetization intelligence for technical professionals, with emphasis on concrete signals, numbers, and evidence over generic advice.

---

## 1. Signal Sources

### Primary Sources
- **Contract/freelance platforms**: Upwork, Toptal, Arc, Gun.io, Lemon.io (rate data, category growth/decline)
- **Job market data**: LinkedIn Talent Insights, HeroHunt.io, PwC AI surveys, BLS/OES wage data, Levels.fyi
- **Blockchain/crypto bounty platforms**: Algora, Gitcoin, Immunefi, HackerOne, Bugcrowd
- **Open-source sponsorship**: GitHub Sponsors, Open Collective, Patreon for devs, Polar.sh, grants from NLNet, Ford Foundation, Chan Zuckerberg Initiative
- **Tech layoff/hire trackers**: Layoffs.fyi, Initialize.io, Blind, Blind hiring threads
- **AI automation reports**: McKinsey, PwC, Accenture, Upwork "AI Impact" reports, O*NET automation risk data
- **SaaS side-project evidence**: Indie Hackers, MicroConf, SaaS掌舵人 (SaaS communities), AppSumo marketplace trends

### Secondary Signals
- HackerNews "Who is hiring" monthly threads (compensation bands, remote ratio)
- Substack authors in AI+software niche publishing rate data
- Reddit r/forhire, r/freelance, r/selfhosted "I made $X" posts
- Twitter/X tech founders posting rate cards or RFP shout-outs
- Product Hunt launch revenue signals

---

## 2. Evidence Quality Framework

**Tier 1 (act on immediately)**: Current quarter data from >500 transactions, named companies, exact rates, methodology disclosed.
**Tier 2 (track closely)**: Survey data from reputable institution (PwC, McKinsey, Stanford HAI) with sample size >1,000 and year-over-year comparison.
**Tier 3 (context only)**: Anecdotal, <100 data points, or self-reported without verification.

**Rule**: Only store Tier 1/2 data as intel. Suppress Tier 3 unless it reveals a structural shift tracked across multiple independent sources.

---

## 3. Classification Framework

Label every signal with:

```
TYPE: [contract-rate-change|freelance-niche|ai-automation-risk|hiring-surge|hiring-decline|open-source-bounty|sponsorship|platform-shift|side-project-monetization|interview-pattern]
EVIDENCE_TIER: [1|2|3]
WINDOW: [current quarter|6-month trailing|12-month trailing|one-time event]
DIRECTION: [rising|falling|stable|volatile|fragmented]
NU_MRT: [yes|no]  # Named rates/numbers present
COMPANIES: [count or list]
RATE_USD: [specific number or range if present]
SKILLS_DEMANDED: [comma-separated list]
ACTION: [upskill|pivot|raise-rates|expand-services|protect-income|monitor-only|pursue-bounty|sponsor-outreach]
CONFIDENCE: [high|medium|low]
SOURCE_URL: [URL]
```

---

## 4. Validation Checklist

Before storing intel, verify:
- [ ] Contains at least one named number (rate, percentage, transaction count, company count)
- [ ] Source is identifiable and verifiable
- [ ] Trend is either structural (not one vendor's pricing change) OR explicitly flagged as vendor-specific
- [ ] Time window is clear (not "recent" — specify dates or quarters)
- [ ] Action taken is proportionate to evidence quality

---

## 5. Action Mapping by Signal Type

### Contract Rate Changes
- **Rising rates + rising demand**: Raise retainer floor by 10–25%; add named companies to outreach list.
- **Rising rates + declining demand**: Rates likely feast/famine. Shift to productized services or retainers.
- **Falling rates + rising demand**: Race to the bottom; specialize immediately or pivot to higher-tier niche.
- **Falling rates + falling demand**: Abandon niche or add premium layer.

### AI Automation Risk
- **Specific task automatable**: Repackage as AI-augmented service or move to implementation/strategy layer.
- **Full role displacement risk within 2 years**: Start transition now; add AI-native skills to stack.

### Hiring Surges
- **Specific company/role surge**: Update LinkedIn, prepare targeted portfolio case studies, reach out to hiring managers directly.
- **Sector-wide surge**: Create sector-specific content/case studies; become discoverable via community answers.

### Open-Source Bounty/Sponsorship
- **Named bounty with amount**: Evaluate effort vs. bounty, check bounty history, consider long-term maintainer relationship.
- **Sponsorship program**: Apply with active usage metrics, maintain consistent contribution rhythm.

### Platform Shift
- **Major platform V2 launch or policy change**: Audit current portfolio/presence on affected platform; migrate or expand accordingly.

### Side-Project Monetization
- **Concrete MRR numbers + churn data from similar devs**: Build comparable MVP; validate within 4 weeks.

---

## 6. Anti-Patterns to Reject

- "AI is taking all jobs" without specific role/rate/timeframe
- Generic "learn to code" or "upskill in AI" without evidence of premium magnitude
- Unverified "I made $10K/month" anecdotes without comparable cohort data
- Outdated data (>18 months) presented as current
- Confusing correlation with causation (e.g., "AI hiring up" without decomposing which *roles* are up vs. down)

---

## 7. Storage and Retrieval

- **Intel store**: `/home/nova/.hermes/intel/career/YYYY-MM-DD-<slug>.md`
- **Format**: Use classification fields as YAML frontmatter; body contains structured evidence.
- **Skill updates**: After each signal capture, update `contract-market-signal-detection` action mapping if new pattern category is observed.
- **Review cadence**: Monthly intel review to update confidence ratings and consolidate trends.

---

## 8. Example Intel Entry

See `/home/nova/.hermes/intel/career/` for current entries formatted per this schema.
