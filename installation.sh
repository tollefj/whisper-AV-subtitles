# ---------------
# Author: tollefj
# ---------------

# youtube-dl
# check youtube-dl: youtube-dl --version
if [ -z "$(youtube-dl --version | grep '2021')" ]; then
    echo "youtube-dl not installed"
    sudo apt install youtube-dl
else
    echo sudo pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
fi

# ffmpeg
# check if ffmpeg is installed: ffmpeg -version
if [ -z "$(ffmpeg -version | grep 'ffmpeg version')" ]; then
    echo "ffmpeg not installed"
    sudo apt install ffmpeg -y
else
    echo "ffmpeg already installed"
fi


# ffmpeg with cuda
# https://publit.io/community/blog/ffmpeg-with-cuda-and-gpu-accelerated-video-conversion

# transformers
pip install transformers