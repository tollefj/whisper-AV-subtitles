import os
import shutil

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.util import download_video, get_args
from utils.whisper_util import transcribe_audio

ext = (".mp4", ".mkv", ".avi")
ext_audio = (".mp3", ".wav", ".ogg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDER = os.path.join(BASE_DIR, "store")
OUTPUT = os.path.join(BASE_DIR, "output")
STORE = {
    "video": os.path.join(TMP_FOLDER, "video.mp4"),
    "audio": os.path.join(TMP_FOLDER, "audio.mp3"),
    "srt": os.path.join(TMP_FOLDER, "subtitles.srt"),
}


if __name__ == "__main__":
    args = get_args()
    os.makedirs(TMP_FOLDER, exist_ok=True)

    if args.media_path.startswith("http"):
        download_video(args.media_path, output=STORE["video"])
        extract_audio(STORE["video"], STORE["audio"])
    elif args.media_path.endswith(ext):
        extract_audio(args.media_path, STORE["audio"])
    elif args.media_path.endswith(ext_audio):
        STORE["audio"] = args.media_path

    transcribe_audio(STORE["audio"], model_id=args.model, output_file=STORE["srt"])

    if args.save:
        output_file = args.save if args.save.endswith(ext) else args.save + ".mp4"
        output_file = os.path.join(OUTPUT, output_file)
        write_video_with_subs(STORE["video"], STORE["srt"], output_file)
        shutil.rmtree(TMP_FOLDER, ignore_errors=True)
