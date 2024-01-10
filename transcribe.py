import os
import shutil
import subprocess

import torch
from transformers import pipeline

from util import download_video, get_args, get_subs

device = "cuda:0" if torch.cuda.is_available() else "cpu"
ext = (".mp4", ".mkv", ".avi")
TMP_FOLDER = "store"
OUTPUT_SRT = f"{TMP_FOLDER}/subtitles.srt"
AUDIO_TMP = f"{TMP_FOLDER}/audio.mp3"


def delete_tmp():
    shutil.rmtree(TMP_FOLDER, ignore_errors=True)


def extract_audio(video_path):
    subprocess.call(
        f"ffmpeg -i {video_path} -f mp3 -b:a 96k -vn {AUDIO_TMP} -y", shell=True
    )


def transcribe_audio(audio_path, model_id, output_file, duration=None):
    print(f"Loading model {model_id} on device {device}...")
    pipe = pipeline(
        "automatic-speech-recognition", model=model_id, chunk_length_s=30, device=device
    )
    prediction = pipe(audio_path, batch_size=8, return_timestamps=True)["chunks"]
    last_timestamp = prediction[-1]["timestamp"]
    if duration:
        duration = float(duration)
        if last_timestamp[-1] < duration:
            prediction[-1]["timestamp"] = (last_timestamp[0], duration)

    subs = get_subs(prediction)
    with open(output_file, "w") as f:
        f.writelines(subs)


if __name__ == "__main__":
    args = get_args()
    delete_tmp()
    os.makedirs(TMP_FOLDER, exist_ok=True)

    video_path = "store/video.mp4"
    if args.media_path.startswith("http"):
        download_video(args.media_path, output=video_path)
        extract_audio(video_path)
    elif args.media_path.endswith(ext):
        video_path = args.media_path
        extract_audio(video_path)
    else:
        AUDIO_TMP = args.media_path

    # ffmpeg get the length of the audio file:
    probe_duration_cmd = (
        f"ffprobe -i {AUDIO_TMP} -show_entries format=duration -v quiet -of csv='p=0'"
    )
    probe_duration = subprocess.check_output(
        probe_duration_cmd, shell=True, stderr=subprocess.STDOUT
    ).decode("utf-8")
    print(f"Audio duration: {probe_duration} seconds")

    transcribe_audio(
        AUDIO_TMP, model_id=args.model, output_file=OUTPUT_SRT, duration=probe_duration
    )

    if args.save:
        output_file = args.save if args.save.endswith(ext) else args.save + ".mp4"
        output_file = os.path.join("output", output_file)
        print(f"Saving subtitled video to {output_file}...")

        effects = {
            # "vf": f"scale=1920:1080,subtitles={OUTPUT_SRT}",
            "vf": f"subtitles={OUTPUT_SRT}",
        }
        if torch.cuda.is_available():
            cmd = f"ffmpeg -hwaccel cuvid -hwaccel_output_format cuda -i {video_path} -c:v h264_nvenc -max_muxing_queue_size 9999 -vf {effects['vf']} -c:a aac --ar 48000 -maxrate 1500k -bufsize 2000k {output_file} -y"
        else:
            cmd = f"ffmpeg -i {video_path} -vf {effects['vf']} -c:a aac -ar 48000 -b:a 96k -maxrate 1500k -bufsize 2000k {output_file} -y"
        subprocess.call(cmd, shell=True)

    # delete_tmp()
