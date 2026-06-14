---
name: file-writing-resilience
description: Fallback patterns for writing complex content when standard file tools hit quoting/escaping limits. Use when patch/write_file fail due to nested backticks, triple quotes, YAML frontmatter, bulk markdown, or Obsidian-style wikilinks.
---

# File Writing Resilience

Fallback patterns for writing complex content when `write_file` or `patch` hit quoting/escaping limits.

## When This Applies

- `write_file` or `patch` fails because the content contains backticks, triple quotes, or complex markdown/YAML
- You need to write many files with similar scaffolding in bulk
- Content includes YAML frontmatter, nested code blocks, or Obsidian-style `[[wikilinks]]`

## Preferred Order

1. `write_file` — use first for simple text
2. `patch` — use for targeted edits in existing files
3. `execute_code` with Python `Path.write_text()` — fallback when 1-2 fail or content is complex
4. `execute_code` with Python loop — use for bulk creation (>3 files)

## Minimal Python Template

```python
from pathlib import Path
p = Path('/path/to/file.md')
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(content)
```

## Pitfalls

- Do not use this for binary files — stick to text/markdown/YAML/JSON/TOML
- `write_file` auto-runs linters for some extensions; Python does not. Run checks manually if syntax matters.
- Large single writes (>50KB) may hit output caps. Split into chunks if needed.
