import argparse

import youtube_dl


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


def download_video(url, output="store/video.mp4"):
    ydl_opts = {
        # never download anything above 1200 in height, typically 1080p
        "format": "bestvideo[height<=1200][ext=mp4]+bestaudio[ext=m4a]/mp4",
        "outtmpl": output,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
