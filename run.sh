#!/bin/bash

source venv/bin/activate
# if [ -z "$1" ]; then
#   echo "No media path or url supplied"
#   exit 1
# fi
python transcription.py https://www.youtube.com/watch?v=newJ8YbVWiY --save
