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

if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg not found. Proceeding with installation..."
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
else
    echo "FFmpeg is already installed."
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Installation complete."