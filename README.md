# Inline video subtitles with Whisper
![tom-scott](assets/tomscott.png)

## Usage

`python transcription.py [-h] [--model MODEL] [--diarize] [--save_to_path SAVE_TO_PATH] media_path language`

Alternatively, `./run.sh` is mapped to `python transcription.py`.

### Arguments

```console
positional arguments:
  media_path            Path to the media file
  language              Language for translation

options:
  -h, --help            show this help message and exit
  --model MODEL         Model for transcription
  --diarize             Whether to diarize the audio
  --save                Whether to render a video + subtitles
```

## Example

- English (with diarization and re-rendering with subtitles):
  - `./run.sh https://www.youtube.com/watch\?v\=Zl_5LT2fzak en --model=base --diarize --save`
- Norwegian (no diarization or re-rendering):
  - `./run.sh https://tv.nrk.no/serie/munter-mat/2023/KOID33006222/avspiller no --model=NbAiLabBeta/nb-whisper-small`

## Setup and installation

- Find the proper PyTorch 2.0 installation for your system:
  - <https://pytorch.org/get-started/previous-versions/#v200>
- run `make`

To support speaker diarization, you need to save your huggingface token in `secrets.yml` in the root dir:

1. Create a huggingface account
2. Accept the terms at <https://huggingface.co/pyannote/speaker-diarization-3.1>
3. Create a token from <https://huggingface.co/settings/tokens>
4. Create `secrets.yml` in the root dir with the following content:

    ```yaml
    HF: <your-token>
    ```

## With other languages/models

Optional models must support FasterWhisper/WhisperX

- `--model=<model-name>`
  - Example model:
  - Norwegian Bokmål: `NbAiLabBeta/nb-whisper-small`

