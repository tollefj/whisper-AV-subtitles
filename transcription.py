import logging
import os
import shutil
import sys

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.whisper_util import segments_to_srt, whisperx_transcription
from utils.youtube_util import download_audio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "output")


ext = (".mp4", ".mkv", ".avi")


def transcribe(
    media_path: str,
    model: str = "NbAiLabBeta/nb-whisper-small",
    align: bool = True,
    diarize: bool = False,
    save_to_path: str = None,  # saves a subtitled video to the specified path
    delete_files: bool = True,  # deletes the tmp folder (store)
    skip_download: bool = False,
) -> None:
    logger = logging.getLogger(__name__)

    name = media_path.split("/")[-1].split(".")[0]
    tmp_folder = os.path.join(BASE_DIR, "store", name)
    if delete_files:
        shutil.rmtree(tmp_folder, ignore_errors=True)
    os.makedirs(tmp_folder, exist_ok=True)
    STORE = {
        "video": os.path.join(tmp_folder, "video.mp4"),
        "audio": os.path.join(tmp_folder, "audio.mp3"),
        "srt": os.path.join(tmp_folder, "subtitles.srt"),
    }

    if "http" in media_path and not skip_download:
        logger.info("Downloading media...")
        # download_video(media_path, output=STORE["video"])
        # extract_audio(STORE["video"], STORE["audio"])
        download_audio(media_path, output=STORE["audio"])
    else:
        logger.info("Extracting audio...")
        STORE["video"] = media_path
        extract_audio(STORE["video"], STORE["audio"])

    logger.info("Transcribing audio...")
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

    logging.info(f"Transcription complete. See the output files in {tmp_folder}")
    # open the folder in the OS:
    if sys.platform == "darwin":
        os.system(f"open {tmp_folder}")
    elif sys.platform == "win32":
        os.system(f"start {tmp_folder}")
    elif sys.platform == "linux":
        os.system(f"xdg-open {tmp_folder}")

    return STORE


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if sys.argv[1]:
        transcribe(sys.argv[1])
    else:
        print("No media path provided")
        sys.exit(1)
