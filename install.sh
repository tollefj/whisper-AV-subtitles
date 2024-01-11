#!/bin/bash

detect_os() {
    case "$(uname -s)" in
        Linux*)     OS=Linux;;
        Darwin*)    OS=Mac;;
        CYGWIN*)    OS=Cygwin;;
        MINGW*)     OS=MinGw;;
        *)          OS="UNKNOWN:${unameOut}"
    esac

    echo "Detected OS: $OS"
}

install_linux() {
    sudo apt update
    sudo apt install ffmpeg
    # check that cuda 11.8 is installed
    if ! command -v nvcc &> /dev/null; then
        echo "CUDA not found. Proceeding with CPU-only installation."
        # check if conda exists:
        if ! command -v conda &> /dev/null; then
            echo "Conda not found. Proceeding with pip installation."
            pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu

        else
            conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 cpuonly -c pytorch
        fi
    else
        # check if conda exists:
        if ! command -v conda &> /dev/null; then
            echo "Conda not found. Proceeding with pip installation."
            pip install torch==2.0.0+cu113 torchvision==0.15.0+cu113 torchaudio==2.0.0 -f https://download.pytorch.org/whl/torch_stable.html
        else
            conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 -c pytorch
        fi
    fi
    if ! command -v conda &> /dev/null; then
        echo "Conda not found. Proceeding with pip installation."
        pip install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0
    else
        conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 -c pytorch
    fi
}

install_mac() {
    brew install ffmpeg
    # check if conda exists:
    if ! command -v conda &> /dev/null; then
        echo "Conda not found. Proceeding with pip installation."
        pip install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0
    else
        conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 -c pytorch
    fi
}

install_windows() {
    choco install ffmpeg
}

detect_os

case $OS in
    Linux)
        install_linux
        ;;
    Mac)
        install_mac
        ;;
    MinGw|Cygwin)
        # Assuming Windows with MinGw or Cygwin
        if command -v choco &> /dev/null; then
            install_windows
        else
            echo "Chocolatey not found. Please install Chocolatey to proceed with FFmpeg installation on Windows."
        fi
        ;;
    *)
        echo "Unsupported OS for FFmpeg installation"
        ;;
esac

echo "FFmpeg installation complete."
