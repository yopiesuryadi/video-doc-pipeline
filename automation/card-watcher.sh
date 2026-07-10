#!/bin/bash
# card-watcher.sh — fires the video-doc-pipeline agent when a memory card is inserted.
# Triggered by launchd on /Volumes changes (see card-watcher.plist).
#
# What it does: scans newly mounted volumes for video files; when a volume looks
# like a camera card (>= MIN_VIDEO_FILES clips), it wakes the agent with an
# instruction to start Step 0-1 (screening from the card, read-only).
# Each volume name triggers at most once per day.

# launchd runs with a minimal PATH; make Homebrew/node visible for the notify command
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

MIN_VIDEO_FILES=5
STATE_DIR="$HOME/Documents/video/logs"
STATE_FILE="$STATE_DIR/card-watcher.state"
LOG_FILE="$STATE_DIR/card-watcher.log"

# The command that wakes your agent. Default: OpenClaw (reply goes to your chat
# channel, e.g. Telegram). Swap for anything else — a notification, a webhook:
#   NOTIFY_CMD() { osascript -e "display notification \"$1\""; }
NOTIFY_CMD() {
  /opt/homebrew/bin/openclaw agent --agent main --deliver -m "$1"
}

mkdir -p "$STATE_DIR"
touch "$STATE_FILE"
TODAY="$(date +%Y-%m-%d)"

for vol in /Volumes/*; do
  [ -d "$vol" ] || continue
  name="$(basename "$vol")"
  case "$name" in "Macintosh HD"*|"Recovery"|"Preboot"|"VM"|"Update") continue ;; esac

  # already handled today?
  grep -qF "$TODAY $name" "$STATE_FILE" && continue

  count=$(find "$vol" -maxdepth 4 \
    \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.insv' -o -iname '*.mts' -o -iname '*.mxf' \) \
    2>/dev/null | head -500 | wc -l | tr -d ' ')
  [ "$count" -lt "$MIN_VIDEO_FILES" ] && continue

  echo "$TODAY $name" >> "$STATE_FILE"
  echo "[$(date '+%F %T')] card detected: $name ($count video files)" >> "$LOG_FILE"

  NOTIFY_CMD "Kartu memori '$name' baru tercolok di Mac, terdeteksi $count file video. Jalankan skill video-doc-pipeline mode low-storage: screening + contact sheet langsung dari kartu di /Volumes/$name (READ-ONLY, jangan tulis apa pun ke kartu), lalu kirim contact sheet dan ringkasan isi per hari ke chat ini." \
    >> "$LOG_FILE" 2>&1
done
