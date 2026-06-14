# Course Completion API / Webhook Template

## Concept
Emit an event when a learner completes the course.

## Payload (Example JSON)
```
{
  "event": "course.completed",
  "learner": "octocat",
  "cohort": "2026-06",
  "skills": ["git", "gh", "pr-workflow", "actions"],
  "completed_at": "2026-06-20T17:00:00Z"
}
```

## Uses
- Issue a badge
- Send certificate email
- Update alumni directory
- Trigger celebration message in chat

## Implementation note
Use a simple webhook or GitHub Actions workflow dispatch. Never expose secrets in payload.
