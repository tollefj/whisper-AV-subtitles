import argparse
import subprocess
import time

import ffmpeg
import torch
import youtube_dl
from transformers import pipeline


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


def extract_audio(video_path, audio_path):
    (
        ffmpeg.input(video_path)
        .output(audio_path, format="mp3", audio_bitrate="96k", vn=True)
        .overwrite_output()
        .run()
    )


def get_audio_len(audio_path):
    cmd = (
        f"ffprobe -i {audio_path} -show_entries format=duration -v quiet -of csv='p=0'"
    )
    duration = subprocess.check_output(
        cmd, shell=True, stderr=subprocess.STDOUT
    ).decode("utf-8")
    return float(duration)


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


def transcribe_audio(audio_path, model_id, output_file):
    device = 0 if torch.cuda.is_available() else -1
    pipe = pipeline(
        "automatic-speech-recognition", model=model_id, chunk_length_s=30, device=device
    )
    prediction = pipe(audio_path, batch_size=8, return_timestamps=True)["chunks"]

    last_timestamp = prediction[-1]["timestamp"]
    duration = get_audio_len(audio_path)
    if last_timestamp[-1] < duration:
        prediction[-1]["timestamp"] = (last_timestamp[0], duration)

    subs = get_subs(prediction)
    with open(output_file, "w") as f:
        f.writelines(subs)
