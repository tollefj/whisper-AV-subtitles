# Simple Subtitles with Whisper
**Generate inline subtitles in videos with Whisper**

### Setup
run `make`

### Usage
- From a video url:
    - python transcribe.py url --save output_video_filename
- From a local video:
    - python transcribe.py path-to-video --save output_video_filename

Requires:
- ffmpeg
- python (see `requirements.txt`)

