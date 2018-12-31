#!/usr/bin/python3
'Pychat!'
import time
import getpass
import argparse
import colorama
import leancloud

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
    for i in range(ptr+1, 100):
        print(talk[i])
    for i in range(ptr+1):
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
        print('You\'re register a new user')
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
    talk = todo.get('contents')
    if ptr == 100:
        ptr = 0
    talk[ptr] = user.get('username') + ' at ' + time.strftime("%D:%H:%M") + ': ' + con
    todo.set('contents', talk)
    todo.set('point', ptr)
    todo.save()

def welcome(): # {{{1
    'welcome screen'
    print(colorama.Fore.BLUE, end='')
    print('┌────────────────────────┐')
    print('│      Welcome !!!       │')
    print('│                        │')
    print('│  p   y   c   h   a   t │')
    print('│                        │')
    print('│                        │')
    print('└────────────────────────┘')
    info = Notice.create_without_data('5c29d4ab9f5454007005488b')
    info.fetch()
    print(colorama.Fore.RED, 'Notice:\n', info.get('content'))
    print(colorama.Style.RESET_ALL)

def main(): # {{{1
    'Main function'
    user = leancloud.User()
    welcome()
    if first(user) == 1:
        print('failed')
        return 1
    while True:
        printinfo()
        con = input('Input yours(input :q or :exit to quit): ')
        if con in ('fuck', ':q', ':exit'):
            break
        else:
            updateinfo(user, con)

# }}}1

RES = main()
exit(RES)
