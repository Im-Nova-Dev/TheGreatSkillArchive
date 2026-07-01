---
name: hermes-tweet
description: "Use Hermes Tweet for X/Twitter drafting, live read checks, monitoring, and confirmed account actions from Hermes Agent."
version: 1.0.0
author: Hermes Tweet contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [x, twitter, social-media, hermes-plugin, drafting, monitoring]
    homepage: https://github.com/Xquik-dev/hermes-tweet
---

# Hermes Tweet

Use Hermes Tweet when the user needs X/Twitter research, post drafting,
thread planning, reply preparation, live read checks, or account actions from
Hermes Agent.

## Install

```bash
hermes plugins install Xquik-dev/hermes-tweet
```

Set `XQUIK_API_KEY` before live reads. Set
`HERMES_TWEET_ENABLE_ACTIONS=true` only when the user explicitly wants
account-changing actions available.

## Use

- Draft posts, replies, quote posts, and threads in draft-only mode by default.
- Use live reads only when current X/Twitter context changes the answer.
- Show the final text, target account or post, and action before any write.
- Wait for explicit user confirmation before posting, replying, following,
  liking, reposting, deleting, or changing account state.
- Never ask users to paste API keys, cookies, tokens, or session values into
  chat.

If the API key is missing, continue with planning and drafting only. Do not
simulate live X/Twitter state.
