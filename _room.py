'A chat room'
import time
import colorama
import _print
import _monitor

class ChatRoom:
    'A chat room'
    def __init__(self, user, todo):
        self.todo = todo
        self.user = user
        self.mon = _monitor.Monitor(todo)
        self.mon.start()
        self.printer = _print.Printer()
        self.lastsend = time.time()
        self.__send('root', self.user.get('username') + ' join chat room!')

    def __del__(self):
        self.__send('root', self.user.get('username') + ' quit chat room!')
        self.mon.tostop()

    def __send(self, username, content):
        self.todo.fetch()
        ptr = self.todo.get('point') + 1
        times = self.todo.get('times') + 1
        talk = self.todo.get('contents')
        size = self.todo.get('size')
        while len(talk) < size:
            talk.append([])
        if ptr == size:
            ptr = 0
        talk[ptr] = make_content(username, content)
        self.todo.set('point', ptr)
        self.todo.set('times', times)
        self.todo.set('contents', talk)
        self.todo.save()
        self.mon.send()

    def printall(self):
        'print all messages of the chat room'
        self.todo.fetch()
        ptr = self.todo.get('point')
        talk = self.todo.get('contents')
        size = self.todo.get('size')
        self.printer.reset()
        for rgs in range(ptr+1, size), range(ptr+1):
            for i in rgs:
                self.printer.printamess(talk[i])

    def send(self, content):
        'send [content] to the chat room'
        nowtime = time.time()
        if nowtime < self.lastsend + 1:
            print(colorama.Fore.RED, 'input too fast!!!\n', \
                    'please wait at lease one second!', colorama.Style.RESET_ALL)
            time.sleep(1)
        else:
            self.__send(self.user.get('username'), content)
        self.lastsend = nowtime

def make_content(username, content):
    'make [content] a message'
    return [int(time.strftime('%m')), int(time.strftime('%d')), \
            int(time.strftime('%H')), int(time.strftime('%M')), \
            username, content]
