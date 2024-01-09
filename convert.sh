#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_path>"
    exit 1
fi

input_path=$1
output_path="audio_tmp.mp3"

ffmpeg -i $input_path -f mp3 -ab 192000 -vn $output_path