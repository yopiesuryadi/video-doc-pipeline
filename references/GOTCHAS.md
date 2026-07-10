# Gotchas — paid-for lessons, read before executing

## ffmpeg / shell

- Inside a `while read` loop, ffmpeg MUST get `-nostdin`, or it eats the loop's stdin and corrupts the next filenames.
- `-ss` values like `.67` (no leading zero, e.g. from `bc`) are rejected. Wrap with `printf "%.3f"`.
- Contact sheets: `montage` on macOS needs an explicit font or it errors: `-font /System/Library/Fonts/Helvetica.ttc`. In zsh, expand word-split vars with `${=var}`.
- Thumbnail at a single mid-frame is often misleading; verify selects with 3-frame strips (10/50/85%).

## Whisper

- ALWAYS pass `--language` explicitly. Auto-detect can lock onto the wrong language and the whole batch is garbage.
- Transcripts normalize speech: flubs, retakes, and doubled words disappear into clean text. Transcripts are for finding content, never for QC of a recording. QC = human ears.
- Bilingual audio (two languages interleaved) transcribes acceptably but breaks downstream auto-captioning — plan manual captions.

## VO audio processing

- Do NOT denoise a quiet-room recording; denoising muffles the voice. EQ only: highpass 100 Hz, dip ~280 Hz, presence 3 kHz + 8 kHz, loudnorm ≈ -13.5 LUFS.
- Leave gaps between VO blocks on the timeline. Back-to-back blocks clip each other's tails (a final word was cut this way in production).

## Palmier Pro (via MCP)

- Photos: max 150 frames (5 s at 30fps) per `add_clips`; extending via `set_clip_properties` is also rejected. Chain multiple clips for longer holds.
- `add_texts` with fontSize > ~100 fails SILENTLY (ghost clip, doesn't render, doesn't save). Safe max ≈ 92.
- `add_texts`/`add_clips` onto the same track at overlapping times OVERWRITES. Overlapping-in-time elements need separate tracks.
- `add_captions` (auto) produces garbage on bilingual audio. Build captions manually from whisper SRT.
- Photos default to FIT (pillarboxed). For fill-frame set transform {width: 1, height: canvasAR/imageAR}. Ken Burns = simultaneous scale+position keyframes; position anchor is TOP-LEFT, not center.
- `add_clips` without trackIndex creates a new track (safe way to keep music/VO/natural audio on separate tracks).
- Extending a clip mid-timeline: move everything after it first (right-to-left order), then set durationFrames.
- Batch `add_clips` with ~60 entries in one call works fine.
- After placing photos, verify each with `inspect_timeline` — check no heads are cropped.

## YouTube Studio (UI as of 2026)

- Subtitles menu is called "Languages". The ORIGINAL language uploads via "Upload manual" at the top, NOT in the Translations table. Other languages via "Add language".
- Chapters activate automatically when the description contains a timestamp list starting at `0:00`.
- Custom thumbnails require a verified account.
- On a public thumbnail, fix quotes that read as typos (e.g. "missed heaven" → "miss heaven") while keeping in-film VO verbatim — tell the user you did so.
- Replacing a published video's file is impossible; delete + re-upload means a new URL. Hence: full watch-through before publish.
