import ffmpeg


def write_video_with_subs(video_path, srt_path, output_file):
    (
        ffmpeg.input(video_path)
        .output(
            output_file,
            vcodec="h264_nvenc",
            acodec="aac",
            vf=f"subtitles={srt_path}",
            ar=48000,
            max_muxing_queue_size=9999,
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
