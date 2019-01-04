#!/usr/bin/python3
'Pychat!'
import time
import getpass
import argparse
import os
import colorama
import leancloud as AV
import yaml

VERSION = 1.2
CONFIGDIR = os.path.expandvars('$HOME') + '/.config/pychat/'

PARSER = argparse.ArgumentParser(description='this is help')
PARSER.add_argument('-r', '--register', action='store_true', help='register a user')
PARSER.add_argument('-l', '--login', action='store_true', help='login a user')
ARGS = PARSER.parse_args()

AV.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
colorama.init()

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

def login_register(user, types): # {{{1
    'get a user'
    try:
        if types == '':
            return 1
        if types[0] == 'l':
            name = input('User name: ')
            passwd = getpass.getpass('Password: ')
            user.login(name, passwd)
        elif types[0] == 'r':
            print('You\'re registering a new user')
            name = input('User name: ')
            passwd = getpass.getpass('Password: ')
            user.set_username(name)
            user.set_password(passwd)
            user.sign_up()
        else:
            return 1
    except AV.errors.LeanCloudError as err:
        print('error!')
        print(colorama.Fore.RED, err, colorama.Style.RESET_ALL)
        exit(1)
    return 0

def first(user): # {{{1
    'first join in'
    if ARGS.login:
        login_register(user, 'login')
    elif ARGS.register:
        login_register(user, 'register')
    elif config.get('name') and config.get('pass'):
        user.login(config['name'], config['pass'])
    else:
        choose = input('login or register? ')
        return login_register(user, choose)
    return 0

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
    if com in ('quit', 'q', 'exit'):
        res1, res2 = 'quit', 'You quited!'
    elif com in ('w', 'who'):
        pass
    elif com in ('h', 'help'):
        res2 = 'No help!!! It\'s easy enough!!!'
    else:
        res2 = 'No such a cammond!'
    return res1, res2

def main(): # {{{1
    'Main function'
    user = AV.User()
    welcome()
    if first(user) == 1:
        print('failed')
        return 1
    caminfo = ''
    while True:
        # os.system("clear")
        printinfo()
        print(caminfo)
        con = input('Input yours(input :q or :exit to quit)$ ')
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
    except KeyboardInterrupt as err:
        print(colorama.Fore.RED)
        print('Unexcept Ctrl-C!', colorama.Style.RESET_ALL)
