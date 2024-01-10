import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Transcribe and generate subtitles.")
    parser.add_argument("media_path", help="Path to local video/audio or video url")
    parser.add_argument(
        "--model",
        default="openai/whisper-small",
        help="Select a Whisper model (huggingface ref). Defaults to the small model",
    )
    parser.add_argument(
        "--output", default="subtitles.srt", help="Path to the output subtitles file"
    )
    parser.add_argument("--save", help="Path to the output subtitled video file")

    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Download the video from the url (if provided)",
    )

    args = parser.parse_args()
    return args
