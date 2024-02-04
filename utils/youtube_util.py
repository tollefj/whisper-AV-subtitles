import youtube_dl


def download_video(url, output="store/video.mp4"):
    ydl_opts = {
        # never download anything above 1200 in height, typically 1080p
        "format": "bestvideo[height<=1200]+bestaudio/best",
        "outtmpl": output,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio(url, output="store/audio.mp3"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
