---
name: video-summary
description: Summarize tutorial, commentary, strategy, lecture, and long-form spoken videos by extracting audio, transcribing locally with Whisper, then organizing the result into concise notes, pocket cards, or structured summaries. Use when the user sends a Bilibili video link, local audio/video file, or asks to summarize spoken video content from links.
---

# Video Summary

Default workflow:
1. If input is a Bilibili link, run `scripts/video_transcribe.py` to fetch audio and transcribe locally.
2. If input is a local audio file, transcribe it directly.
3. Read the generated `.txt` transcript.
4. Produce the format the user asked for:
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

Example:

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BVxxxx" --name my-video
```

Output files land in `output/` by default:
- `my-video.m4a`
- `my-video.txt`
- `my-video.srt`
- `my-video.vtt`

## Limits

- Current script is stabilized first for Bilibili links.
- For pure visual videos with little speech, transcript-only summaries may miss screen-only information.
- If transcript quality is noisy, summarize conservatively and say so.
