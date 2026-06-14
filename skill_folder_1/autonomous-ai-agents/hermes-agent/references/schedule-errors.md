# Schedule and Script Errors Observed

## Rejected schedule forms
- `@every 3m` -> cronparser rejects this prefix
- bare `3m` -> not accepted as standalone schedule

## Working schedule form
- `every 3m`
- `every 6m`
- `every 4m`
- `every 1m`
- `every 10m`
- `every 20m`
- `0 */6 * * *`

## Script path errors
- `script: '/home/nova/.hermes/scripts/random-skill-elaborator.py'` -> rejected as absolute/home-relative
- Workaround: keep scripts in `~/.hermes/scripts/` and reference by bare filename in the cron

## Frontmatter / JSON write errors
- Skill files expecting minimal YAML frontmatter; complex JSON inside frontmatter caused write_file errors.
- Fix: keep frontmatter simple; put rich data outside frontmatter or load via script.