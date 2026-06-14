# Certificate Verification System

## Concept
Each completion certificate includes a verifiable URL or repo reference so employers can confirm a learner finished the course.

## Implementation A — Repo Badge
- Create a private repo named `completions/{github-username}`.
- Add a README with completion metadata.
- Share link with learner.

## Implementation B — Verification Page
- Page lists learner name, cohort, completion date.
- Instructor signs with a GPG-signed comment or via `gh gist` link.

## Implementation C — Ed25519 Signed JSON
```
{
  "name": "Learner Name",
  "cohort": "2026-06",
  "date": "2026-06-20",
  "skills": ["git", "gh", "pr-workflow"],
  "signature": "base64(ed25519(sign(json)))"
}
```

## Privacy Note
Never store raw credentials or secret keys in verification repos.
