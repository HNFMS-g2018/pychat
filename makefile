pips=pip/argparse.lock pip/colorama.lock pip/leancloud.lock pip/yaml.lock

all: $(pips) /usr/bin/pychat ~/.config/pychat/lock
	echo -e '\033[32minstalled\033[0m!!'

/usr/bin/pychat: main.py
	cp main.py pychat
	chmod +x pychat
	sudo mv pychat /usr/bin/pychat

~/.config/pychat/lock:
	mkdir -p ~/.config/pychat
	touch ~/.config/pychat/init.yaml
	echo 'exist: true' > ~/.config/pychat/init.yaml
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

