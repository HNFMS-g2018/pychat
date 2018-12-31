#!/usr/bin/python3
'Pychat!'
import time
import getpass
import argparse
import colorama
import leancloud

VERSION = 1.0
PARSER = argparse.ArgumentParser(description='this is help')
PARSER.add_argument('-r', '--register', action='store_true', help='register a user')
PARSER.add_argument('-l', '--login', action='store_true', help='register a user')
ARGS = PARSER.parse_args()

leancloud.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")
colorama.init()

Chat = leancloud.Object.extend('talk')
Notice = leancloud.Object.extend('notice')
todo = Chat.create_without_data('5c29b63afb4ffe005fb0de88')

def printinfo(): # {{{1
    'print infomation'
    todo.fetch()
    ptr = todo.get('point')
    talk = todo.get('contents')
    size = todo.get('size')
    for i in range(ptr+1, size):
        print(talk[i])
    for i in range(ptr+1):
        if talk[i]:
            print(talk[i])

def login_register(user, types): # {{{1
    'get a user'
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
    return 0

def first(user): # {{{1
    'first join in'
    if ARGS.login:
        login_register(user, 'login')
    elif ARGS.register:
        login_register(user, 'register')
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
    talk[ptr] = user.get('username') + ' at ' + time.strftime("%D:%H:%M") + ': ' + con
    todo.set('point', ptr)
    todo.set('times', times)
    todo.set('contents', talk)
    todo.save()

def welcome(): # {{{1
    'welcome screen'
    print(colorama.Fore.BLUE, end='')
    print('┌─────────────────────────┐')
    print('│      Welcome !!!        │')
    print('│                         │')
    print('│  p   y   c   h   a   t  │')
    print('│   VERSION:  ', VERSION, '       │')
    print('│                         │')
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
    if com in ('r', 'redarw'):
        pass
    else:
        res2 = 'No such a cammond!'
    return res1, res2

def main(): # {{{1
    'Main function'
    user = leancloud.User()
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

RES = main()
# os.system("clear")
exit(RES)
