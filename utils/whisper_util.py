import gc
import logging
import time
import warnings
from typing import Dict

from torch import cuda

# avoid PyAnnote warnings for torchaudio backend.
warnings.filterwarnings("ignore", category=UserWarning)
import whisperx


def whisperx_transcription(
    store,
    config: Dict[str, str],
    diarize_config: Dict[str, str] = None,
    model_id=None,
    min_speakers=None,
    max_speakers=None,
    language="no",
):
    logger = logging.getLogger(__name__)
    if not logging.root.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    logger.info(f"Using whisperx version {whisperx.__version__}")

    logger.info(locals())
    cuda_enabled = cuda.is_available()
    device = "cuda" if cuda_enabled else "cpu"
    model_id = model_id if model_id else config["model"]
    model = whisperx.load_model(
        model_id,
        device=device,
        compute_type=config["compute_type"],
        language=language,
    )

    logger.info("1. Transcribing...")
    audio = whisperx.load_audio(store["audio"])
    result = model.transcribe(audio, batch_size=config["batch_size"])
    if cuda_enabled:
        gc.collect()
        cuda.empty_cache()
    del model

    logger.info("2. Aligning...")

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

    if cuda_enabled:
        gc.collect()
        cuda.empty_cache()
    del alignment

    if diarize_config:
        logger.info("3. Diarizing...")
        diarize_model = whisperx.DiarizationPipeline(
            use_auth_token=diarize_config["HF"], device=device
        )
        diarize_segments = diarize_model(
            audio, min_speakers=min_speakers, max_speakers=max_speakers
        )
        result = whisperx.assign_word_speakers(diarize_segments, result)

    length_in_seconds = len(audio) / whisperx.audio.SAMPLE_RATE
    logger.info(f"Detected audio with length {length_in_seconds} seconds")
    result["segments"][-1]["end"] = length_in_seconds
    return result


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
