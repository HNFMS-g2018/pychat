/usr/bin/pychat: main.py ~/.config/pychat/lock
	cp main.py pychat
	chmod +x pychat
	sudo mv pychat /usr/bin/pychat

~/.config/pychat/lock:
	mkdir -p ~/.config/pychat
	touch ~/.config/pychat/init.yaml
	touch ~/.config/pychat/lock
