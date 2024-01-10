import gc
import time
from datetime import timedelta

import torch
import whisperx
import yaml
from transformers import pipeline

from utils.ffmpeg_util import get_audio_length

secrets = yaml.load(open("secrets.yml", "r"), Loader=yaml.FullLoader)
config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
config = config["whisper"]


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


def transcribe(
    audio_path,
    model_id=None,
    min_speakers=None,
    max_speakers=None,
    align=False,
    diarize=False,
):
    model_id = model_id if model_id else config["model"]
    device = config["device"]
    model = whisperx.load_model(
        model_id, device=device, compute_type=config["compute_type"]
    )

    print("1. Transcribing...")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=config["batch_size"])
    gc.collect()
    torch.cuda.empty_cache()
    del model

    if align:
        print("2. Aligning...")
        alignment, metadata = whisperx.load_align_model(
            language_code=result["language"], device=device
        )
        result = whisperx.align(
            result["segments"],
            alignment,
            metadata,
            audio,
            device,
            return_char_alignments=False,
        )
        gc.collect()
        torch.cuda.empty_cache()
        del alignment

    if diarize:
        print("3. Diarizing...")
        diarize_model = whisperx.DiarizationPipeline(
            use_auth_token=secrets["HF"], device=device
        )
        diarize_segments = diarize_model(
            audio, min_speakers=min_speakers, max_speakers=max_speakers
        )
        diarize_segments = diarize_model(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)

    length_in_seconds = len(audio) / whisperx.audio.SAMPLE_RATE
    print(f"Detected audio with length {length_in_seconds} seconds")
    result["segments"][-1]["end"] = length_in_seconds
    return result


def transcribe_audio(audio_path, model_id):
    device = 0 if torch.cuda.is_available() else -1
    pipe = pipeline(
        "automatic-speech-recognition", model=model_id, chunk_length_s=30, device=device
    )
    prediction = pipe(audio_path, batch_size=8, return_timestamps=True)["chunks"]

    last_timestamp = prediction[-1]["timestamp"]
    duration = get_audio_length(audio_path)
    if last_timestamp[-1] < duration:
        prediction[-1]["timestamp"] = (last_timestamp[0], duration)

    return prediction


def create_segment(index, start, end, text, speaker=None):
    start = time.strftime("%H:%M:%S,000", time.gmtime(start))
    end = time.strftime("%H:%M:%S,000", time.gmtime(end))
    text = text.strip()
    return {
        "index": index,
        "start": start,
        "end": end,
        "text": text,
        "speaker": speaker,
    }


def segments_to_srt(segments, output=None):
    subs = []
    for i, segment in enumerate(segments):
        start = segment["start"]
        end = segment["end"]
        start = time.strftime("%H:%M:%S,000", time.gmtime(start))
        end = time.strftime("%H:%M:%S,000", time.gmtime(end))
        text = segment["text"].strip()
        speaker = segment.get("speaker")
        text = f"{speaker}: {text}" if speaker else text
        sub = f"{i + 1}\n{start} --> {end}\n{text}\n\n"
        subs.append(sub)

    if output:
        with open(output, "w") as f:
            f.writelines(subs)
    return subs