import argparse
import subprocess
import time


def get_subs(prediction):
    subs = []
    for i, pred in enumerate(prediction):
        start, end = pred["timestamp"]
        text = pred["text"].strip()
        start = time.strftime("%H:%M:%S,000", time.gmtime(start))
        end = time.strftime("%H:%M:%S,000", time.gmtime(end))
        srt = f"{i+1}\n{start} --> {end}\n{text}\n\n"
        subs.append(srt)
    return subs


def download_video(url, output="store/video.mp4"):
    cmd = f"youtube-dl -f 'bestvideo[height<=2000][ext=mp4]+bestaudio[ext=m4a]/mp4' --output {output} {url}"
    subprocess.call(cmd, shell=True)


def get_args():
    parser = argparse.ArgumentParser(description="Transcribe and generate subtitles.")
    parser.add_argument("media_path", help="Path to local video/audio or video url")
    parser.add_argument(
        "--model",
        default="openai/whisper-base.en",
        help="Select a Whisper model (huggingface ref). Defaults to the English base model",
    )
    parser.add_argument(
        "--output", default="subtitles.srt", help="Path to the output subtitles file"
    )
    parser.add_argument("--save", help="Path to the output subtitled video file")

    args = parser.parse_args()
    return args
