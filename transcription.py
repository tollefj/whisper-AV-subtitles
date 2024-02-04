import logging
import os
import shutil

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.whisper_util import segments_to_srt, whisperx_transcription
from utils.youtube_util import download_audio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "output")


ext = (".mp4", ".mkv", ".avi")


def transcribe(
    media_path: str,
    model: str,
    align: bool = True,
    diarize: bool = False,
    save_to_path: str = None,  # saves a subtitled video to the specified path
    delete_files: bool = False,  # deletes the tmp folder (store)
    skip_download: bool = False,
) -> None:

    name = media_path.split("/")[-1].split(".")[0]
    tmp_folder = os.path.join(BASE_DIR, "store", name)
    STORE = {
        "video": os.path.join(tmp_folder, "video.mp4"),
        "audio": os.path.join(tmp_folder, "audio.mp3"),
        "srt": os.path.join(tmp_folder, "subtitles.srt"),
    }

    logger = logging.getLogger(__name__)
    if delete_files:
        shutil.rmtree(tmp_folder, ignore_errors=True)
    os.makedirs(tmp_folder, exist_ok=True)

    if "http" in media_path and not skip_download:
        # download_video(media_path, output=STORE["video"])
        # extract_audio(STORE["video"], STORE["audio"])
        download_audio(media_path, output=STORE["audio"])
    else:
        STORE["video"] = media_path
        extract_audio(STORE["video"], STORE["audio"])

    transcription = whisperx_transcription(
        audio_path=STORE["audio"],
        model_id=model,
        align=align,
        diarize=diarize,
    )
    subtitles = segments_to_srt(segments=transcription["segments"])

    with open(STORE["srt"], "w") as f:
        f.writelines(subtitles)

    if save_to_path:
        output_file = (
            save_to_path if save_to_path.endswith(ext) else f"{save_to_path}.mp4"
        )
        output_file = os.path.join(OUTPUT, output_file)
        os.makedirs(OUTPUT, exist_ok=True)
        write_video_with_subs(STORE["video"], STORE["srt"], output_file)
        if delete_files:
            shutil.rmtree(tmp_folder, ignore_errors=True)

    return STORE
