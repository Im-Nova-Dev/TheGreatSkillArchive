#!/bin/bash
# Count skills and append a timestamped entry to a markdown log.

DOCS_DIR="$HOME/Documents"
LOG_FILE="$DOCS_DIR/skill-count-log.md"
SKILLS_DIR="$HOME/.hermes/skills"

mkdir -p "$DOCS_DIR"

TOTAL=$(find "$SKILLS_DIR" -maxdepth 2 -name 'SKILL.md' | wc -l)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

cat >> "$LOG_FILE" <<EOF
## $TIMESTAMP

- **Total skills counted:** $TOTAL

EOF
