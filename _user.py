'User do'
import readline
import getpass
import colorama
import leancloud as AV

class UserError(Exception):
    'a error to raise'
    def __init__(self, value):
        Exception.__init__(self, value)

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
            passwd2 = getpass.getpass('Password again: ')
            if passwd != passwd2:
                raise UserError('There\' difference between the two password')
            if name.count(' '):
                raise UserError('Space is not allow')
            user.set_username(name)
            user.set_password(passwd)
            user.sign_up()
        else:
            return 1
    except (AV.errors.LeanCloudError, UserError) as err:
        print()
        print('error!')
        print(colorama.Fore.RED, err, colorama.Style.RESET_ALL)
        exit(2)
    return 0

def email(user): # {{{1
    'set email for [user]'
    mail = input('Your email: ')
    user.set_email(mail)
    user.save()

def init(user, args, config): # {{{1
    'first join in'
    if args.login:
        login_register(user, 'login')
    elif args.register:
        login_register(user, 'register')
    elif config.get('name') and config.get('pass'):
        user.login(config['name'], config['pass'])
    else:
        choose = input('login or register? ')
        return login_register(user, choose)
    return 0
