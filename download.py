import argparse
import logging
import os
from utils.youtube_util import download_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "output")

def download(media_path: str, out_name: str) -> None:
    if any(url_like in media_path for url_like in ["http", "www"]):
        download_video(media_path, output=os.path.join(OUTPUT, out_name))
    else:
        raise ValueError("Not a valid media path")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("media_path", help="Path to the media file")
    parser.add_argument("output", help="Name of the output file")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.info(f"Recieved args: {args}")

    download(args.media_path, args.output)
