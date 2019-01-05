'Messagebox'
import os

def info(mes):
    'print info on a new window'
    os.system('zenity 2> /dev/null --info --title=\'pychat\' --text=\'' + mes + '\'')
