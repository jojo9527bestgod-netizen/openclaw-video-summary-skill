#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import subprocess
import urllib.request

WORKDIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_OUT = WORKDIR / "output"
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg"}

SUMMARY_TEMPLATE = """# 视频总结模板

## 基本信息
- 文件名：{name}
- 音频：{audio}
- 转写文本：{txt}
- 字幕：{srt}

## 一句话总结
- 

## 核心内容（3-5条）
1. 
2. 
3. 

## 章节/主题拆分
### 1.
- 

### 2.
- 

### 3.
- 

## 可执行要点 / 清单
- 
- 
- 

## 适合输出格式
- 普通摘要
- 口袋卡片版
- 分章节版
- 按角色/对象版

## 备注
- 若转写噪音较大，先校正专有名词再总结。
"""


def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)


def fetch_bilibili_audio(url: str, out_audio: pathlib.Path) -> None:
    html = run(f"curl -L --compressed -A 'Mozilla/5.0' '{url}'")
    m = re.search(r'window\.__playinfo__=(\{.*?\})</script>', html, re.S)
    if not m:
        raise RuntimeError("未找到 Bilibili playinfo，可能页面结构变化或链接不可用")
    obj = json.loads(m.group(1))
    audio_url = obj["data"]["dash"]["audio"][0]["baseUrl"]
    req = urllib.request.Request(audio_url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com/"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out_audio.write_bytes(r.read())


def fetch_youtube_audio(url: str, out_audio: pathlib.Path) -> None:
    cmd = (
        f'yt-dlp -x --audio-format m4a --no-playlist '
        f'-o "{out_audio.with_suffix("%(ext)s")}" "{url}"'
    )
    subprocess.check_call(cmd, shell=True)
    # yt-dlp 输出可能已是 .m4a，也可能按 ext 产物命名，这里做一次收拢
    candidates = list(out_audio.parent.glob(out_audio.stem + '.*'))
    for c in candidates:
        if c.suffix.lower() in AUDIO_EXTS:
            if c != out_audio:
                c.replace(out_audio)
            return
    raise RuntimeError("YouTube 音频下载完成，但未找到输出音频文件")


def extract_audio_from_video(video_path: pathlib.Path, out_audio: pathlib.Path) -> None:
    cmd = (
        f'ffmpeg -y -i "{video_path}" -vn -acodec aac -b:a 192k '
        f'"{out_audio}"'
    )
    subprocess.check_call(cmd, shell=True)


def ensure_whisper_in_path() -> str:
    home_bin = pathlib.Path.home() / "Library/Python/3.9/bin"
    return f"{home_bin}:{pathlib.os.environ.get('PATH','')}"


def transcribe(audio_path: pathlib.Path, out_dir: pathlib.Path, model: str, language: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    path_env = ensure_whisper_in_path()
    cmd = (
        f'PATH="{path_env}" whisper "{audio_path}" '
        f'--language {language} --model {model} --task transcribe '
        f'--output_dir "{out_dir}"'
    )
    subprocess.check_call(cmd, shell=True)


def write_summary_template(out_dir: pathlib.Path, stem: str):
    audio = out_dir / f"{stem}.m4a"
    txt = out_dir / f"{stem}.txt"
    srt = out_dir / f"{stem}.srt"
    md = out_dir / f"{stem}-summary-template.md"
    md.write_text(
        SUMMARY_TEMPLATE.format(name=stem, audio=audio.name, txt=txt.name, srt=srt.name),
        encoding="utf-8",
    )
    return md


def main():
    p = argparse.ArgumentParser(description="抓取 B 站/YouTube 音频、提取本地视频音频，并用本地 Whisper 转写")
    p.add_argument("input", help="B站链接、YouTube 链接、本地音频文件路径、或本地视频文件路径")
    p.add_argument("--name", default="video", help="输出文件前缀")
    p.add_argument("--outdir", default=str(DEFAULT_OUT), help="输出目录")
    p.add_argument("--model", default="base", help="Whisper 模型，默认 base")
    p.add_argument("--language", default="Chinese", help="默认 Chinese")
    args = p.parse_args()

    out_dir = pathlib.Path(args.outdir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_path = out_dir / f"{args.name}.m4a"

    if args.input.startswith("http"):
        if "bilibili.com/video/" in args.input:
            print("[1/3] 抓取 B 站音频…")
            fetch_bilibili_audio(args.input, audio_path)
        elif any(x in args.input for x in ["youtube.com/watch", "youtu.be/"]):
            print("[1/3] 抓取 YouTube 音频…")
            fetch_youtube_audio(args.input, audio_path)
        else:
            raise SystemExit("当前仅支持 Bilibili 与 YouTube 链接")
    else:
        src = pathlib.Path(args.input).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"文件不存在: {src}")
        suffix = src.suffix.lower()
        if suffix in VIDEO_EXTS:
            print("[1/3] 从本地视频提取音频…")
            extract_audio_from_video(src, audio_path)
        elif suffix in AUDIO_EXTS:
            audio_path = src
        else:
            raise SystemExit(f"暂不支持的本地文件类型: {suffix}")

    print(f"[2/3] 本地 Whisper 转写… -> {audio_path}")
    transcribe(audio_path, out_dir, args.model, args.language)

    print("[3/3] 生成摘要模板…")
    md = write_summary_template(out_dir, audio_path.stem)

    txt = out_dir / f"{audio_path.stem}.txt"
    srt = out_dir / f"{audio_path.stem}.srt"
    vtt = out_dir / f"{audio_path.stem}.vtt"
    print("完成：")
    for pth in [audio_path, txt, srt, vtt, md]:
        if pth.exists():
            print(pth)


if __name__ == "__main__":
    main()
