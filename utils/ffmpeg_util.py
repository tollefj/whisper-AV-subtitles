from sys import platform

import ffmpeg
import torch

# for specifics, see: https://trac.ffmpeg.org/wiki/HWAccelIntro#VideoToolbox
video_codec = "libx264"
if torch.cuda.is_available():
    video_codec = "h264_nvenc"
elif platform == "darwin":
    video_codec = "h264_videotoolbox"


def write_video_with_subs(video_path, srt_path, output_file):
    (
        ffmpeg.input(video_path)
        .output(
            output_file,
            vcodec=video_codec,
            acodec="aac",
            vf=f"subtitles={srt_path}",
            ar=48000,
            max_muxing_queue_size=9999,
            pix_fmt="yuv420p",
            maxrate="1500k",
            bufsize="2000k",
        )
        .overwrite_output()
        .run()
    )


def extract_audio(video_path, audio_path):
    (
        ffmpeg.input(video_path)
        .output(audio_path, format="mp3", audio_bitrate="96k", vn=None)
        .overwrite_output()
        .run()
    )


def get_audio_length(audio_path):
    probe = ffmpeg.probe(audio_path)
    audio_duration = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "audio"), None
    )["duration"]
    return float(audio_duration)
