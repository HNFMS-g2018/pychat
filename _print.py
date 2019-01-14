'print meesage on the screen'
import colorama

class Printer:
    'To print something'
    def __init__(self):
        self.last_time = [0, 0, 0, 0,]
        self.allow = [0, 0, 0, 2,]
        self.time_size = 4

    def __upd_time(self, content, now):
        self.last_time[now] = content[now]
        if now < self.time_size - 1:
            self.__upd_time(content, now+1)

    def reset(self):
        'reset time'
        self.last_time = [0, 0, 0, 0,]

    def printamess(self, content):
        'print one message on the screen'
        if len(content) == self.time_size + 2:
            ptime = False
            for i in range(self.time_size):
                content[i] = int(content[i])
            for i in range(self.time_size):
                if content[i] < self.last_time[i] \
                        or content[i] > self.last_time[i] + self.allow[i]:
                    self.__upd_time(content, i)
                    ptime = True
                    break
            if ptime:
                print_time(content)
            color = colorama.Fore.BLUE
            if content[self.time_size] == 'root':
                color = colorama.Fore.RED
            print(color, content[self.time_size] + ':', \
                    colorama.Style.RESET_ALL, end=' ')
            print_text(content[self.time_size + 1])
        else:
            print('Outdated message')

def print_time(content):
    'print the time of a message'
    print(content[0], '.', content[1], '.' \
            , content[2], ':', content[3])

def print_text(content):
    'print [content] after processing'
    deal = False
    for i in content:
        if deal:
            if i == 'n':
                print()
            elif i == 'R':
                print(colorama.Fore.RED, end='')
            elif i == 'B':
                print(colorama.Fore.BLUE, end='')
            elif i == 'G':
                print(colorama.Fore.GREEN, end='')
            elif i == 'Y':
                print(colorama.Fore.YELLOW, end='')
            elif i == '0':
                print(colorama.Style.RESET_ALL, end='')
            deal = False
        else:
            if i == '\\':
                deal = True
            else:
                print(i, end='')
    print(colorama.Style.RESET_ALL)
