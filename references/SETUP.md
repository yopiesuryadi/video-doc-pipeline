# Setup — install commands (macOS)

Everything below is one-time. Versions proven in production: ffmpeg 8.x, ImageMagick 7.x, mlx-whisper 0.4.x (model large-v3-turbo), Higgsfield CLI 1.1.x.

## 1. Base tools (Homebrew)

```
brew install ffmpeg imagemagick node
```

If `brew` is missing, install Homebrew first: https://brew.sh

## 2. Whisper (local transcription)

Apple Silicon (recommended — fast, free, offline after first model download):

```
python3 -m venv <videos-root>/.venv-whisper
<videos-root>/.venv-whisper/bin/pip install mlx-whisper
```

Usage:

```
<videos-root>/.venv-whisper/bin/mlx_whisper clip.mp4 \
  --model mlx-community/whisper-large-v3-turbo \
  --language <lang> --output-dir work/transcripts --output-format txt
```

`--output-format srt` for subtitles. Non-Apple-Silicon machines: use `pip install openai-whisper` or `whisper.cpp` instead; same rule about explicit `--language` applies.

## 3. Timeline editor (Palmier Pro, optional but proven)

1. Install the Palmier Pro desktop app and log in.
2. Register its MCP server with Claude Code so Claude can drive the timeline. The server ships with the Palmier installation; find `server/index.js` under the Palmier MCP directory (one known install location is `~/.openclaw/mcp/palmier-pro/server/index.js`), then:

```
claude mcp add palmier-pro -- node <path-to>/palmier-pro/server/index.js
```

The Palmier app must be open while Claude drives it.

## 4. Music generation (Higgsfield, optional, paid credits)

```
npm install -g @higgsfield/cli
higgsfield auth login
higgsfield workspace set <workspace-id>   # mandatory after login
```

Music model: `sonilo_music`, one generation per act mood. Output is copyright-free.

## 5. Project folder

```
mkdir -p <project>/{source,work,exports}
```

## 6. Hands-free bridge (OpenClaw, optional)

Open source: https://openclaw.ai — Telegram → local agent bridge.

1. Install and run onboarding.
2. Create a bot via @BotFather, put the token in the OpenClaw config.
3. **Lock the bot to your own Telegram ID (`allowFrom`).** Without this anyone can command your machine.
4. It runs as a service (launchd), keeps the machine awake, and transcribes incoming voice notes locally.
