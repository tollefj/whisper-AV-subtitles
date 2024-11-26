import youtube_dl
import yt_dlp


def download_video(url, output="store/video.mp4"):
    max_res = "1080"
    parameters = {
        "format": "bestvideo[ext=mp4][height<="
        + max_res
        + "]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": output,
    }
    with yt_dlp.YoutubeDL(parameters) as video:
        info_dict = video.extract_info(url, download=True)
        video_title = info_dict["title"]
        print(f"Downloaded {video_title}")
        video.download(url)


def download_audio(url, output="store/audio.mp3"):
    with yt_dlp.YoutubeDL(
        {"extract_audio": True, "format": "bestaudio", "outtmpl": output}
    ) as video:
        info_dict = video.extract_info(url, download=True)
        video_title = info_dict["title"]
        print(f"Downloaded {video_title}")
        video.download(url)


# def download_audio(url, output="store/audio.mp3"):
#     # handle escaping the url, including backslashes in urls
#     url = url.replace("\\", "\\\\")
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": output,
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "128",
#             }
#         ],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
