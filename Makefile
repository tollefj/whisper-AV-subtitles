default: update_permissions install

update_permissions:
	chmod +x install.sh
	chmod +x run.sh

install:
	./install.sh
