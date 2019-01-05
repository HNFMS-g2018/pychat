#!/usr/bin/python3
'Pychat!'
import time
import os
import colorama
import leancloud as AV
import yaml
import threading
import _user
import _args
import _messagebox

AV.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
colorama.init()

VERSION = 1.3
CONFIGDIR = os.path.expandvars('$HOME') + '/.config/pychat/'
ARGS = _args.init()
Chat = AV.Object.extend('talk')
Notice = AV.Object.extend('notice')
todo = Chat.create_without_data('5c29b63afb4ffe005fb0de88')
config = yaml.load(open(CONFIGDIR + 'init.yaml'))

def printinfo(): # {{{1
    'print infomation'
    todo.fetch()
    ptr = todo.get('point')
    talk = todo.get('contents')
    size = todo.get('size')
    for i in range(ptr+1, size):
        if len(talk[i]) == 3:
            print(colorama.Fore.BLUE, talk[i][0], colorama.Style.RESET_ALL, \
                talk[i][1], ': ', talk[i][2])
    for i in range(ptr+1):
        if len(talk[i]) == 3:
            print(colorama.Fore.BLUE, talk[i][0], colorama.Style.RESET_ALL, \
                talk[i][1], ': ', talk[i][2])

def monitor(): # {{{1
    'listening for new messages'
    last = 0
    while True:
        todo.fetch()
        times = todo.get('times')
        if last == 0:
            last = times
        elif times > last:
            _messagebox.info('New message!')
            last = times

def updateinfo(user, con): # {{{1
    'update information'
    todo.fetch()
    ptr = todo.get('point') + 1
    times = todo.get('times') + 1
    talk = todo.get('contents')
    size = todo.get('size')
    if ptr == size:
        ptr = 0
    talk[ptr] = [user.get('username'), time.strftime("%D:%H:%M"), con]
    todo.set('point', ptr)
    todo.set('times', times)
    todo.set('contents', talk)
    todo.save()

def welcome(): # {{{1
    'welcome screen'
    print(colorama.Fore.BLUE, end='')
    print('┌─────────────────────────┐')
    print('│        Welcome !!!      │')
    print('│                         │')
    print('│  p   y   c   h   a   t  │')
    print('│                         │')
    print('│     VERSION:  ', VERSION, '     │')
    print('└─────────────────────────┘')
    info = Notice.create_without_data('5c29d4ab9f5454007005488b')
    info.fetch()
    print(colorama.Fore.RED, 'Notice:\n', info.get('content'))
    print(colorama.Style.RESET_ALL)

def cammond(com): # {{{1
    'deal with a cammond'
    res1, res2 = 'null', ''
    if com in ('quit', 'q'):
        res1, res2 = 'quit', 'You quited!'
    elif com in ('w', 'who'):
        pass
    elif com in ('h', 'help'):
        res2 = 'This is help message:\n \
                use q[uit] to quit\n \
                use h[elp] to get help\n \
                use e[dit] to edit configuration file\n'
    elif com in ('e', 'edit'):
        os.system('edit ~/.config/pychat/init.yaml')
        res2 = 'editing'
    else:
        res2 = 'No such a cammond!'
    return res1, res2

def main(): # {{{1
    'Main function'
    user = AV.User()
    welcome()
    threading._start_new_thread(monitor, ())
    if _user.init(user, ARGS, config) == 1:
        print('failed')
        return 1
    caminfo = ''
    while True:
        # os.system("clear")
        printinfo()
        print(caminfo)
        con = input('Input yours(input :h to get help)$ ')
        comres = 'null'
        if con == '':
            caminfo = 'input EMPTY!'
            continue
        elif con[0] == ':':
            comres, caminfo = cammond(con[1:])
        else:
            updateinfo(user, con)
            caminfo = ''
        if comres == 'quit':
            break

# }}}1

if __name__ == '__main__':
    try:
        res = main()
        # os.system("clear")
        exit(res)
    except EOFError as err:
        print(colorama.Fore.RED)
        print('Unexcept EOF!', colorama.Style.RESET_ALL)
        exit(1)
    except KeyboardInterrupt as err:
        print(colorama.Fore.RED)
        print('Unexcept Ctrl-C!', colorama.Style.RESET_ALL)
        exit(1)
    except TypeError as err:
        print(colorama.Fore.RED)
        print(err, colorama.Style.RESET_ALL)
        exit(1)
