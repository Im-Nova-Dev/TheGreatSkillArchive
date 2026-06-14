---
name: productivity-tools
description: "Productivity toolbox: Airtable (bases/tables/automations), Blogwatcher (RSS/Atom feeds), Google Workspace (Docs/Sheets/Slides/Drive/Gmail/Calendar), Himalaya (IMAP/SMTP email CLI), nano-pdf (NL PDF editing), Obsidian (vault notes), PowerPoint (automation), Teams Meeting Pipeline (summarization). Use for any personal/productivity workflow."
version: 1.0.0
category: productivity
tags: [productivity, airtable, rss, google-workspace, email, pdf, obsidian, powerpoint, teams, notes]
---

# Productivity Tools

Unified class-level skill covering personal/productivity workflows. Replaces 8 narrow skills: `airtable`, `blogwatcher`, `google-workspace`, `himalaya`, `nano-pdf`, `obsidian`, `powerpoint`, `teams-meeting-pipeline`.

## When to Use

- Airtable: bases, tables, fields, filters, views, forms, automations, API access
- Blog/RSS monitoring: tracking feeds, auto-discovery, OPML import, read/unread management
- Google Workspace: Docs, Sheets, Slides, Drive, Gmail, Calendar, Apps Script, mail merge
- Terminal email: IMAP/SMTP via Himalaya CLI (compose, read, search, move, flags)
- PDF editing: natural-language text/typos/title edits via nano-pdf CLI
- Obsidian vault: read/search/create/edit notes, wikilinks, vault conventions
- PowerPoint: read/edit/create slides, design ideas, convert to images
- Teams meetings: capture, summarize, replay, manage Graph subscriptions

---

## Decision Guide

| Task | Sub-Tool |
|------|----------|
| Structured data, trackers, project management | **Airtable** |
| Monitor blogs, RSS/Atom feeds | **Blogwatcher** |
| Docs, sheets, slides, drive, gmail, calendar | **Google Workspace** |
| Terminal email client (IMAP/SMTP) | **Himalaya** |
| Edit PDF text/typos via natural language | **nano-pdf** |
| Personal knowledge base, linked notes | **Obsidian** |
| PowerPoint automation (read/write/convert) | **PowerPoint** |
| Teams meeting summaries & pipeline | **Teams Meeting Pipeline** |

---

## 1. Airtable

### Core Concepts

- **Bases** — databases containing tables
- **Tables** — records with typed fields
- **Fields** — single line text, long text, attachment, checkbox, select, formula, rollup, lookup, etc.
- **Views** — grid, calendar, kanban, gallery, form, timeline

### Workflows

```bash
# API access via curl (requires AIRTABLE_API_KEY)
curl -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  "https://api.airtable.com/v0/<BASE_ID>/<TABLE_NAME>"

# Create record
curl -X POST -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Name": "Task 1", "Status": "Todo"}}' \
  "https://api.airtable.com/v0/<BASE_ID>/<TABLE_NAME>"

# Filter views
curl "https://api.airtable.com/v0/<BASE_ID>/<TABLE_NAME>?filterByFormula={Status}='Done'"
```

### Teaching Approach

1. Build one tracker base
2. Add one filter view and one form
3. Use API to read records

---

## 2. Blogwatcher (RSS/Atom Feed Monitoring)

### Installation

```bash
# Go
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Binary (Linux amd64)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli

# Docker
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

### Common Commands

```bash
# Add blog (auto-discovers feed)
blogwatcher-cli add "My Blog" https://example.com

# Add with explicit feed
blogwatcher-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml

# Add with HTML scraping
blogwatcher-cli add "My Blog" https://example.com --scrape-selector "article h2 a"

# List tracked blogs
blogwatcher-cli blogs

# Scan for new articles
blogwatcher-cli scan
blogwatcher-cli scan "My Blog"

# List unread articles
blogwatcher-cli articles
blogwatcher-cli articles --blog "My Blog"
blogwatcher-cli articles --category "Engineering"

# Mark read/unread
blogwatcher-cli read 1
blogwatcher-cli unread 1
blogwatcher-cli read-all
blogwatcher-cli read-all --blog "My Blog" --yes

# Import from OPML
blogwatcher-cli import subscriptions.opml
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BLOGWATCHER_DB` | SQLite database path (default: `~/.blogwatcher-cli/blogwatcher-cli.db`) |
| `BLOGWATCHER_WORKERS` | Concurrent scan workers (default: 8) |
| `BLOGWATCHER_SILENT` | Only output "scan done" |
| `BLOGWATCHER_YES` | Skip confirmations |
| `BLOGWATCHER_CATEGORY` | Default category filter |

### Docker Persistence

```bash
# Named volume
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan

# Host bind mount
docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

---

## 3. Google Workspace

### Core Topics

1. **Documents** — Docs, Sheets, Slides basics, comments, suggestions
2. **Collaboration** — Sharing/permissions, live editing, history
3. **Automation** — Google Apps Script, Forms, mail merge
4. **Organization** — Drive structure, search, labels

### Key References (in `references/google-workspace/`)

- `gmail-search-syntax.md` — Gmail search operators
- `scripts/google_api.py` — API wrapper
- `scripts/gws_bridge.py` — Bridge for Hermes
- `scripts/setup.py` — First-time setup

### Teaching Approach

1. Create one shared doc end-to-end
2. Add one scripted automation
3. Review one messy shared drive

---

## 4. Himalaya (Terminal Email CLI)

### Installation

```bash
# Pre-built binary (recommended)
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS
brew install himalaya

# Cargo
cargo install himalaya --locked
```

### Configuration

Run interactive wizard:
```bash
himalaya account configure
```

Or create `~/.config/himalaya/config.toml`:
```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"

# Folder aliases (v1.2.0+ syntax — REQUIRED for Gmail)
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

### Common Operations

```bash
# List emails
himalaya envelope list
himalaya envelope list --folder "Sent" --page 1 --page-size 20

# Search
himalaya envelope list from john@example.com subject meeting

# Read email
himalaya message read 42
himalaya message export 42 --full

# Reply (non-interactive)
himalaya template reply 42 | sed 's/^$/\\nYour reply here\\n/' | himalaya template send

# Forward
himalaya template forward 42 | sed 's/^To:.*/To: new@example.com/' | himalaya template send

# New email
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test
Hello from Himalaya!
EOF

# Move/copy/delete
himalaya message move 42 "Archive"
himalaya message copy 42 "Important"
himalaya message delete 42

# Flags
himalaya flag add 42 --flag seen
himalaya flag remove 42 --flag seen

# Attachments
himalaya attachment download 42 --dir ~/Downloads

# JSON output
himalaya envelope list --output json
```

### Critical: Folder Alias Syntax

Use `folder.aliases.X` (plural, dotted) NOT `[accounts.NAME.folder.alias]` (singular, subsection). The old syntax is silently ignored in v1.2.0+, causing sent-mail save failures and duplicate emails on retry.

---

## 5. nano-pdf (Natural Language PDF Editing)

### Installation

```bash
uv pip install nano-pdf
# or: pip install nano-pdf
```

### Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

### Examples

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

### Notes

- Page numbers may be 0-based or 1-based — retry with ±1 if wrong page
- Verify output PDF after editing
- Requires LLM API key (check `nano-pdf --help`)
- Works for text changes; complex layouts need other tools

---

## 6. Obsidian Vault

### Vault Path

Use `OBSIDIAN_VAULT_PATH` env var (from `~/.hermes/.env`) or fallback `~/Documents/Obsidian Vault`.

Resolve to absolute path before file tools — paths may contain spaces.

### Operations

| Action | Tool |
|--------|------|
| Read note | `read_file` with absolute path |
| List notes | `search_files(target="files", pattern="*.md", path=<vault>)` |
| Search content | `search_files(target="content", pattern=<regex>, file_glob="*.md", path=<vault>)` |
| Create note | `write_file` with absolute path + markdown |
| Append note | `read_file` → `patch` (anchored) or `write_file` (full rewrite) |
| Targeted edit | `patch` with stable context |

### Wikilinks

Use `[[Note Name]]` syntax. For cross-directory: relative paths.

### Vault Conventions

- Canonical filenames: `Fox_Kitesune.md` not `Fox.md`
- Frontmatter: `**Species**`, `**Tier**`, `**Tags**`, `**Sources**`, `**Last Updated**`
- Link format: `[[filename.md]]` same-dir, relative paths cross-dir
- Sources use wikilinks to index/monetization/game-plan files

### Update Workflow

- Bulk link normalization via deterministic script
- Deduplicate before expanding (collapse synonyms)
- Validate node view accuracy on stable sample

---

## 7. PowerPoint

### Capabilities

- Read content from slides
- Edit existing slides
- Create presentations from scratch
- Apply design ideas
- QA (required)
- Convert to images

### Key References (in `references/powerpoint/`)

- `when-to-use.md`, `quick-reference.md`
- `reading-content.md`, `editing-workflow.md`
- `creating-from-scratch.md`, `design-ideas.md`
- `qa.md`, `converting-to-images.md`
- `dependencies.md`

### Scripts (in `scripts/powerpoint/`)

- `add_slide.py`, `clean.py`, `__init__.py`

### Usage

Use `skill_view(name="powerpoint", file_path="references/creating-from-scratch.md")` for detailed workflow.

---

## 8. Teams Meeting Pipeline

### Core Workflow

1. Trigger meeting capture
2. Inspect job status
3. Replay summary
4. Manage Microsoft Graph subscriptions

### Teaching Approach

- Run one meeting pipeline end-to-end
- Review one pipeline status output
- Repeat one failed job safely

### Key References (in `references/teams-meeting-pipeline/`)

- Use `skill_view(name="teams-meeting-pipeline", file_path="references/...")` for detailed workflow.

---

## Cross-Tool Workflows

| Goal | Tools |
|------|-------|
| Email → Task tracker | Himalaya (read) → Airtable (create record via API) |
| Blog feed → Knowledge base | Blogwatcher (scan) → Obsidian (create notes) |
| Meeting → Action items | Teams Pipeline (summary) → Airtable (track) / Obsidian (notes) |
| PDF contract → Tracker | nano-pdf (extract/edit) → Airtable (log) |
| Drive doc → Presentation | Google Workspace (read) → PowerPoint (create) |

---

## Common Pitfalls

1. **Himalaya folder aliases** — Use `folder.aliases.X` (v1.2.0+), not old subsection syntax
2. **Obsidian vault path** — Resolve to absolute path; don't pass shell variables to file tools
3. **nano-pdf page numbers** — Try ±1 if edit hits wrong page
4. **Blogwatcher Docker** — Use volume mount for DB persistence
5. **Google Workspace auth** — Run `scripts/setup.py` for first-time OAuth
6. **PowerPoint QA** — Always run QA checks after edits
7. **Teams subscriptions** — Manage Graph subscriptions carefully to avoid duplicates

---

## Verification Checklist

- [ ] Airtable: API key configured, base accessible, API calls work
- [ ] Blogwatcher: `blogwatcher-cli blogs` shows tracked feeds, `scan` finds articles
- [ ] Google Workspace: OAuth configured, API calls succeed
- [ ] Himalaya: `himalaya envelope list` works, folder aliases correct
- [ ] nano-pdf: `nano-pdf --help` works, test edit produces expected output
- [ ] Obsidian: Vault path resolved, `read_file`/`search_files` work
- [ ] PowerPoint: Scripts run, QA passes
- [ ] Teams Pipeline: Can trigger capture, view status, replay summary