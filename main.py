#!/usr/bin/python3
'Pychat!'
import readline
import os
import colorama
import leancloud as AV
import yaml
import _user
import _args
import _curse
import _room

VERSION = 1.5
CONFIGDIR = os.path.expandvars('$HOME') + '/.config/pychat/'
ARGS = _args.init()
Chat = AV.Object.extend('talk')
Notice = AV.Object.extend('notice')
config = yaml.load(open(CONFIGDIR + 'init.yaml'))
AV.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
# AV.init('ULc6VQsRiQr4NENpfoJpfd52-gzGzoHsz', 'iYA2I9QBd6SJ1fwGOQxceyQD')
colorama.init()

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
        res1 = 'who'
    elif com in ('p', 'printall'):
        res1 = 'printall'
    elif com in ('h', 'help'):
        res2 = 'This is help message:\n \
                use q[uit] to quit\n \
                use h[elp] to get help\n \
                use p[rint] to print all messages\n \
                use e[dit] to edit configuration file'
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
    camres, caminfo = '', ''
    room = _room.ChatRoom(user, \
            Chat.create_without_data('5c29b63afb4ffe005fb0de88'))
            # Chat.create_without_data('5c30264bfb4ffe005fd22a11'))
    while True:
        if camres == 'printall':
            room.printall()
        else:
            room.printnew()
        if caminfo != '':
            print(caminfo)
        if camres == 'who':
            print(room.user_list())
        con = input('Input yours(input :h to get help)$ ')
        _curse.cup(1)
        print('                                                                                ')
        _curse.cup(1)
        camres = 'null'
        if con == '':
            caminfo = 'input EMPTY!'
            continue
        elif con[0] == ':':
            camres, caminfo = cammond(con[1:])
        else:
            room.send(con)
            caminfo = ''
        if camres == 'quit':
            break

def toexit(res): # {{{1
    'to exit the execute and return [res]'
    exit(res)

if __name__ == '__main__': # {{{1
    try:
        # os.system('cd ~/.config/pychat/upstream/; git pull; make;')
        toexit(main())
    except EOFError as err:
        print(colorama.Fore.RED)
        print('Unexcept EOF!', colorama.Style.RESET_ALL)
        toexit(1)
    except KeyboardInterrupt as err:
        print(colorama.Fore.RED)
        print('Unexcept Ctrl-C!', colorama.Style.RESET_ALL)
        toexit(1)

# }}}1
