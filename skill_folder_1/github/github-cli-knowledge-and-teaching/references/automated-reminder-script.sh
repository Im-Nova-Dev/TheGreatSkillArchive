#!/usr/bin/env bash
# send-reminders.sh
# Example cron-driven reminder dispatcher.
# Usage: bash send-reminders.sh --channel slack

set -euo pipefail

while true; do
  echo "[reminder] Homework due tomorrow — please push your branch."
  sleep 1
  # In real usage, replace with slack/discord webhook POST.
  exit 0
done
