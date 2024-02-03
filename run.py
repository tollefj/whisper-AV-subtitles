import os
import shutil

import fire

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.whisper_util import segments_to_srt, whisperx_transcription
from utils.youtube_util import download_video

ext = (".mp4", ".mkv", ".avi")
ext_audio = (".mp3", ".wav", ".ogg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDER = os.path.join(BASE_DIR, "store", "tmp")
OUTPUT = os.path.join(BASE_DIR, "output")


STORE = {
    "video": os.path.join(TMP_FOLDER, "video.mp4"),
    "audio": os.path.join(TMP_FOLDER, "audio.mp3"),
    "srt": os.path.join(TMP_FOLDER, "subtitles.srt"),
}

# DEFAULT_MODEL = "base"
DEFAULT_MODEL = "NbAiLabBeta/nb-whisper-small"


def transcribe(
    media_path: str,
    name: str,
    model: str = DEFAULT_MODEL,
    align: bool = True,
    diarize: bool = False,
    save_to_path: str = None,  # saves a subtitled video to the specified path
    delete_files: bool = False,  # deletes the tmp folder (store)
    skip_download: bool = False,
) -> None:
    if delete_files:
        shutil.rmtree(TMP_FOLDER, ignore_errors=True)
        os.makedirs(TMP_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT, exist_ok=True)

    if "http" in media_path and not skip_download:
        download_video(media_path, output=STORE["video"])
        extract_audio(STORE["video"], STORE["audio"])
    elif media_path.endswith(ext):
        STORE["video"] = media_path
        extract_audio(STORE["video"], STORE["audio"])
    elif media_path.endswith(ext_audio):
        STORE["audio"] = media_path

    transcription = whisperx_transcription(
        audio_path=STORE["audio"],
        model_id=model,
        align=align,
        diarize=diarize,
    )
    subtitles = segments_to_srt(segments=transcription["segments"])

    with open(STORE["srt"], "w") as f:
        f.writelines(subtitles)

    if name:
        os.rename(TMP_FOLDER, os.path.join(BASE_DIR, "store", name))

    if save_to_path:
        output_file = (
            save_to_path if save_to_path.endswith(ext) else f"{save_to_path}.mp4"
        )
        output_file = os.path.join(OUTPUT, output_file)
        write_video_with_subs(STORE["video"], STORE["srt"], output_file)
        if delete_files:
            shutil.rmtree(TMP_FOLDER, ignore_errors=True)


if __name__ == "__main__":
    fire.Fire(transcribe)
