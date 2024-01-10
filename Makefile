.PHONY: all install_ffmpeg install_python_deps update_permissions clean

all: update_permissions install_ffmpeg install_python_deps

update_permissions:
	chmod +x install_ffmpeg.sh

install_ffmpeg:
	./install_ffmpeg.sh

install_python_deps:
	pip install -r requirements.txt
