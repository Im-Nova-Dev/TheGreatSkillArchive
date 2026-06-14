---
name: media-content-tools
description: "Media & content toolbox: GIF search (Tenor), HeartMuLa (AI song generation), Maps (Telegram location), Songsee (audio spectrograms), xurl (social media URLs), YouTube Content (transcripts → summaries), Yuanbao (group mentions/DMs). Use for any media processing, content extraction, or social media workflow."
version: 1.0.0
category: media
tags: [media, gif, music, maps, audio, youtube, social-media, content-extraction, transcripts]
---

# Media & Content Tools

Unified class-level skill covering media processing, content extraction, and social media workflows. Replaces 7 narrow skills: `gif-search`, `heartmula`, `maps`, `songsee`, `xurl`, `youtube-content`, `yuanbao`.

## When to Use

- Search/download GIFs from Tenor for reactions, content, chat
- Generate songs from lyrics/tags via HeartMuLa (Suno-like AI music)
- Work with Telegram location pins and maps
- Generate audio spectrograms/features (mel, chroma, MFCC) via Songsee
- Process social media URLs (extract, format, share) via xurl
- Extract YouTube transcripts and convert to summaries/threads/blogs
- Interact with Yuanbao groups: @mention users, query info/members, send DMs

---

## Decision Guide

| Task | Sub-Tool |
|------|----------|
| Find/download GIFs (Tenor API) | **GIF Search** |
| AI song generation from lyrics/tags | **HeartMuLa** |
| Telegram location pins, maps workflows | **Maps** |
| Audio spectrograms (mel, chroma, MFCC) | **Songsee** |
| Social media URL extraction/formatting | **xurl** |
| YouTube transcripts → summaries/threads/blogs | **YouTube Content** |
| Yuanbao group: @mention, query members, DM | **Yuanbao** |

---

## 1. GIF Search (Tenor API)

### Setup

```bash
# Set API key in ~/.hermes/.env
TENOR_API_KEY=your_key_here

# Get free key: https://developers.google.com/tenor/guides/quickstart
```

### Prerequisites

- `curl` and `jq` (standard on macOS/Linux)
- `TENOR_API_KEY` environment variable

### Search for GIFs

```bash
# Search and get GIF URLs
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'

# Get smaller/preview versions
curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'
```

### Download a GIF

```bash
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif
```

### Get Full Metadata

```bash
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'
```

### API Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (URL-encode spaces as `+`) |
| `limit` | Max results (1-50, default 20) |
| `key` | API key (from `$TENOR_API_KEY`) |
| `media_filter` | Filter formats: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm` |
| `contentfilter` | Safety: `off`, `low`, `medium`, `high` |
| `locale` | Language: `en_US`, `es`, `fr`, etc. |

### Media Formats

| Format | Use Case |
|--------|----------|
| `gif` | Full quality GIF |
| `tinygif` | Small preview GIF |
| `mp4` | Video version (smaller file) |
| `tinymp4` | Small preview video |
| `webm` | WebM video |
| `nanogif` | Tiny thumbnail |

---

## 2. HeartMuLa (AI Song Generation)

### Core Concepts

1. **Prompts** — Genre/mood tags, instrumentation hints, vocal style description
2. **Lyrics** — Structure for music, rhyme and meter, verses/chorus shaping
3. **Iteration** — Seed and variation, style transfer

### Teaching Approach

- Write one short lyric set together
- Generate three prompt variants
- Compare outputs and refine

### Usage

Use for Suno-like song generation from lyrics and tags including prompt crafting, style selection, structure hints, lyric writing for AI music, iteration workflow, and evaluating generated music outputs.

---

## 3. Maps (Telegram Location Pins)

### Capabilities

- Working with Telegram location pins
- Map-related workflows and commands

### Key References (in `references/maps/`)

- `when-to-use.md`, `prerequisites.md`
- `commands.md`
- `working-with-telegram-location-pins.md`
- `workflow-examples.md`
- `pitfalls.md`, `verification.md`

### Scripts (in `scripts/maps/`)

- `maps_client.py`

### Usage

Use `skill_view(name="maps", file_path="references/...")` for detailed workflow guidance.

---

## 4. Songsee (Audio Spectrograms/Features)

### Installation

```bash
# Requires Go
go install github.com/steipete/songsee/cmd/songsee@latest

# Optional: ffmpeg for formats beyond WAV/MP3
```

### Quick Start

```bash
# Basic spectrogram
songsee track.mp3

# Save to specific file
songsee track.mp3 -o spectrogram.png

# Multi-panel visualization grid
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux

# Time slice (start at 12.5s, 8s duration)
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# From stdin
cat track.mp3 | songsee - --format png -o out.png
```

### Visualization Types

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

### Common Flags

| Flag | Description |
|------|-------------|
| `--viz` | Visualization types (comma-separated) |
| `--style` | Color palette: `classic`, `magma`, `inferno`, `viridis`, `gray` |
| `--width`/`--height` | Output image dimensions |
| `--window`/`--hop` | FFT window and hop size |
| `--min-freq`/`--max-freq` | Frequency range filter |
| `--start`/`--duration` | Time slice of audio |
| `--format` | Output format: `jpg` or `png` |
| `-o` | Output file path |

### Notes

- WAV/MP3 decoded natively; other formats need `ffmpeg`
- Output images work with `vision_analyze` for automated audio analysis
- Useful for comparing audio outputs, debugging synthesis, documenting pipelines

---

## 5. xurl (Social Media URL Workflows)

### Core Concepts

- URL extraction from social media
- Metadata retrieval (title, description, images)
- Sharing preparation and formatting

### Teaching Approach

- Extract one post URL data
- Format one shareable summary
- Discuss privacy implications

### Key References (in `references/xurl/`)

- `secret-safety.md`, `installation.md`
- `one-time-user-setup.md`, `quick-reference.md`
- `command-details.md`, `raw-api-access.md`
- `global-flags.md`, `streaming.md`
- `output-format.md`, `common-workflows.md`
- `error-handling.md`, `agent-workflow.md`
- `troubleshooting.md`, `notes.md`, `attribution.md`

### Usage

Use `skill_view(name="xurl", file_path="references/...")` for detailed workflow guidance.

---

## 6. YouTube Content (Transcripts → Summaries/Threads/Blogs)

### When to Use

- User shares YouTube URL/video link
- Request to summarize a video
- Extract/reformat content from YouTube videos

### Setup

```bash
pip install youtube-transcript-api
```

### Helper Script

`SKILL_DIR/scripts/fetch_transcript.py` accepts any standard YouTube URL format.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

### Output Formats

| Format | Description |
|--------|-------------|
| **Chapters** | Timestamped chapter list grouped by topic shifts |
| **Summary** | 5-10 sentence overview |
| **Chapter summaries** | Chapters with paragraph summary each |
| **Thread** | Twitter/X thread format (numbered posts, <280 chars) |
| **Blog post** | Full article with title, sections, key takeaways |
| **Quotes** | Notable quotes with timestamps |

### Workflow

1. **Fetch** transcript: `fetch_transcript.py "URL" --text-only --timestamps`
2. **Validate**: Non-empty, expected language. Retry without `--language` if empty.
3. **Chunk if needed**: Split >50K chars into ~40K chunks with 2K overlap
4. **Transform** to requested format (default: summary)
5. **Verify**: Coherence, correct timestamps, completeness

### Error Handling

- **Transcript disabled** → Tell user; check subtitles on video page
- **Private/unavailable** → Relay error; verify URL
- **No matching language** → Retry without `--language`, note actual language
- **Dependency missing** → `pip install youtube-transcript-api` and retry

---

## 7. Yuanbao (Group Interaction: @Mention, Query, DM)

### CRITICAL: How Messaging Works

**Your text reply IS the message sent to the group/user.** The gateway automatically delivers your response. You do NOT need a special "send message" tool.

When you include `@nickname` in your reply, the gateway converts it to a real @mention that notifies the user.

**NEVER say you cannot send messages or @mention. Just reply with the text.**

### Available Tools

| Tool | When to Use |
|------|-------------|
| `yb_query_group_info` | Query group name, owner, member count |
| `yb_query_group_members` | Find user, list bots, list all members, get nickname for @mention |
| `yb_send_dm` | Send private/direct message (DM/私信) with optional media |

### @Mention Workflow

When you need to @mention / 艾特 someone:

1. Call `yb_query_group_members` with `action="find"`, `name="<target>"`, `mention=true`
2. Get exact nickname from response
3. Include `@nickname` in your reply text — gateway handles the rest

**Example:** User says "帮我艾特元宝"

```json
// Step 1 — tool call
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
```

```text
// Step 2 — your reply (sent to group with working @mention)
@元宝 你好，有人找你！
```

**Rules:**
- Call `yb_query_group_members` first — do NOT guess nickname
- Format: `@nickname` with space before @
- Your reply text IS the message — it WILL be sent
- Be concise. No explanation about @mention mechanics.

### Send DM (Private Message) Workflow

When asked to send 私信/DM to a user:

1. Call `yb_send_dm` with `group_code`, `name` (target user), `message`
2. Tool finds user and sends DM
3. Report result to user

```json
yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })
```

With media:
```json
yb_send_dm({
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "Here is the image",
  "media_files": [{"path": "/tmp/photo.jpg"}]
})
```

**Rules:**
- Extract `group_code` from chat_id: `group:535168412` → `535168412`
- If you know `user_id`, pass directly via `user_id` to skip lookup
- If multiple matches, tool returns candidates — ask user to clarify
- Do NOT use `send_message` for Yuanbao DMs — use `yb_send_dm`
- Media: images (.jpg/.png/.gif/.webp/.bmp) as image messages, others as documents

### Query Group Info

```json
yb_query_group_info({ "group_code": "328306697" })
```

### Query Members

| Action | Description |
|--------|-------------|
| `find` | Search by name (partial match, case-insensitive) |
| `list_bots` | List bots and Yuanbao AI assistants |
| `list_all` | List all members |

### Notes

- `group_code` from chat_id: `group:328306697` → `328306697`
- Groups called "派 (Pai)" in Yuanbao app
- Member roles: `user`, `yuanbao_ai`, `bot`

---

## Cross-Tool Workflows

| Goal | Tools |
|------|-------|
| Social post → GIF reaction | xurl (extract) → GIF Search (find) |
| Video → Audio features | YouTube Content (extract) → Songsee (analyze) |
| Song lyrics → Music video | HeartMuLa (generate) → YouTube Content (promote) |
| Location → Map share | Maps (workflow) → xurl (format) |
| Group coordination | Yuanbao (@mention/DM) + xurl (share links) |

---

## Common Pitfalls

1. **GIF Search**: Missing `TENOR_API_KEY`, not URL-encoding query (`+` for spaces)
2. **HeartMuLa**: Vague prompts — describe journey, not just genre
3. **Maps**: Requires Telegram context; check `references/maps/` for setup
4. **Songsee**: Needs Go + `ffmpeg` for non-WAV/MP3; verify output with `vision_analyze`
5. **xurl**: Privacy implications — don't extract private URLs without consent
6. **YouTube Content**: Transcript disabled → tell user; private video → verify URL; missing language → retry without `--language`
7. **Yuanbao**: Must call `yb_query_group_members` first for exact nickname; reply text IS the message; `group_code` from chat_id

---

## Verification Checklist

- [ ] GIF Search: `TENOR_API_KEY` set, search returns URLs, download works
- [ ] HeartMuLa: Lyric set written, 3 prompt variants generated, outputs compared
- [ ] Maps: Telegram location workflow executes, `maps_client.py` runs
- [ ] Songsee: `songsee` installed, spectrogram generated, multi-panel works
- [ ] xurl: URL extracted, metadata retrieved, shareable summary formatted
- [ ] YouTube Content: Transcript fetched, validated, transformed to requested format
- [ ] Yuanbao: `@nickname` works in reply, DM sent successfully, group query returns data