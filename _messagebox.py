'Messagebox'
import os

def info(mes):
    'print info on a new window'
    os.system('zenity --info --text=' + mes)
