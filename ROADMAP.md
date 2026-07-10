# Roadmap: 80% AI → 98% AI

Today the human does 5 things: ingest the card, answer the language question, decide the story, record + QC the VO, watch previews, pick title/cover, and upload. The end state: **the human only shoots footage** (plus one publish tap). Everything else below is the path.

## v1 — today (80% AI)

Human: ingest, language answer, story decisions, VO record + listen, preview notes, title/cover pick, upload.

## v1.5 — kill the mechanical steps (≈90% AI)

| Manual step today | Replacement |
|---|---|
| Plug card, wait, then instruct | **Card-insert trigger**: a watcher (launchd on macOS) detects the mounted card and starts screening + transcription unprompted. First contact sheet arrives on the phone before the human sits down. |
| "What language is the audio?" | **Detect-and-verify**: transcribe 5 sampled clips with auto-detect, cross-check agreement; ask the human ONLY when samples disagree. |
| Manual YouTube Studio upload | **YouTube Data API**: video, title, description, thumbnail, and both caption tracks uploaded programmatically as unlisted. Human review happens on the unlisted URL. |

## v2 — fold creative input into the shoot (≈95% AI)

| Manual step today | Replacement |
|---|---|
| Story discussion + structure approval | **Director's log**: while shooting, the human records short voice notes ("today was the baptism — this is the climax", "the hospital story matters, camera missed it"). The agent treats the log as the story brief: structure, climax, and must-include moments come from it. Approval shrinks to one reply: "go" or corrections. |
| VO recording session at home | **Voice clone** (with the owner's consent, trained once on their voice) reads the agent's script — no recording session, no flubs, retakes are free. The director's log audio can also be cut directly into the film as authentic narration. |
| VO ear-check | Clone output is deterministic; alignment QC (script vs. rendered audio via whisper) is automatic. For human-recorded VO, an audio-QC pass detects retakes/doubled words by comparing waveform repetitions, not transcripts. |
| Music mood approval | Mood inferred from the act structure; generated without asking. |

## v3 — replace the human review loop (≈98% AI)

| Manual step today | Replacement |
|---|---|
| Watching every preview | **Adversarial QC panel**: independent agent passes over the rendered preview — visual (cropped heads, black frames, resync drift, caption overlap), audio (loudness, VO collisions, gaps), and story (does the cut match the approved brief?). Issues are fixed and re-rendered before the human ever sees a frame. |
| Title + cover choice | Variants generated, scored by a hook/virality predictor, best one picked. All variants kept in `work/youtube/` for override. |
| Publish | Auto-upload unlisted + full QC report sent to the phone. The human's entire remaining job: watch once if they want, tap **publish**. |

## The 2% that stays human — on purpose

1. **Shooting.** The camera is the one input AI cannot create. Shot discipline (5-shot rule, director's log) becomes MORE important as everything downstream automates.
2. **The publish tap.** This pipeline shipped a film with VO flubs once because QC leaned on transcripts; it had to be deleted and re-uploaded. Final accountability — privacy of people in frame, minors, sensitive audio, and the decision that this story is ready to be public — does not get delegated. One tap, but a human tap.

## Sequencing

v1.5 is pure plumbing (watcher + API), no new AI capability needed — build first. v2's director's log costs nothing to adopt today (just start recording voice notes on shoots) and pays off even before the automation exists. v3's QC panel is the hardest and the most valuable: it is what actually removes the review loop.
