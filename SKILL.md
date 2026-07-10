---
name: video-doc-pipeline
description: End-to-end documentary video pipeline, from a folder of raw clips to a YouTube-ready package. Use when the user wants to turn raw footage into an edited film (mini-doc, travel doc, mission/event recap, family montage with narration) - screening, transcription, paper edit, voice over, music, timeline assembly, QC, and YouTube packaging. Not for social clips/shorts derivation or talking-head videos.
---

# Video Doc Pipeline

Turn raw footage (phone or camera) into a finished narrated documentary. Proven on a real project: 215 clips (~57 min raw) became a published 12:29 film in about one working day.

**Division of labor is the core of this skill.** AI does everything heavy and repetitive. The human owns exactly two things that must never be delegated: **story decisions** (structure, what the climax is, what gets cut) and **QC with their own eyes and ears** before anything is published. A film shipped with VO flubs because QC relied on transcripts alone and had to be deleted and re-uploaded. Do not let that happen again.

Respond and write user-facing documents in the user's language. Keep internal working files in whatever language the user prefers.

## Requirements check (do this first)

Before starting, verify tools and offer to install what's missing (commands in `references/SETUP.md`):

- `ffmpeg` + `ffprobe` (cutting, audio EQ, encoding)
- ImageMagick `montage` (contact sheets)
- Whisper for transcription - on Apple Silicon prefer `mlx-whisper` in a dedicated venv; elsewhere any whisper CLI works
- A timeline editor the agent can drive (Palmier Pro via MCP is proven; check with `get_timeline`). If none is available, the pipeline still works through Step 4 - deliver a paper edit + assembly plan the user can execute in any editor
- Music source: AI generation (e.g. Higgsfield `sonilo_music`, paid credits) or the user's own licensed tracks

Ask the user which are available rather than assuming. Palmier and music generation are paid; never present them as required if the user only wants a rough cut.

## Project structure

One folder per project, created at the start:

```
<project>/
├── source/<YYYY-MM-DD>/   raw clips per shooting day - NEVER rename, NEVER delete
├── source/photos/          photos
├── source/vo-raw.*         VO recording (arrives at Step 4)
├── work/                    every intermediate file (transcripts, selects, music, srt, sheets)
└── (root)                   rough cuts, previews, master
```

Originals are read-only by convention. Everything the agent produces goes in `work/`.

## The pipeline

### Step 0 - Ingest
Human copies files off the phone/card. The agent sorts into `source/<date>/` folders by file timestamp. Verify clip count and total duration with ffprobe; report both.

**Zero-touch trigger (optional):** `automation/card-watcher.sh` + `card-watcher.plist` make macOS launchd watch `/Volumes` and wake the agent the moment a camera card is inserted, so read-only screening starts before the user sits down. Install: copy the plist to `~/Library/LaunchAgents/` with the script's absolute path filled in, then `launchctl bootstrap gui/$(id -u) <plist>`. The notify command inside the script is pluggable (OpenClaw message, webhook, or plain notification).

**Low-storage variant (working from a memory card):** if disk space is tight, Steps 1-3 can read directly from the mounted card (`/Volumes/<card>`) - screening, transcription, and select verification are single-pass sequential reads and safe on a card. Then copy **only the approved selects** (~25-30% of raw) into `source/` and continue normally. Never assemble or render against files on the card: editors re-read media constantly, removable volumes break projects when unplugged, and if the card is the only original it must stay read-only. Do not format the card until the master is rendered and QC'd.

### Step 1 - Screening: thumbnails + contact sheets
Generate a thumbnail per clip (ffmpeg, ~40% into the clip), assemble per-day contact sheets with `montage`. Present sheets to the user and build a per-day log of what was filmed. Mid-clip thumbnails can be misleading - final select verification happens in Step 3.

### Step 2 - Transcribe everything
**HARD RULE: never batch-transcribe on blind auto-detect** - a wrong language guess wastes the entire run. Protocol: if the user already stated the language, use it. Otherwise **detect-and-verify**: auto-detect on 5 sampled clips from different shooting days; if all samples agree, proceed with that language and tell the user which one was picked; if samples disagree or look garbled, stop and ask the user.

Transcribe every clip to `work/transcripts/`, one file per clip. This is the highest-leverage step: transcripts find the audio backbone of the film (recurring briefings, sermons, testimonies, one-liners) that visual screening misses. Read the transcripts and surface the best bites to the user.

### Step 3 - Paper edit (the film is decided here, on paper)
**HARD RULE: no timeline work until the user approves the paper edit.** Produce in `work/`:

1. **Act structure** (typically 5 acts: departure, arrival, the work, climax, return - adapt to the story). Propose which moment is the climax; the user decides. Target duration per act.
2. **Selects** - the shortlist of clips (roughly 25-30% of raw), each with duration and cut notes.
3. **Visual verification of every select** - render a 3-frame strip (10/50/85%) per select and check it against its label. Expect several mislabels; fix them now, not in the editor.
4. Map which audio bites (from Step 2) open or anchor each act - real location audio reduces the VO burden.

Flag privacy-sensitive audio (personal prophecies, pastoral conversations, names of minors) and confirm with the user before using it; visual-only use is often the right call.

**Log footage (iLog, S-Log, D-Log, ...):** apply the camera's official LUT on the fly when generating thumbnails/contact sheets (`-vf lut3d='<lut>.cube'`) so the user reviews normal colors, and bake the LUT into the selects when copying them off the card (`ffmpeg -vf lut3d=... -c:v libx264 -crf 16`) so the editor never has to think about color. Test the LUT on ONE short clip and show the user before batching - a wrong LUT/firmware pairing ruins every select. The card keeps the log originals for serious grading later. If the shoot mixes log and non-log cameras, only the log clips go through the LUT pass.

### Step 4 - Voice over
1. Draft the VO script from the transcripts + act structure. Moments the camera missed can live in VO. Mark facts you could not verify as [FILL] for the user.
2. **Human records** - one clean continuous take beats many fragments; quiet room; phone voice-memo quality is fine.
3. **HARD RULE: the user must LISTEN to the recording with their own ears before assembly.** Transcripts normalize away flubs and doubled words; a transcript check is not QC.
4. The agent cuts the take into per-position blocks and applies EQ. Proven recipe for a quiet-room phone recording: **no denoise** (it muffles), highpass 100 Hz, small dip ~280 Hz, presence lift 3 kHz + 8 kHz, `loudnorm` to about -13.5 LUFS. Leave gaps between VO blocks on the timeline so nothing overlaps.

### Step 5 - Music
One track per act mood (opening / daily life / climax / closing). Generate copyright-free tracks or use the user's library. Bed volume low (~0.15-0.18) with ducking under VO; let the climax act breathe with music down or out.

### Step 6 - Assembly
Write the full assembly plan as a text blueprint first (every clip: start frame, duration, source trim, which VO block and photo overlays it) - then execute it in the editor. Track layout: V1 picture, V2 photo overlays, A1 music, A2 VO, A3 natural clip audio. Duck natural audio to ~0.2 under VO; keep briefings/sermon bites/testimonies at 1.0. Photos: fill-frame + gentle Ken Burns (~6%), and verify each one so no heads are cropped. Title and closing cards. Captions for hard-to-hear speech, built manually from whisper SRT when the audio is bilingual (auto-captioning fails on mixed-language audio). Editor-specific traps are in `references/GOTCHAS.md` - read it before driving Palmier.

**Digital multicam (static-shot rescue):** any long static shot of a speaking person (sermon, testimony, interview) can be cut like a multi-camera shoot using crops of the same footage, as long as source resolution exceeds delivery resolution (4K source → 1080p delivery gives ~2x punch-in room). Build 2-3 virtual angles - tight talking head, medium, full wide - by splitting the clip and giving each segment a different scale+position transform. Switch angles at natural sentence pauses; alternate angles on every cut. This also makes mid-sentence trims invisible: a jump cut disguised as an angle change. Keep punch-ins under ~2x so the crop never upscales visibly; keep headroom and eyeline consistent across angles.

### Step 7 - Review loop
Export preview → user watches → user gives notes as `mm:ss` timestamps → the agent executes all of them → new preview. Repeat until approved (2-3 rounds is normal). Never render the master from an unapproved preview.

### Step 8 - Master + archive
Master at source resolution (H.265 works well). Also offer a **chronological archive**: every raw clip concatenated in time order at 1080p, so the user can wipe cards/phone without losing the record.

### Step 9 - YouTube package
Prepare in `work/youtube/`: 2-3 title options (user picks), description with a CHAPTERS list (timestamps from act positions, starting at `0:00`), tags, 2-3 thumbnail variants (user picks), and SRT subtitles - original language plus a translation if wanted. Keep quotes on thumbnails free of what will read as typos.

### Step 10 - Upload (human)
Manual via YouTube Studio; all files are ready in `work/youtube/`. UI notes (2026): subtitles live under "Languages"; the original language goes in via "Upload manual" at the top, other languages via "Add language". **Final HARD RULE: the user watches the full master before (or immediately after) publishing** - if anything slipped through, replacing the file means a new URL, so catch it first.

## Hands-free mode (optional)

If the machine runs OpenClaw (or a similar chat-to-agent bridge), the whole pipeline can be driven from a phone: commands and VO files arrive via chat, contact sheets and previews go back as files, revision notes come back as timestamped messages. Requirements: the computer stays on and online, and the editor app is open for assembly steps. The two human duties do not change.

## Updating this skill

This skill is distributed as a git repository. When the user asks to update it (e.g. "update the video skill"), run:

```
git -C "$(dirname <path-to-this-SKILL.md>)" pull --ff-only
```

Then report what changed: summarize the new entries at the top of `CHANGELOG.md` (fall back to `git log --oneline HEAD@{1}..HEAD`). If the pull fails because of local edits, show `git status` and let the user decide; never discard their local changes silently.

## Principles (why this works)

1. **Paper edit first, editor second.** Every structural decision is made in markdown before the timeline exists. Assembly becomes execution, not exploration.
2. **Transcribe everything up front.** The best bites are found by reading, not by re-watching hours of footage.
3. **Visually verify every select.** First-pass labels lie.
4. **Never touch originals.** Work in `work/`, archive before anyone wipes a card.
5. **Timestamped review notes.** Precise notes get precise fixes.
