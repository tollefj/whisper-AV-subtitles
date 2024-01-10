# Simple Subtitles with Whisper
**Generate inline subtitles in videos with Whisper**

### Setup and installation
- run `make`
- To support diarization, you need to save your huggingface token in `secrets.yml` in the root dir:
    1. Create a huggingface account
    2. Accept the terms at https://huggingface.co/pyannote/speaker-diarization-3.1
    3. Create a token from https://huggingface.co/settings/tokens
    4. Create `secrets.yml` in the root dir with the following content:
        ```yaml
        HF: <your-token>
        ```


### Usage
- From a video url:
    - python run.py url --save output_video_filename
- From a local video:
    - python run.py path-to-video --save output_video_filename
