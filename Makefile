.PHONY: all install_ffmpeg install_python_deps update_permissions clean

all: update_permissions install_ffmpeg install_python_deps

update_permissions:
	chmod +x install.sh

install_ffmpeg:
	./install.sh

install_python_deps:
	pip install -r requirements.txt