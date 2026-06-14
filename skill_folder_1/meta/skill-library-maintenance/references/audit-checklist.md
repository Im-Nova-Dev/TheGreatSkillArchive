# Skill library audit checklist

Use this checklist before and after maintenance.

## Before maintenance

1. Confirm skill count: 113
2. Confirm skills with references/ directory
3. Confirm skills with linked_files frontmatter
4. Target: 0 mismatches between items 2 and 3

## During maintenance

For each oversized skill:

- [ ] Does SKILL.md exceed ~320 body lines?
- [ ] Does linked_files have fewer than 3 entries?
- [ ] Did you create references/?
- [ ] Did you move long sections into references/<topic>.md?
- [ ] Is SKILL.md now a focused index?
- [ ] Is linked_files updated with every support file?

## After maintenance

1. Re-run referenced-files scan across all skills
2. Re-run linked_files coverage check
3. Verify skill count unchanged unless intentionally adding/removing
4. Spot-check 3-5 large skills to confirm focused entrypoints

## Common false positives

- A skill with many links is fine even if body is long
- Legacy skills may reference docs/ instead of references/
- Some skills intentionally have 0 links; skip those

## Signals of incomplete splits

- Section headings inside SKILL.md instead of references
- Long code blocks in SKILL.md
- linked_files entry present but file missing
- Frontmatter inside body text (lint error)
