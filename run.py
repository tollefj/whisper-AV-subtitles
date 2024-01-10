import os
import shutil

import fire

from utils.ffmpeg_util import extract_audio, write_video_with_subs
from utils.whisper_util import segments_to_srt, transcribe
from utils.youtube_util import download_video

ext = (".mp4", ".mkv", ".avi")
ext_audio = (".mp3", ".wav", ".ogg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDER = os.path.join(BASE_DIR, "store")
OUTPUT = os.path.join(BASE_DIR, "output")


class Transcriber:
    def __init__(
        self,
        media_path: str,
        model: str = "base",
        align: bool = True,
        diarize: bool = False,
        save_to_path: str = None,  # saves a subtitled video to the specified path
        skip_download: bool = False,
    ) -> None:
        self.media_path = media_path
        self.model = model
        self.align = align
        self.diarize = diarize
        self.save_to_path = save_to_path
        self.skip_download = skip_download

        self.STORE = {
            "video": os.path.join(TMP_FOLDER, "video.mp4"),
            "audio": os.path.join(TMP_FOLDER, "audio.mp3"),
            "srt": os.path.join(TMP_FOLDER, "subtitles.srt"),
        }

        shutil.rmtree(TMP_FOLDER, ignore_errors=True)

    def transcribe(self):
        os.makedirs(TMP_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT, exist_ok=True)

        if self.media_path.startswith("http"):
            download_video(self.media_path, output=self.STORE["video"])
            extract_audio(self.STORE["video"], self.STORE["audio"])
        elif self.media_path.endswith(ext):
            self.STORE["video"] = self.media_path
            extract_audio(self.STORE["video"], self.STORE["audio"])
        elif self.media_path.endswith(ext_audio):
            self.STORE["audio"] = self.media_path

        transcription = transcribe(
            audio_path=self.STORE["audio"],
            model_id=self.model,
            align=self.align,
            diarize=self.diarize,
        )
        subtitles = segments_to_srt(segments=transcription["segments"])

        with open(self.STORE["srt"], "w") as f:
            f.writelines(subtitles)

        if self.save_to_path:
            output_file = (
                self.save_to_path
                if self.save_to_path.endswith(ext)
                else f"{self.save_to_path}.mp4"
            )
            output_file = os.path.join(OUTPUT, output_file)
            write_video_with_subs(self.STORE["video"], self.STORE["srt"], output_file)
            shutil.rmtree(TMP_FOLDER, ignore_errors=True)


if __name__ == "__main__":
    fire.Fire(Transcriber)
