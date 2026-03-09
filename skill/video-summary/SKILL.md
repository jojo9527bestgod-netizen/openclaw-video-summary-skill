---
name: video-summary
description: Summarize tutorial, commentary, strategy, lecture, and long-form spoken videos by extracting audio, transcribing locally with Whisper, then organizing the result into concise notes, pocket cards, or structured summaries. Use when the user sends a Bilibili video link, local audio file, local video file, or asks to summarize spoken video content from links/files.
---

# Video Summary

Default workflow:
1. If input is a Bilibili link, run `scripts/video_transcribe.py` to fetch audio and transcribe locally.
2. If input is a local video file, extract audio first, then transcribe locally.
3. If input is a local audio file, transcribe it directly.
4. Read the generated `.txt` transcript.
5. Use the generated `*-summary-template.md` as the working skeleton.
6. Produce the format the user asked for:
   - normal summary
   - pocket card / cheat sheet
   - chapter summary
   - role-based notes
   - Word-ready text

## Output guidance

Keep summaries practical.
Prefer:
- sectioned bullets
- boss/task/checklist style notes for game guides
- very short “pocket card” format when asked

## Scripts

Use:
- `scripts/video_transcribe.py`

Examples:

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BVxxxx" --name my-video
python3 scripts/video_transcribe.py "/path/to/video.mp4" --name my-local-video
python3 scripts/video_transcribe.py "/path/to/audio.m4a" --name my-audio
```

Output files land in `output/` by default:
- `*.m4a`
- `*.txt`
- `*.srt`
- `*.vtt`
- `*-summary-template.md`

## Limits

- Current script is stabilized first for Bilibili links and local files.
- For pure visual videos with little speech, transcript-only summaries may miss screen-only information.
- If transcript quality is noisy, summarize conservatively and say so.
