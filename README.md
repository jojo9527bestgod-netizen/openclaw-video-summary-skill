# openclaw-video-summary-skill

本地视频总结工作流：先抓音频，再用本地 Whisper 转写，再让 OpenClaw/Agent 做结构化总结。

## 包含内容

- `scripts/video_transcribe.py`：抓取 B 站音频并调用本地 Whisper 转写
- `skill/video-summary/`：供 Agent 使用的 skill

## 用法

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BV1GWPiz7EKi/" --name my-video
```

输出默认在 `output/`：
- `my-video.m4a`
- `my-video.txt`
- `my-video.srt`
- `my-video.vtt`

## 依赖

- ffmpeg
- 本地 `whisper`
- Python 3

## 说明

当前脚本先稳定支持 Bilibili 链接与本地音频文件。
后续可继续扩展 YouTube / 本地视频抽音频 / 自动生成摘要模板。
