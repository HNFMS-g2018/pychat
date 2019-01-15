'A chat room'
import readline
import time
import colorama
import _print
import _monitor
import _messagebox

class ChatRoom: # {{{1
    'A chat room'
    def __init__(self, user, todo): # {{{2
        self.todo = todo
        self.user = user
        self.mon = _monitor.Monitor(todo)
        self.mon.start()
        self.printer = _print.Printer()
        self.lastsend = time.time()
        self.lastprint = 0
        users = self.user_list()
        username = self.user.get('username')
        join_succes = True
        if users.count(username):
            join_succes = False
            _messagebox.warning('Warning: User has logined in')
            chos = input('!If you are the only user named that, type ok')
            if chos == 'ok':
                while users.count(username):
                    users.remove(username)
        users.append(username)
        self.todo.set('users', users)
        self.todo.save()
        if join_succes:
            self.__send('root', username + ' join chat room!')

    def __del__(self): # {{{2
        self.mon.tostop()
        users = self.user_list()
        username = self.user.get('username')
        quit_succes = True
        if users.count(username) > 1:
            quit_succes = False
            _messagebox.warning('Warning: There are other same user')
        users.remove(username)
        self.todo.set('users', users)
        self.todo.save()
        self.user.save()
        if quit_succes:
            self.__send('root', self.user.get('username') + ' quit chat room!')

    def __send(self, username, content): # {{{2
        self.todo.fetch()
        ptr = self.todo.get('point') + 1
        times = self.todo.get('times') + 1
        talk = self.todo.get('contents')
        size = self.todo.get('size')
        for i in talk:
            if len(i[5]) > 50:
                i[5] = '我他妈发了一个超长的句子，怕辣你们眼睛'
        while len(talk) < size:
            talk.append([])
        if ptr == size:
            ptr = 0
        talk[ptr] = make_content(username, content)
        self.todo.set('point', ptr)
        self.todo.set('times', times)
        self.todo.set('contents', talk)
        self.todo.save()
        self.mon.send(times)

    def printall(self, printroot=True): # {{{2
        '''
        print all messages of the chat room
        if [printroot] is true, donot print root h \'s messages
        '''
        self.todo.fetch()
        ptr = self.todo.get('point')
        talk = self.todo.get('contents')
        size = self.todo.get('size')
        self.printer.reset()
        print('————————————————————')
        for rgs in range(ptr+1, size), range(ptr+1):
            for i in rgs:
                if printroot or talk[i][4] != 'root':
                    self.printer.printamess(talk[i])

    def printnew(self): # {{{2
        'print new messages of the chat room'
        self.todo.fetch()
        ptr = self.todo.get('point')
        talk = self.todo.get('contents')
        size = self.todo.get('size')
        times = self.todo.get('times')
        ptimes = times - self.lastprint
        if ptimes > size:
            ptimes = size
        for i in range(ptr-ptimes+1, ptr+1):
            if i < 0:
                i += size
            self.printer.printamess(talk[i])
        self.lastprint = times

    def send(self, content): # {{{2
        'send [content] to the chat room'
        if time.time() < self.lastsend + 1:
            print(colorama.Fore.RED, 'input too fast!!!\n', \
                    'please wait at lease one second!', colorama.Style.RESET_ALL)
            time.sleep(1)
        elif len(content) > 50:
            print(colorama.Fore.RED, 'message too long!!!\n', \
                    'please wait at lease one second!', colorama.Style.RESET_ALL)
            time.sleep(1)
        else:
            self.__send(self.user.get('username'), content)
            self.user.set('active', self.user.get('active') + 1)
        self.lastsend = time.time()

    def user_list(self): # {{{2
        'return a list of users in the chat room'
        self.todo.fetch()
        return self.todo.get('users')

    def exist(self): # {{{2
        'return if the user is still in the chat room'
        self.todo.fetch()
        users = self.user_list()
        return bool(users.count(self.user.get('username')))

def make_content(username, content): # {{{1
    'make [content] a message'
    return [int(time.strftime('%m')), int(time.strftime('%d')), \
            int(time.strftime('%H')), int(time.strftime('%M')), \
            username, content]
