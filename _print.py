'print meesage on the screen'
import colorama

class Printer:
    'To print something'
    def __init__(self):
        self.last_month = 0
        self.last_day = 0
        self.last_hour = 0
        self.last_minute = 0
    def __upd_month(self, content):
        self.last_month = content[0]
        self.__upd_day(content)
    def __upd_day(self, content):
        self.last_day = content[1]
        self.__upd_hour(content)
    def __upd_hour(self, content):
        self.last_hour = content[2]
        self.__upd_minute(content)
    def __upd_minute(self, content):
        self.last_minute = content[3]
    def reset(self):
        'reset time'
        self.last_month = 0
        self.last_day = 0
        self.last_hour = 0
        self.last_minute = 0
    def printamess(self, content):
        'print one message on the screen'
        if len(content) == 6:
            ptime = True
            for i in range(4):
                content[i] = int(content[i])
            if content[0] > self.last_month:
                self.__upd_month(content)
            elif content[1] > self.last_day:
                self.__upd_day(content)
            elif content[2] > self.last_hour:
                self.__upd_hour(content)
            elif content[3] > self.last_minute + 1:
                self.__upd_minute(content)
            else:
                ptime = False
            if ptime:
                print_time(content)
            color = colorama.Fore.BLUE
            if content[4] == 'root':
                color = colorama.Fore.RED
            print(color, content[4] + ':', colorama.Style.RESET_ALL, \
                content[5])
        else:
            print('Outdated message')

def print_time(content):
    'print the time of a message'
    print(content[0], '.', content[1], '.' \
            , content[2], ':', content[3])
