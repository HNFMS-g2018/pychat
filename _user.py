'User do'
import readline
import getpass
import colorama
import leancloud as AV

class UserError(Exception):
    'a error to raise'
    def __init__(self, value):
        Exception.__init__(self, value)

class User: # {{{1
    'user of leancloud'
    def __init__(self):
        self.avuser = AV.User()
        self.__level = 0
        self.__need_active = 3
        self.__now_active = 0
        self.logined = None

    def get_username(self):
        'return username'
        return self.avuser.get_username()

    def get_active(self):
        'return active'
        return self.__now_active

    def get_active_tot(self):
        'return total active'
        res = self.avuser.get('active_tot')
        if not res:
            res = 0
        return res

    def get_active_need(self):
        'return active needed'
        return self.__need_active

    def add_active(self, times):
        'active += [times]'
        self.avuser.set('active_tot', self.get_active_tot() + times)
        self.__now_active += times

    def get_level(self):
        'return level'
        while self.get_active() >= self.__need_active:
            self.__now_active -= self.__need_active
            if self.__need_active < 50:
                self.__need_active += 1
            self.__level += 1
        return self.__level

    def try_save(self):
        'try to save'
        if self.logined:
            self.avuser.save()

    def login(self, username, password=None):
        'login'
        if password:
            self.avuser.login(username, password)
            self.logined = True
        else:
            self.avuser.set_username(username)
        self.try_fetch()
        self.__now_active = self.get_active_tot()

    def register(self, username, password):
        'register'
        self.avuser.sign_up(username, password)
        self.login(username, password)

    def try_fetch(self):
        'try to fetch data'
        if self.logined:
            self.avuser.fetch()

    def change_password(self, newpass):
        'change password to [newpass]'
        self.avuser.set_password(newpass)
        self.try_save()

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
            user.register(name, passwd)
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
