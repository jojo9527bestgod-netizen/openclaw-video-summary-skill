# openclaw-video-summary-skill

本地视频总结工作流：先抓音频，再用本地 Whisper 转写，再做文字总结/压缩总结，最后可导出 Word。

## 当前完整流程

```text
链接/文件 → 抽音频 → Whisper 转写 → transcript / 字幕 → 总结模板 → 文字总结 → 导出 Word（可选）
```

## 已支持输入

- Bilibili 链接
- YouTube 链接
- 本地视频文件
- 本地音频文件

## 已支持输出

- `*.m4a`
- `*.txt`
- `*.srt`
- `*.vtt`
- `*-summary-template.md`
- `*.docx`（通过导出脚本）

## 包含内容

- `scripts/video_transcribe.py`：支持 B 站链接、YouTube 链接、本地音频、本地视频
- `scripts/export_docx.py`：把 Markdown/TXT 摘要正确导出为 docx（避免中文乱码）
- `skill/video-summary/`：供 Agent 使用的 skill

## 这套仓库现在能做什么

### 1. 先转写
- 从 B站 / YouTube / 本地视频里拿音频
- 用本地 Whisper 转成 transcript / 字幕

### 2. 再做文字总结
转写完成后，可以继续输出：
- 普通摘要
- 简明版
- 口袋卡片版
- 按章节整理
- 按对象/角色整理
- 操作清单版

当前默认走法：
- 使用已安装的 `summarizer` 思路/skill 对 transcript 做二次压缩总结
- 再按需要整理成群聊版、口袋卡片版或 Word 版

说明：
- `summarize` 这个 skill 虽然已安装，但其底层 CLI 在当前 Intel Mac（x64）上不兼容，因此不作为默认主路
- 当前主路是：Whisper 转写 → `summarizer` 风格文字总结 → 导出 Word（可选）

### 3. 最后导出 Word
如果需要留档或发给别人，可以把整理后的 Markdown / TXT 导出为 `.docx`。

## 用法

### B站链接

```bash
python3 scripts/video_transcribe.py "https://www.bilibili.com/video/BV1GWPiz7EKi/" --name my-video
```

### YouTube 链接

```bash
python3 scripts/video_transcribe.py "https://www.youtube.com/watch?v=xxxx" --name my-youtube-video
```

### 本地视频

```bash
python3 scripts/video_transcribe.py "/path/to/video.mp4" --name my-local-video
```

### 本地音频

```bash
python3 scripts/video_transcribe.py "/path/to/audio.m4a" --name my-audio
```

### 导出 Word

```bash
python3 scripts/export_docx.py output/my-video-summary-template.md --output ~/Desktop/my-video.docx
```

## 依赖

- ffmpeg
- yt-dlp（YouTube 用）
- 本地 `whisper`
- Python 3
- `python-docx`（导出 Word 用，建议放虚拟环境）

## 说明

当前这套仓库已经不只是“转写脚本集合”，而是：
- 转写
- 生成总结模板
- 做文字总结
- 导出 Word

也就是说，它现在更接近一个完整的“视频总结底座”。
