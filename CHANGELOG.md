# Changelog

All notable changes to this skill. Update this file with every release — users see it when they pull.

## 2026-07-10 — v0.3.0 "toward 98%"

- **YouTube Data API scripts** (`automation/youtube/`): `yt_auth.py` (one-time OAuth consent) + `yt_publish.py` set title, description+chapters, thumbnail, and multi-language captions on a video via API — the click-heavy part of publishing, automated. File upload stays manual until the project passes YouTube API audit. Secrets live in `~/.config/youtube-pipeline/`, never in the repo.
- **Card-insert watcher** (`automation/`): launchd watches `/Volumes` and wakes the agent the moment a camera card is inserted — screening starts before you sit down. Pluggable notify command (OpenClaw / webhook / notification).
- **Language detect-and-verify**: no more mandatory language question — auto-detect on 5 sampled clips, proceed when they agree, ask only on disagreement.
- **Digital multicam**: official Step 6 technique — cut long static talking shots like a multi-camera shoot using ≤2x crops (tight / medium / wide), switching angles at sentence pauses. Also hides jump cuts.
- **ROADMAP.md**: the published path from 80% AI to 98% AI (human only shoots + one publish tap).

## 2026-07-10 — v0.2.0 "runs anywhere"

- **Agent-neutral wording**: SKILL.md no longer assumes a specific agent — works on Claude Code and OpenClaw (GPT, Kimi, etc.).
- **OpenClaw install path** in README: clone into `~/.openclaw/workspace/skills/` and drive the whole pipeline hands-free from Telegram.
- **Log footage handling** (Step 3): apply the camera LUT on the fly for screening, bake it into selects on ingest, test ONE clip before batching.
- **Low-storage mode** (Step 0): screen/transcribe directly from the memory card (read-only), copy only approved selects (~25-30%) to disk. Never assemble or render from the card.

## 2026-07-10 — v0.1.0 initial release

- Full pipeline: ingest → screening (contact sheets) → transcribe-everything → paper edit (act structure, selects, 3-frame visual verification) → VO (script, EQ recipe, ear-QC rule) → music per act mood → blueprint-first assembly → timestamped review loop → master + chronological archive → YouTube package (title/description/chapters/thumbnails/2-language subtitles) → upload.
- Hard rules: paper edit approved before any timeline work; never touch originals; QC with human eyes and ears before publish.
- `references/SETUP.md` (one-time install) and `references/GOTCHAS.md` (production lessons: ffmpeg, whisper, Palmier Pro, YouTube Studio).
- Proven on a real project: 215 clips (~57 min raw) → published 12:29 documentary in about one working day.
