import argparse
import logging
import os

import yaml

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.whisper_util import segments_to_srt, whisperx_transcription
from utils.youtube_util import download_audio, download_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "output")


ext = (".mp4", ".mkv", ".avi")


logging.basicConfig(level=logging.INFO)


def transcribe(
    media_path: str,
    model: str = "NbAiLabBeta/nb-whisper-small",
    diarize: bool = False,
    save_to_path: str = None,  # saves a subtitled video to the specified path
    language="no",
) -> None:
    logger = logging.getLogger(__name__)
    config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)

    name = media_path.split("/")[-1].split(".")[0]
    tmp_folder = os.path.join(BASE_DIR, "store", name)
    os.makedirs(tmp_folder, exist_ok=True)
    STORE = {
        "video": os.path.join(tmp_folder, "video.mp4"),
        "audio": os.path.join(tmp_folder, "audio.mp3"),
        "srt": os.path.join(tmp_folder, "subtitles.srt"),
    }

    if any(url_like in media_path for url_like in ["http", "www"]):
        logger.info("Downloading media...")
        if save_to_path:
            download_video(media_path, output=STORE["video"])
            extract_audio(STORE["video"], STORE["audio"])
        else:
            download_audio(media_path, output=STORE["audio"])
    else:
        logger.info("Extracting audio...")
        STORE["video"] = media_path
        extract_audio(STORE["video"], STORE["audio"])

    logger.info("Transcribing audio...")
    diarize_config = None
    if diarize:
        diarize_config = yaml.load(open("secrets.yml"), Loader=yaml.FullLoader)
    transcription = whisperx_transcription(
        store=STORE,
        config=config["whisper"],
        diarize_config=diarize_config,
        model_id=model,
        language=language,
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

    return STORE


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("media_path", help="Path to the media file")
    parser.add_argument("language", help="Language for translation", default="no")
    parser.add_argument(
        "--model",
        help="Model for transcription",
        default="NbAiLabBeta/nb-whisper-small",
    )
    parser.add_argument(
        "--diarize", help="Whether to diarize the audio", action="store_true"
    )
    parser.add_argument("--save_to_path", help="Path to save the subtitled video")
    args = parser.parse_args()
    print(f"Recieved args: {args}")

    store = transcribe(
        args.media_path,
        model=args.model,
        diarize=args.diarize,
        save_to_path=args.save_to_path,
        language=args.language,
    )
    print(f"Transcription complete. See the output files in {store}")
