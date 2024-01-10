import os
import shutil

import ffmpeg

from util import download_video, extract_audio, get_args, transcribe_audio

ext = (".mp4", ".mkv", ".avi")
TMP_FOLDER = "store"
OUTPUT_SRT = f"{TMP_FOLDER}/subtitles.srt"
AUDIO_TMP = f"{TMP_FOLDER}/audio.mp3"


def delete_tmp():
    shutil.rmtree(TMP_FOLDER, ignore_errors=True)


if __name__ == "__main__":
    args = get_args()
    delete_tmp()
    os.makedirs(TMP_FOLDER, exist_ok=True)

    video_path = "store/video.mp4"
    if args.media_path.startswith("http"):
        download_video(args.media_path, output=video_path)
        extract_audio(video_path, AUDIO_TMP)
    elif args.media_path.endswith(ext):
        video_path = args.media_path
        extract_audio(video_path, AUDIO_TMP)
    else:
        AUDIO_TMP = args.media_path

    transcribe_audio(AUDIO_TMP, model_id=args.model, output_file=OUTPUT_SRT)

    if args.save:
        output_file = args.save if args.save.endswith(ext) else args.save + ".mp4"
        output_file = os.path.join("output", output_file)

        (
            ffmpeg.input(video_path)
            .output(
                output_file,
                acodec="aac",
                vf=f"subtitles={OUTPUT_SRT}",
                ar=48000,
                max_muxing_queue_size=9999,
                maxrate="1500k",
                bufsize="2000k",
            )
            .overwrite_output()
            .run()
        )
        delete_tmp()
