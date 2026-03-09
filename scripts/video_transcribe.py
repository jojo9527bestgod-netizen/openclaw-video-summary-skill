#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

WORKDIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_OUT = WORKDIR / "output"


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


def main():
    p = argparse.ArgumentParser(description="抓取 B 站音频并用本地 Whisper 转写")
    p.add_argument("input", help="B站视频链接，或本地音频文件路径")
    p.add_argument("--name", default="video", help="输出文件前缀")
    p.add_argument("--outdir", default=str(DEFAULT_OUT), help="输出目录")
    p.add_argument("--model", default="base", help="Whisper 模型，默认 base")
    p.add_argument("--language", default="Chinese", help="默认 Chinese")
    args = p.parse_args()

    out_dir = pathlib.Path(args.outdir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_path = out_dir / f"{args.name}.m4a"

    if args.input.startswith("http"):
        if "bilibili.com/video/" not in args.input:
            raise SystemExit("目前脚本先稳定支持 Bilibili 视频链接")
        print("[1/2] 抓取 B 站音频…")
        fetch_bilibili_audio(args.input, audio_path)
    else:
        src = pathlib.Path(args.input).expanduser().resolve()
        if not src.exists():
            raise SystemExit(f"文件不存在: {src}")
        audio_path = src

    print(f"[2/2] 本地 Whisper 转写… -> {audio_path}")
    transcribe(audio_path, out_dir, args.model, args.language)

    txt = out_dir / f"{audio_path.stem}.txt"
    srt = out_dir / f"{audio_path.stem}.srt"
    vtt = out_dir / f"{audio_path.stem}.vtt"
    print("完成：")
    for pth in [audio_path, txt, srt, vtt]:
        if pth.exists():
            print(pth)


if __name__ == "__main__":
    main()
