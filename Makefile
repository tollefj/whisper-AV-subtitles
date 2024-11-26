default: update_permissions install

update_permissions:
	chmod +x install.sh
	chmod +x run.sh

download:
	wget -O nbailab-whisper-q5_0.bin https://huggingface.co/NbAiLab/nb-whisper-medium/resolve/main/ggml-model-q5_0.bin?download=true

install:
	./install.sh
