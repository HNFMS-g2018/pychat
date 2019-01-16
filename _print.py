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
            color = colorama.Fore.CYAN
            begin = ''
            if content[self.time_size] == 'root':
                color = colorama.Fore.LIGHTYELLOW_EX
                begin = '\\Y'
            print('', content[self.time_size] + ': ', end='')
            print_text(begin + content[self.time_size + 1])
            print(colorama.Cursor.UP(1), end='')
            print(color, content[self.time_size] + ':', \
                    colorama.Style.RESET_ALL)
        else:
            print('Outdated message')

def print_time(content):
    'print the time of a message'
    print(content[0], '月', content[1], '日' \
            , content[2], '时', content[3], '分')

def print_text(content):
    'print [content] after processing'
    content = dealstr(content)
    deal = False
    for i in content:
        if deal:
            if i == 'n':
                print()
                print('> ', end='')
            elif i == 'R':
                print(colorama.Fore.RED, end='')
            elif i == 'B':
                print(colorama.Fore.BLUE, end='')
            elif i == 'G':
                print(colorama.Fore.GREEN, end='')
            elif i == 'Y':
                print(colorama.Fore.YELLOW, end='')
            elif i == 'P':
                print(colorama.Fore.MAGENTA, end='')
            elif i == '0':
                print(colorama.Style.RESET_ALL, end='')
            elif i == '\\':
                print('\\', end='')
            deal = False
        else:
            if i == '\\':
                deal = True
            else:
                print(i, end='')
    print(colorama.Style.RESET_ALL)

BAN_LIST = ['ak', 'ioi', 'irc', 'fuck']

def dealstr(content):
    'deal with string [content] and return it'
    if len(content) > 50:
        content = '\\R我他妈发了一个超长的句子，怕辣你们眼睛'
    elif '' in content:
        content = '\\R我他妈发了一个有终端控制符的句子，怕辣你们眼睛'
    else:
        for ban in BAN_LIST:
            while content.find(ban) != -1:
                pos = content.find(ban)
                if pos == 0:
                    string = '\\R***\\0' + content[len(ban):]
                else:
                    string = content[:pos-1] + '\\R***\\0' + content[pos+len(ban):]
                content = string
    return content
