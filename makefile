pips=pip/argparse.lock pip/colorama.lock pip/leancloud.lock pip/yaml.lock

all: $(pips) /usr/bin/pychat /usr/bin/update-pychat ~/.config/pychat/lock
	@echo -e '\033[32minstalled\033[0m!!'

/usr/bin/update-pychat:
	touch update-pychat
	echo '#!/bin/bash' > update-pychat
	echo -n 'dir=' >> update-pychat
	pwd >> update-pychat
	echo 'cd $$dir/ ; git pull' >> update-pychat
	chmod +x update-pychat
	sudo mv update-pychat /usr/bin/update-pychat

/usr/bin/pychat: main.py _*py
	touch pychat
	echo '#!/bin/bash' > pychat
	echo -n 'dir=' >> pychat
	pwd >> pychat
	echo 'python3 $$dir/main.py $$@' >> pychat
	# cp main.py pychat
	chmod +x pychat
	sudo mv pychat /usr/bin/pychat

~/.config/pychat/lock:
	mkdir -p ~/.config/pychat
	cp example.yaml ~/.config/pychat/init.yaml
	touch ~/.config/pychat/lock

pip/argparse.lock:
	pip3 install argparse
	touch pip/argparse.lock

pip/colorama.lock:
	pip3 install colorama
	touch pip/colorama.lock

pip/leancloud.lock:
	pip3 install leancloud
	touch pip/leancloud.lock

pip/yaml.lock:
	pip3 install pyyaml
	touch pip/yaml.lock

