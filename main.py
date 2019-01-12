#!/usr/bin/python3
'Pychat!'
import readline
import time
import os
import colorama
import leancloud as AV
import yaml
import _user
import _args
import _monitor

VERSION = 1.3
CONFIGDIR = os.path.expandvars('$HOME') + '/.config/pychat/'
ARGS = _args.init()
Chat = AV.Object.extend('talk')
Notice = AV.Object.extend('notice')
todo = Chat.create_without_data('5c29b63afb4ffe005fb0de88')
# todo = Chat.create_without_data('5c30264bfb4ffe005fd22a11')
config = yaml.load(open(CONFIGDIR + 'init.yaml'))

AV.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
# AV.init('ULc6VQsRiQr4NENpfoJpfd52-gzGzoHsz', 'iYA2I9QBd6SJ1fwGOQxceyQD')
colorama.init()

def printinfo(): # {{{1
    'print infomation'
    todo.fetch()
    ptr = todo.get('point')
    talk = todo.get('contents')
    size = todo.get('size')
    for i in range(ptr+1, size):
        if len(talk[i]) == 3:
            color = colorama.Fore.BLUE
            if talk[i][0] == 'root':
                color = colorama.Fore.RED
            print(color, talk[i][0], colorama.Style.RESET_ALL, \
                talk[i][1], ': ', talk[i][2])
    for i in range(ptr+1):
        if len(talk[i]) == 3:
            color = colorama.Fore.BLUE
            if talk[i][0] == 'root':
                color = colorama.Fore.RED
            print(color, talk[i][0], colorama.Style.RESET_ALL, \
                talk[i][1], ': ', talk[i][2])

def updateinfo(user, con, lasttime): # {{{1
    'update information'
    nowtime = time.time()
    if nowtime < lasttime + 1:
        print(colorama.Fore.RED, 'input too fast!!!\n', \
                'please wait at lease one second!', colorama.Style.RESET_ALL)
        time.sleep(1)
        return time.time()
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
    MON.send()
    return nowtime

def updatesysinfo(con): # {{{1
    'update system information'
    todo.fetch()
    ptr = todo.get('point') + 1
    times = todo.get('times') + 1
    talk = todo.get('contents')
    size = todo.get('size')
    if ptr == size:
        ptr = 0
    talk[ptr] = ['root', time.strftime("%D:%H:%M"), con]
    todo.set('point', ptr)
    todo.set('times', times)
    todo.set('contents', talk)
    todo.save()
    MON.send()

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
    # info = Notice.create_without_data('5c3025e667f35600631c87d0')
    info.fetch()
    print(colorama.Fore.RED, 'Notice:\n', info.get('content'))
    print(colorama.Style.RESET_ALL)

def call(user, name): # {{{1
    '[user] call a user named [name]'
    todo.fetch()
    calls = todo.get('calls')
    itcall = calls.get(name)
    itcall.append(user.get('username'))

def cammond(comms): # {{{1
    'deal with a cammond'
    res1, res2 = 'null', ''
    comms = comms.split(' ')
    if comms == []:
        return res1, res2
    com = comms[0]
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
    elif com in ('c', 'call'):
        pass
    else:
        res2 = 'No such a cammond!'
    return res1, res2

def main(): # {{{1
    'Main function'
    user = AV.User()
    welcome()
    if _user.init(user, ARGS, config) == 1:
        print('failed')
        return 1
    caminfo = ''
    lasttime = time.time()
    updatesysinfo(user.get('username') + ' join chat room!')
    try:
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
                lasttime = updateinfo(user, con, lasttime)
                caminfo = ''
            if comres == 'quit':
                break
    except:
        updatesysinfo(user.get('username') + ' quit chat room!')
        raise
    updatesysinfo(user.get('username') + ' quit chat room!')

def toexit(res, mon): # {{{1
    mon.tostop()
    exit(res)

if __name__ == '__main__': # {{{1
    try:
        # os.system('cd ~/.config/pychat/upstream/; git pull; make;')
        MON = _monitor.Monitor(todo)
        MON.start()
        toexit(main(), MON)
    except EOFError as err:
        print(colorama.Fore.RED)
        print('Unexcept EOF!', colorama.Style.RESET_ALL)
        toexit(1, MON)
    except KeyboardInterrupt as err:
        print(colorama.Fore.RED)
        print('Unexcept Ctrl-C!', colorama.Style.RESET_ALL)
        toexit(1, MON)
    except TypeError as err:
        print(colorama.Fore.RED)
        print(err, colorama.Style.RESET_ALL)
        toexit(1, MON)

# }}}1
