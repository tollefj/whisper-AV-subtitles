update_permissions:
	chmod +x install.sh

install_ffmpeg:
	./install.sh

install_python_deps:
	pip install -r requirements.txt

prep:
	chmod +x run.sh
