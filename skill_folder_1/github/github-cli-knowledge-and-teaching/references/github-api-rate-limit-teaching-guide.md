# GitHub API Rate Limit Teaching Guide

## Lesson: “Quotas are real.”

High-level explanation only.
- Authenticated requests get higher limits
- `X-RateLimit-Remaining` header shows count
- `gh api` handles auth automatically

## Demo
```
gh api /rate_limit --jq .rate
```

## Discussion
Why does GitHub limit API usage?

## Best Practices
- Cache responses when possible
- Use conditional requests (ETag)
- Spread heavy work over time
