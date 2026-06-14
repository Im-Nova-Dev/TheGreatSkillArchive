---
name: research-methods
description: "Research toolbox: arXiv (paper search/fetch), LLM Wiki (structured knowledge base), Research Paper Writing (NeurIPS/ICML/ICLR pipeline), Smart Home Research (device taxonomy, market recon). Use for any academic/technical research workflow — paper discovery, literature review, knowledge management, writing, domain-specific recon."
version: 1.0.0
category: research
tags: [research, arxiv, wiki, paper-writing, literature-review, smart-home, taxonomy, knowledge-base]
---

# Research Methods

Unified class-level skill covering academic and technical research workflows. Replaces 4 narrow skills: `arxiv`, `llm-wiki`, `research-paper-writing`, `smart-home-research`.

## When to Use

- Discovering and fetching papers from arXiv (search, download, metadata)
- Building and querying structured LLM knowledge bases (wiki)
- End-to-end research paper pipeline: design → experiments → writing → submission
- Domain-specific research: smart home device taxonomy, market reconnaissance, product surveys

---

## Decision Guide

| Task | Sub-Tool |
|------|----------|
| Search/fetch arXiv papers, metadata, PDFs | **arXiv** |
| Create/query structured knowledge wiki | **LLM Wiki** |
| Write ML paper for NeurIPS/ICML/ICLR | **Research Paper Writing** |
| Smart home product/brand/protocol research | **Smart Home Research** |

---

## 1. arXiv (Paper Search & Fetch)

### Capabilities

- Search arXiv by query, author, category, date range
- Fetch paper metadata (title, authors, abstract, categories, DOI, journal ref)
- Download PDFs
- Batch operations for literature reviews

### Usage

```bash
# Search (via web_search or arxiv CLI if available)
web_search(query="attention mechanism site:arxiv.org", limit=10)

# Fetch paper details
web_extract(urls=["https://arxiv.org/abs/1706.03762"])

# Download PDF
web_extract(urls=["https://arxiv.org/pdf/1706.03762.pdf"])
```

### Key References (in `references/arxiv/`)

- Search syntax and operators
- Category taxonomy (cs.LG, cs.CL, cs.CV, stat.ML, etc.)
- Batch download patterns
- Citation extraction

### Teaching Approach

- Search for papers on a topic
- Fetch and organize 5-10 papers
- Extract key metadata for literature review

---

## 2. LLM Wiki (Structured Knowledge Base)

### Overview

A three-layer wiki system for building structured, queryable knowledge bases optimized for LLM consumption and updates.

**Layers:**
1. **Entities** — People, organizations, papers, models, datasets
2. **Concepts** — Methods, techniques, theories, frameworks
3. **Comparisons** — Side-by-side analyses, trade-offs, benchmarks

### When to Use

- Building a persistent knowledge base for a research domain
- Need structured, queryable notes that LLMs can read/update
- Tracking entities, concepts, and comparisons over time
- Resuming research across sessions

### Architecture

```
wiki/
├── entities/
│   ├── people/
│   ├── organizations/
│   ├── papers/
│   ├── models/
│   └── datasets/
├── concepts/
│   ├── methods/
│   ├── techniques/
│   └── frameworks/
├── comparisons/
│   ├── model-comparisons/
│   ├── benchmark-results/
│   └── tradeoff-analyses/
└── metadata/
    ├── tag-taxonomy.md
    ├── frontmatter.md
    └── update-policy.md
```

### Core Operations

| Operation | Description |
|-----------|-------------|
| **Initialize** | Create wiki structure, set domain, configure frontmatter |
| **Resume** | **CRITICAL** — do every session: load existing wiki state |
| **Entity pages** | Create/update person, org, paper, model, dataset entries |
| **Concept pages** | Document methods, techniques, frameworks |
| **Comparison pages** | Side-by-side analyses with trade-offs |
| **Queries** | Search across layers, filter by tags/entities |
| **Update policy** | Rules for when/how to update existing entries |

### Key References (in `references/llm-wiki/`)

- `when-this-skill-activates.md`, `wiki-location.md`
- `architecture-three-layers.md`
- `resuming-an-existing-wiki.md` (CRITICAL)
- `initializing-a-new-wiki.md`
- `domain.md`, `conventions.md`, `frontmatter.md`
- `tag-taxonomy.md`, `page-thresholds.md`
- `entity-pages.md`, `concept-pages.md`, `comparison-pages.md`
- `update-policy.md`, `core-operations.md`, `working-with-the-wiki.md`
- `pitfalls.md`, `related-tools.md`

### Critical: Resume Every Session

```bash
# Before any wiki work, ALWAYS resume:
# 1. Load wiki location
# 2. Read recent changes
# 3. Check update policy
# 4. Continue from last state
```

### Frontmatter Schema

```yaml
---
title: "Entity/Concept Name"
type: entity | concept | comparison
subtype: person | organization | paper | model | dataset | method | technique | framework | comparison
tags: [tag1, tag2]
aliases: ["alternative name"]
related: [wiki/path/to/related.md]
sources: [{"type": "arxiv", "id": "1706.03762"}, ...]
last_updated: "2026-06-11"
---
```

### Pitfalls

- Not resuming wiki at session start
- Creating duplicate entity pages (check `related` and search first)
- Inconsistent tagging (follow `tag-taxonomy.md`)
- Skipping `sources` field — critical for verification
- Updating without checking `update-policy.md`

---

## 3. Research Paper Writing (NeurIPS/ICML/ICLR Pipeline)

### Overview

End-to-end pipeline for publication-ready ML/AI research papers.

### Pipeline Stages

| Stage | Reference | Output |
|-------|-----------|--------|
| **Setup** | `project-setup.md` | Git discipline, recruitment, repo structure |
| **Literature Review** | `literature-review.md` | Search, citation verification, BibTeX |
| **Experiment Design** | `experiment-design.md` | Hypotheses, baselines, metrics, ablation plan |
| **Experiment Execution** | `experiment-execution.md` | Running, monitoring, failure recovery |
| **Result Analysis** | `result-analysis.md` | Statistical analysis, negative results, story ID |
| **Writing** | `writing-and-formatting.md` | Sections, style, figures, tables |
| **Review & Revision** | `review-and-revision.md` | Review simulation, rebuttal, claim verification |
| **Submission** | `submission.md` | Validation, arXiv, code packaging |
| **Post-Acceptance** | `post-acceptance.md` | Posters, talks, social impact, code release |

### Specialized Paper Types

- Theory papers: `paper-types.md`
- Survey papers: `paper-types.md`
- Benchmark papers: `paper-types.md`
- Position papers: `paper-types.md`
- Human evaluations (NLP/HCI/alignment): `human-evaluation.md`

### Core Principles

1. **Produce drafts first** — concrete text, not question lists
2. **Never hallucinate citations** — fetch BibTeX programmatically, mark `[CITATION NEEDED]`
3. **Paper is a story** — one-sentence contribution test: specific, falsifiable, interesting
4. **Experiments serve claims** — every experiment supports a stated claim

### One-Sentence Contribution Test

Before writing, state contribution in one sentence and verify:
- Specific, not generic
- Falsifiable, not aspirational
- Interesting to someone outside your immediate lab

### Git Discipline

- Commit after each experiment batch with descriptive messages
- Keep experiment logs connecting results to paper narrative
- Use branches for major revisions and reviewer-response work

### Key References (in `references/research-paper-writing/`)

- `project-setup.md`, `literature-review.md`
- `experiment-design.md`, `experiment-execution.md`
- `experiment-patterns.md`, `result-analysis.md`
- `writing-guide.md`, `reviewer-guidelines.md`
- `citation-workflow.md`, `submission.md`
- `paper-types.md`, `checklists.md`
- `autoreason-methodology.md`, `human-evaluation.md`
- `sources.md`

### Templates (in `templates/research-paper-writing/`)

- Conference templates: NeurIPS, ICML, ICLR, ACL, AAAI, CoLM
- LaTeX templates with math commands
- README per conference with formatting guidance

---

## 4. Smart Home Research (Device Taxonomy & Market Recon)

### Overview

Class-level umbrella for smart-home research, product taxonomy, market reconnaissance, and reference material.

### Trigger

Use when task touches:
- "Smart home" product research or surveys
- Lighting form factors (bulbs, strips, panels, fixtures, outdoor)
- Lighting controls (switches, relays, plugs, remotes, keypads, sensors)
- Protocol/ecosystem comparison (Matter, Thread, Zigbee, Z-Wave, Wi-Fi)
- Vendor/brand landscape mapping for consumer/industrial IoT

### Principles

1. Base research on 2025-2026 products and trends
2. Separate base categories by form factor first, then map brands/models
3. Cite dates for releases/announcements
4. Note protocol support (Matter, Thread, Zigbee, Z-Wave, Wi-Fi)
4. Use `web_search` for market overviews, `web_extract` for editorial comparisons, manufacturer pages for specs

### Research Procedure

1. Confirm category tree and form-factor taxonomy
2. Run parallel `web_search` covering each form factor
3. Supplement with `web_extract` for high-trust editorial sources
4. Collate results into category-organized notes
5. Store reusable research in `references/`
6. Update templates if user wants repeatable output shapes

### Output Format

- Startup: taxonomy overview
- Deep research: category-organized brand/model listing with protocol support and release momentum
- Market notes: takeaway trends and ecosystem gaps
- Knowledge base: references stored under `references/`

### Key References (in `references/smart-home-research/`)

- `lighting-taxonomy-2025-2026.md` — curated deep research
- `research-methodology.md` — sourcing/validation guide

### Templates (in `templates/smart-home-research/`)

- `smart-home-category-template.md` — repeatable category writeup
- `research-sources-template.md` — source log format

### Pitfalls

- Do not invent model names or release dates not seen in research
- Smart-home naming overlaps heavily: flag "same product, different region name"
- Smart mirrors, chandeliers, pendants: thin smart-native offerings; expect bulb-in-fixture bundles
- Smart holiday/outdoor lights: fastest-growing subcategories in 2025-2026
- Smart truck/work lights: largely non-smart; flag when "smart" = high-lumen LED only

---

## Cross-Tool Workflows

| Goal | Tools |
|------|-------|
| Literature review → paper | arXiv (search) → LLM Wiki (organize) → Research Paper Writing (write) |
| Domain recon → paper | Smart Home Research (taxonomy) → LLM Wiki (entities) → Research Paper Writing |
| Paper → knowledge base | Research Paper Writing (read) → LLM Wiki (entities/concepts/comparisons) |
| Ongoing research tracking | LLM Wiki (persistent) + arXiv (new papers) |

---

## Common Pitfalls

1. **arXiv**: Not verifying PDF accessibility, missing category filters, hallucinating citations
2. **LLM Wiki**: Not resuming at session start, duplicate entities, inconsistent tags, missing sources
3. **Research Paper Writing**: Hallucinated citations, no contribution sentence, experiments not tied to claims
4. **Smart Home Research**: Invented models/dates, missing protocol info, region naming overlaps

---

## Verification Checklist

- [ ] arXiv: Papers fetched, metadata extracted, PDFs accessible
- [ ] LLM Wiki: Resumed at session start, no duplicate entities, tags consistent, sources cited
- [ ] Research Paper Writing: Contribution sentence passes test, citations verified, experiments map to claims
- [ ] Smart Home Research: Taxonomy current, brands mapped to form factors, protocols noted, dates cited