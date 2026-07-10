# video-doc-pipeline

A Claude Code skill that turns a folder of raw footage into a finished, narrated documentary — screening, transcription, paper edit, voice over, music, timeline assembly, QC, and a YouTube-ready package.

**80% AI, 20% human.** The AI does everything heavy and repetitive. You keep the two jobs that matter: deciding the story, and QC with your own eyes and ears. No video editing skill required — if you can write an outline and give notes like "2:04 the photo comes in late", you can direct a film.

Proven in production: 215 raw clips (~57 min) became a published 12:29 documentary in about one working day.

## Install

```
git clone https://github.com/yopiesuryadi/video-doc-pipeline ~/.claude/skills/video-doc-pipeline
```

Then in Claude Code, just describe what you want: *"turn the footage in ~/Videos/trip-2026 into a 10-minute travel doc"*. The skill takes over from there, starting with a tool check.

## Update

Ask Claude: *"update the video-doc-pipeline skill"* — or run `git -C ~/.claude/skills/video-doc-pipeline pull`.

## Requirements

- Claude Code
- macOS with ffmpeg + ImageMagick (`brew install ffmpeg imagemagick`)
- Whisper for transcription (free, local; `mlx-whisper` on Apple Silicon)
- Optional: Palmier Pro (AI-drivable timeline editor, subscription) — without it the skill still delivers a complete paper edit + assembly plan for any editor
- Optional: Higgsfield credits for AI music

Full setup commands: [references/SETUP.md](references/SETUP.md). Hard-won operational traps: [references/GOTCHAS.md](references/GOTCHAS.md).

## What's inside

```
SKILL.md                 the pipeline: 11 steps, hard rules, division of labor
references/SETUP.md      one-time install commands
references/GOTCHAS.md    production lessons (ffmpeg, whisper, Palmier, YouTube)
```

## License

MIT
