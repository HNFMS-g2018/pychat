'Messagebox'
import os

def info(mes):
    'print [mes] on a new window'
    os.system('zenity 2> /dev/null --info \
            --title=\'pychat\' --text=\'' + mes + '\'')

def warning(mes):
    'print [mes] on a new windows as a warning'
    os.system('zenity 2> /dev/null --warning \
            --title=\'warning from pychat\' --text=\'' + mes + '\'')

def error(mes):
    'print [mes] on a new windows as an error'
    os.system('zenity 2> /dev/null --error \
            --title=\'warning from pychat\' --text=\'' + mes + '\'')
