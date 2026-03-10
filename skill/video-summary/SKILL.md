---
name: video-summary
description: Summarize tutorial, commentary, strategy, lecture, and long-form spoken videos by extracting audio, transcribing locally with Whisper, then turning the transcript into concise summaries, pocket cards, chapter notes, role-based notes, or Word-ready output. Use when the user sends a Bilibili link, YouTube link, local audio file, local video file, or asks to summarize spoken video content from links/files.
---

# Video Summary

Default workflow:
1. If input is a Bilibili link, run `scripts/video_transcribe.py` to fetch audio and transcribe locally.
2. If input is a YouTube link, use the same script to download audio via `yt-dlp`, then transcribe locally.
3. If input is a local video file, extract audio first, then transcribe locally.
4. If input is a local audio file, transcribe it directly.
5. Read the generated `.txt` transcript.
6. Use the generated `*-summary-template.md` as the working skeleton.
7. Produce the format the user asked for:
   - normal summary
   - short summary
   - pocket card / cheat sheet
   - chapter summary
   - role-based notes
   - action checklist
   - Word-ready text

## Scripts

Use:
- `scripts/video_transcribe.py`
- `scripts/export_docx.py`

Examples:

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BVxxxx" --name my-video
python3 scripts/video_transcribe.py "https://www.youtube.com/watch?v=xxxx" --name my-youtube-video
python3 scripts/video_transcribe.py "/path/to/video.mp4" --name my-local-video
python3 scripts/video_transcribe.py "/path/to/audio.m4a" --name my-audio
python3 scripts/export_docx.py output/my-video-summary-template.md --output ~/Desktop/my-video.docx
```

## Output guidance

Keep summaries practical.
Prefer:
- sectioned bullets
- checklist style notes
- pocket card format when asked
- keep the final output shorter than the raw transcript by a large margin

## Limits

- For pure visual videos with little speech, transcript-only summaries may miss screen-only information.
- If transcript quality is noisy, summarize conservatively and say so.
- Bilibili audio extraction currently relies on page parsing and may need maintenance if page structure changes.
