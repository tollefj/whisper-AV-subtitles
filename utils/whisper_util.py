import time

import torch
from transformers import pipeline

from utils.ffmpeg_util import get_audio_length


def get_subs(prediction):
    subs = []
    for i, pred in enumerate(prediction):
        start, end = pred["timestamp"]
        text = pred["text"].strip()
        start = time.strftime("%H:%M:%S,000", time.gmtime(start))
        end = time.strftime("%H:%M:%S,000", time.gmtime(end))
        srt = f"{i+1}\n{start} --> {end}\n{text}\n\n"
        subs.append(srt)
    return subs


def transcribe_audio(audio_path, model_id, output_file):
    device = 0 if torch.cuda.is_available() else -1
    pipe = pipeline(
        "automatic-speech-recognition", model=model_id, chunk_length_s=30, device=device
    )
    prediction = pipe(audio_path, batch_size=8, return_timestamps=True)["chunks"]

    last_timestamp = prediction[-1]["timestamp"]
    duration = get_audio_length(audio_path)
    if last_timestamp[-1] < duration:
        prediction[-1]["timestamp"] = (last_timestamp[0], duration)

    subs = get_subs(prediction)
    with open(output_file, "w") as f:
        f.writelines(subs)
