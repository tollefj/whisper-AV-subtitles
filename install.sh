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
}

install_mac() {
    brew install ffmpeg
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
