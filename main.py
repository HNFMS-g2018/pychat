#!/usr/bin/python3
import leancloud
import time

leancloud.init("IDDU0rkX0FJ9hi2SFQgP1YIt-gzGzoHsz", "K3zSqgPWAssTN9kyKWDJWG8y")

Chat = leancloud.Object.extend('talk')
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

def first(user): # {{{1
    'first join in'
    info = Chat.create_without_data('5c29b63afb4ffe005fb0de88')
    info.fetch()
    print('Notice:\n', info.get('content'))
    choose = input('login or register? ')
    if choose == '':
        return 'fail'
    if choose[0] == 'l':
        name = input('User name:')
        passwd = input('Password:')
        user.login(name, passwd)
    elif choose[0] == 'r':
        name = input('User name:')
        passwd = input('Password:')
        user.set_username(name)
        user.set_password(passwd)
        user.sign_up()
    else:
        return 'fail'

def updateinfo(user, con): # {{{1
    'update information'
    todo.fetch()
    ptr = todo.get('point') + 1
    talk = todo.get('contents')
    if ptr == 100:
        ptr = 0
    talk[ptr] = user.get('username') + ': ' + con
    todo.set('contents', talk)
    todo.set('point', ptr)
    todo.save()

def main(): # {{{1
    'Main function'
    user = leancloud.User()
    if first(user) == 'fail':
        print('failed')
        return 1
    while True:
        printinfo()
        con = input('Input yours(press :q to quit): ')
        if con in ('fuck', ':q'):
            break
        else:
            updateinfo(user, con)

# }}}1

RES = main()
exit(RES)
