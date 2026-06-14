# Career Intake Self-Test Scorecard

## Instructions
1. Pull the current `/home/nova/.hermes/intel/career/` listing.
2. Score each intel file on a 0–2 scale per dimension:
   - Stack overlap: does it mention tools/patterns you already know? (0=none, 1=some, 2=exact)
   - Rate evidence: does it include dollar ranges or platform data? (0=none, 1=general, 2=specific)
   - Recency: was it written in the last 60 days? (0=older, 1=last 60 d, 2=last 14 d)
3. Sum scores per domain (OSS/security vs AI implementation).
4. Pick the domain with higher total AND an intel file with overall score >=4.

## Scoring Template
```
File | Stack overlap | Rate evidence | Recency | Total | Domain
```

## Conversion Rule
- Total >= 8 => active pivot target.
- Total 5–7 => keep watching, gather 2 more intel files.
- Total <= 4 => deprioritize in next 14 days.

## Example output
`2026-06-05-browser-automation-ai-contract-market.md | 2 | 2 | 2 | 6 | AI implementation`
