---
name: creative-production
description: "Creative production toolbox: diagrams (architecture, excalidraw, ascii), design systems (popular-web-designs, design-md, claude-design), generative art (comfyui, p5js, pretext, ascii-art, ascii-video, manim-video, touchdesigner-mcp), AI music (songwriting-and-ai-music), infographics (baoyu-infographic), sketching (sketch). Use for any visual/creative task — pick the right sub-tool from the decision guide."
version: 1.0.0
category: creative
tags: [creative, design, diagrams, generative-art, architecture, infographics, ascii, video, music, sketching]
---

# Creative Production

Unified class-level skill covering the full creative toolbox. Replaces 13 narrow skills: `architecture-diagram`, `ascii-art`, `ascii-video`, `baoyu-infographic`, `claude-design`, `comfyui`, `design-md`, `excalidraw`, `manim-video`, `p5js`, `popular-web-designs`, `pretext`, `sketch`, `songwriting-and-ai-music`, `touchdesigner-mcp`.

## When to Use

Any visual/creative task: diagrams, design mockups, generative art, animations, infographics, ASCII art, video production, AI music, design systems. Use the **Decision Guide** below to pick the right sub-tool.

---

## Decision Guide: Pick Your Tool

| You want to... | Use this sub-tool |
|----------------|-------------------|
| Architecture/cloud/infra diagrams as HTML/SVG | **Architecture Diagrams** |
| Hand-drawn style diagrams (flow, sequence, arch) as `.excalidraw` JSON | **Excalidraw** |
| Text banners, cowsay, boxes, image→ASCII | **ASCII Art** |
| Video/audio → colored ASCII MP4/GIF | **ASCII Video** |
| Infographics: 21 layouts × 21 styles, structured content | **Baoyu Infographic** |
| Design process & taste for one-off HTML artifacts (prototypes, decks, landing pages) | **Claude Design** |
| ComfyUI workflows for Stable Diffusion (local/cloud, img2img, inpainting) | **ComfyUI** |
| Formal DESIGN.md token spec files (Google's spec, lint, export to Tailwind/DTCG) | **DESIGN.md** |
| 3Blue1Brown-style math/algorithm animations (Manim CE) | **Manim Video** |
| p5.js creative coding sketches, generative art, interactive demos | **p5js** |
| 54 real design systems (Stripe, Linear, Vercel...) as HTML/CSS templates | **Popular Web Designs** |
| @chenglou/pretext browser demos: text flow, kinetic typography, ASCII obstacles | **Pretext** |
| Throwaway HTML mockups: 2-3 variants to compare before committing | **Sketch** |
| Songwriting craft + Suno AI prompt engineering | **Songwriting & AI Music** |
| TouchDesigner via MCP: real-time visuals, audio-reactive, projection mapping | **TouchDesigner MCP** |
| Human-like writing style (voice, personality, filler, hedging) | **Humanizer** |

---

## Sub-Tools Reference

### Architecture Diagrams

**Scope**: Dark-themed SVG architecture/cloud/infra diagrams as standalone HTML.

**Output**: Single `.html` file with inline SVG, works offline.

**Key references**:
- `references/architecture-diagram/design-system.md` — color palette, typography, component rendering
- `references/architecture-diagram/template.html` — full HTML template with examples
- `templates/architecture-diagram.html` — starter template

**When to use**: Software system architecture, cloud infrastructure, microservice topology, database+API maps.

**Not for**: Scientific diagrams, physical objects, hand-drawn sketches (use Excalidraw), animated explainers (use Manim).

### Excalidraw

**Scope**: Hand-drawn Excalidraw JSON diagrams (arch, flow, seq) as `.excalidraw` files.

**Output**: `.excalidraw` JSON — drag onto excalidraw.com to view/edit.

**Key references**:
- `references/excalidraw/colors.md` — color palette
- `references/excalidraw/dark-mode.md` — dark mode styling
- `references/excalidraw/examples.md` — larger examples
- `scripts/excalidraw/upload.py` — upload for shareable link

**When to use**: Architecture diagrams, flowcharts, sequence diagrams, concept maps.

**Critical**: Use container binding for labels (shape `boundElements` + text `containerId`), NOT `label` property on shapes.

### ASCII Art

**Scope**: Text banners (pyfiglet/asciified API), cowsay, boxes, toilet, image→ASCII, pre-made art search.

**Tools**:
1. **pyfiglet** (local): `python3 -m pyfiglet "TEXT" -f slant`
2. **asciified API** (remote): `curl "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"`
3. **cowsay**: `cowsay -f tux "Linux rules"`
4. **boxes**: `echo "Hello" | boxes -d stone`
5. **toilet**: `toilet --gay "Rainbow!"`
6. **Image→ASCII**: `ascii-image-converter image.png -C`
7. **Search art**: `curl ascii.co.uk/art/cat` + parse `<pre>` tags

**Decision flow**: Banner → pyfiglet/asciified → Message art → cowsay → Border → boxes → Specific thing → ascii.co.uk → Image → ascii-image-converter.

### ASCII Video

**Scope**: Production pipeline for ASCII art video — video/audio/images/generative → colored ASCII MP4/GIF.

**Modes**: Video-to-ASCII, Audio-reactive, Generative, Hybrid, Lyrics/text, TTS narration.

**Pipeline**: INPUT → ANALYZE → SCENE_FN → TONEMAP → SHADE → ENCODE

**Key references** (in `references/ascii-video/`):
- `architecture.md` — grid system, palettes, color, `_render_vf()`, GridLayer
- `composition.md` — blend modes, tonemap, FeedbackBuffer, masking
- `effects.md` — value fields, noise, SDFs, particles, coordinate transforms
- `shaders.md` — ShaderChain, 38 shader catalog, transitions
- `scenes.md` — scene protocol, Renderer, SCENES table, parallel rendering
- `inputs.md` — audio FFT, video sampling, TTS integration
- `optimization.md` — hardware detection, quality profiles
- `troubleshooting.md` — broadcast traps, ffmpeg deadlock, font issues

**Critical**: Use adaptive `tonemap()` (percentile-based), never linear multipliers. Per-scene gamma variation.

### Baoyu Infographic

**Scope**: Infographics with 21 layouts × 21 styles (layout × style matrix).

**Layouts**: linear-progression, binary-comparison, comparison-matrix, hierarchical-layers, tree-branching, hub-spoke, structural-breakdown, bento-grid (default), iceberg, bridge, funnel, isometric-map, dashboard, periodic-table, comic-strip, story-mountain, jigsaw, venn-diagram, winding-roadmap, circular-flow, dense-modules.

**Styles**: craft-handmade (default), claymation, kawaii, storybook-watercolor, chalkboard, cyberpunk-neon, bold-graphic, aged-academia, corporate-memphis, technical-schematic, origami, pixel-art, ui-wireframe, subway-map, ikea-manual, knolling, lego-brick, pop-laboratory, morandi-journal, retro-pop-grid, hand-drawn-edu.

**Workflow**:
1. Analyze content → `analysis.md`
2. Generate structured content → `structured-content.md`
3. Recommend layout×style combos (check keyword shortcuts first)
4. Confirm with user (clarify)
5. Generate prompt → `prompts/infographic.md`
6. Generate image via `image_generate`
7. Output to `infographic/{topic-slug}/`

**Key references**:
- `references/baoyu-infographic/analysis-framework.md`
- `references/baoyu-infographic/base-prompt.md`
- `references/baoyu-infographic/structured-content-template.md`
- `references/baoyu-infographic/layouts/<layout>.md` (21 files)
- `references/baoyu-infographic/styles/<style>.md` (21 files)

**Pitfall**: Never summarize/paraphrase source data. Strip secrets. Style consistency mandatory.

### Claude Design

**Scope**: Design process & taste for one-off HTML artifacts (prototypes, decks, landing pages, component labs). Not for diagrams (Excalidraw/Architecture) or formal specs (DESIGN.md).

**Core principles**:
- Start from context, not vibes
- Ask questions before designing
- Anti-slop rules (no generic AI-looking output)
- First-render excellence — verify with `browser_vision`
- Real content, not lorem ipsum
- Dark backgrounds, warm cores, considered palette

**Workflow**:
1. Clarify brief (feel, references, core action)
2. Produce 2-3 variants with different design stances
3. Verify each visually with browser tools
4. Head-to-head comparison with opinionated recommendation

**Key references** (20+ files in `references/claude-design/`):
- `when-to-use-this-skill-vs-popular-web-designs-vs-design-md.md`
- `runtime-mode.md`, `core-identity.md`, `workflow.md`
- `artifact-format-rules.md`, `html-css-js-standards.md`
- `typography.md`, `color.md`, `layout-and-composition.md`, `motion.md`
- `anti-slop-rules.md`, `variation-rules.md`, `verification.md`

**Templates**: `templates/claude-design/` (starter HTML files)

### ComfyUI

**Scope**: ComfyUI workflows for Stable Diffusion — local/cloud setup, img2img/inpainting, queue management, cloud specifics.

**Key references** (in `references/comfyui/`):
- `whats-in-this-skill.md`, `when-to-use.md`
- `architecture-two-layers.md`, `quick-start.md`
- `core-workflow.md`, `decision-tree.md`
- `setup-onboarding.md`, `image-upload.md`
- `cloud-specifics.md`, `queue-system-management.md`
- `pitfalls.md`, `verification-checklist.md`

**Scripts** (in `scripts/comfyui/`):
- `comfyui_setup.sh`, `health_check.py`, `run_workflow.py`
- `run_batch.py`, `ws_monitor.py`, `check_deps.py`, `auto_fix_deps.py`
- `hardware_check.py`, `fetch_logs.py`, `extract_schema.py`

### DESIGN.md

**Scope**: Author/validate/export Google's DESIGN.md token spec files (YAML frontmatter + Markdown body).

**Tokens**: Colors (hex), dimensions (px/em/rem), typography (fontFamily, size, weight, lineHeight, letterSpacing), components (backgroundColor, textColor, typography, rounded, padding, size, height, width).

**Canonical sections**: Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts.

**CLI**: `npx -y @google/design.md lint|diff|export DESIGN.md`

**Workflow**:
1. Ask/infer brand tone, accent color, typography
2. Write DESIGN.md with token references (`{colors.primary}`)
3. Lint: `npx -y @google/design.md lint DESIGN.md`
4. Export: `--format tailwind` or `--format dtcg`

**Pitfalls**: Don't nest component variants (use `button-primary-hover` not `button-primary.hover`), quote hex colors and negative dimensions, enforce section order.

### Manim Video

**Scope**: 3Blue1Brown-style math/algorithm animations using Manim CE.

**Modes**: Concept explainer, equation derivation, algorithm visualization, data story, architecture diagram, paper explainer, 3D visualization.

**Pipeline**: PLAN → CODE → RENDER → STITCH → AUDIO → REVIEW

**Project structure**: `plan.md`, `script.py`, `concat.txt`, `final.mp4`, `media/`

**Key references** (13 files in `references/manim-video/`):
- `animations.md`, `mobjects.md`, `visual-design.md`
- `equations.md`, `graphs-and-data.md`, `camera-and-3d.md`
- `scene-planning.md`, `rendering.md`, `troubleshooting.md`
- `updaters-and-trackers.md`, `paper-explainer.md`
- `production-quality.md`, `decorations.md`

**Creative standards**: Opacity layering (primary 1.0, contextual 0.4, structural 0.15), breathing room (`self.wait()`), cohesive visual language, geometry before algebra.

**Script**: `scripts/manim-video/setup.sh`

### p5js

**Scope**: Creative coding with p5.js — generative art, interactive demos, animations.

**Key references** (in `references/p5js/`):
- `when-to-use.md`, `whats-inside.md`, `creative-standard.md`
- `modes.md`, `stack.md`, `pipeline.md`
- `creative-direction.md`, `workflow.md`
- `critical-implementation-notes.md`, `performance-targets.md`
- `animation.md`, `color-systems.md`, `core-api.md`
- `export-pipeline.md`, `interaction.md`, `shapes-and-geometry.md`
- `webgl-and-3d.md`, `troubleshooting.md`, `typography.md`
- `visual-effects.md`

**Scripts**: `render.sh`, `serve.sh`, `setup.sh`, `export-frames.js`

### Popular Web Designs

**Scope**: 54 real design systems (Stripe, Linear, Vercel, etc.) as HTML/CSS templates with exact tokens.

**Catalog**: AI/ML (Claude, Cohere, ElevenLabs...), DevTools (Cursor, Linear, Vercel...), Infra (ClickHouse, Stripe...), Design (Figma, Framer, Notion...), Fintech (Coinbase, Revolut...), Enterprise (Apple, BMW, SpaceX...).

**Usage**: Load template → `skill_view(name="popular-web-designs", file_path="templates/linear.app.md")` → apply tokens to HTML → verify with `browser_vision`.

**Pair with**: `claude-design` for process/taste, `design-md` for formal specs.

### Pretext

**Scope**: Creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typography.

**Stack**: `@chenglou/pretext` via esm.sh, Canvas 2D, Intl.Segmenter, raw DOM events.

**Patterns**: Reflow around obstacle, text-as-geometry game, shatter/particles, ASCII obstacle typography, editorial multi-column, kinetic type, multiline shrink-wrap.

**Templates**: `hello-orb-flow.html`, `donut-orbit.html`

**Critical**: Dark backgrounds, real prose (no lorem), proportional fonts, prepare once/cache, first-paint excellence.

### Sketch

**Scope**: Throwaway HTML mockups — 2-3 design variants to compare before committing.

**Method**: intake → variants → head-to-head → pick winner

**Variant axes**: Density (compact/airy/ultra-dense), Emphasis (content/action/tool-first), Aesthetic (editorial/utilitarian/playful), Layout (single-column/sidebar/split-pane), Grounding (card/bare-content/document-style).

**Output**: `sketches/NNN-stance-name/index.html` + `README.md` per variant.

**Verify**: `browser_navigate` + `browser_vision` each variant.

**Interactivity bar**: Click primary action → visible state change, see one meaningful transition, hover affordances work.

### Songwriting & AI Music

**Scope**: Songwriting craft (structure, rhyme, meter, emotional arc, lyrics) + Suno AI prompt engineering.

**Structures**: ABABCB (pop/rock), AABA (jazz/ballads), ABAB, AAA (folk).

**Suno Style Field**: Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics. Describe the JOURNEY, not just genre.

**Metatags**: Structure tags ([Verse], [Chorus], [Bridge]...), Vocal ([Whispered], [Belted]...), Dynamics ([High Energy], [Explosive]...), Gender, Atmosphere, SFX.

**Custom Mode**: Always use for serious work. Lyrics ~3000 chars. Structural tags required.

**Phonetic tricks**: Spell as sounded ("thru"), hyphenate syllables, ALL CAPS = louder, vowel extension ("lo-o-ove").

### TouchDesigner MCP

**Scope**: TouchDesigner via MCP — real-time visuals, audio-reactive GLSL, projection mapping, operator quick reference.

**Key references** (in `references/touchdesigner-mcp/`):
- `critical-rules.md`, `architecture.md`, `setup.md`
- `environment-notes.md`, `workflow.md`
- `mcp-tool-quick-reference.md`, `key-implementation-rules.md`
- `recording-exporting-video.md`, `audio-reactive-glsl.md`
- `operator-quick-reference.md`, `security-notes.md`
- Plus 20+ deep-dive references (operators, geometry, GLSL, MIDI/OSC, etc.)

**Script**: `scripts/touchdesigner-mcp/setup.sh`

### Humanizer

**Scope**: Human-like writing style — voice calibration, personality, content/language/style/communication patterns, filler/hedging.

**Output**: Single self-contained response with natural human cadence.

**Key references** (14 files in `references/humanizer/`):
- `voice-calibration.md`, `personality-and-soul.md`
- `content-patterns.md`, `language-and-grammar-patterns.md`
- `style-patterns.md`, `communication-patterns.md`
- `filler-and-hedging.md`, `process.md`, `output-format.md`
- `full-example.md`, `attribution.md`

---

## Cross-Tool Workflows

| Goal | Tools |
|------|-------|
| Design system → HTML prototype | `design-md` (tokens) → `claude-design` (artifact) |
| Brand style → landing page | `popular-web-designs` (template) → `claude-design` (customization) |
| Diagram → presentation | `architecture-diagram` or `excalidraw` → `manim-video` (animate) |
| Audio → visual | `ascii-video` (audio-reactive) or `touchdesigner-mcp` (audio-reactive GLSL) |
| Infographic → social media | `baoyu-infographic` → `ascii-video` (animate) |
| Song → music video | `songwriting-and-ai-music` (Suno) → `ascii-video` or `manim-video` |

---

## Common Pitfalls

1. **Wrong tool for the job** — use the Decision Guide above
2. **Generic AI output** — apply `claude-design` anti-slop rules, `baoyu-infographic` style consistency
3. **Lorem ipsum** — always use real content
4. **Skipping visual verification** — use `browser_vision` on every HTML artifact
5. **Over-engineering throwaways** — `sketch` and `spike` are disposable by design
6. **Ignoring token references** — in `design-md`, always use `{colors.primary}` not raw hex
7. **Nesting component variants** — `button-primary-hover` not `button-primary.hover`
8. **Linear brightness multipliers** — in `ascii-video`, always use `tonemap()`

---

## Verification Checklist

- [ ] Right sub-tool selected per Decision Guide
- [ ] Real content used (no lorem ipsum)
- [ ] Visual verification with `browser_vision` for HTML outputs
- [ ] Style consistency maintained across artifact
- [ ] Token references used (DESIGN.md) or design system tokens applied
- [ ] Output format matches requirement (HTML, SVG, MP4, GIF, JSON, image)