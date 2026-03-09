# openclaw-video-summary-skill

本地视频总结工作流：先抓音频，再用本地 Whisper 转写，再让 OpenClaw/Agent 做结构化总结。

## 包含内容

- `scripts/video_transcribe.py`：支持 B 站链接、本地音频、本地视频
- `skill/video-summary/`：供 Agent 使用的 skill

## 用法

### B站链接

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BV1GWPiz7EKi/" --name my-video
```

### 本地视频

```bash
python3 scripts/video_transcribe.py "/path/to/video.mp4" --name my-local-video
```

### 本地音频

```bash
python3 scripts/video_transcribe.py "/path/to/audio.m4a" --name my-audio
```

输出默认在 `output/`：
- `*.m4a`
- `*.txt`
- `*.srt`
- `*.vtt`
- `*-summary-template.md`

## 依赖

- ffmpeg
- 本地 `whisper`
- Python 3

## 说明

当前脚本已稳定支持：
- Bilibili 链接
- 本地音频文件
- 本地视频文件（自动抽音频）

后续计划再扩展 YouTube 下载与转写支持。
