'Make a monitor'
import threading
import time
import _messagebox

class Monitor(threading.Thread):
    'a Monitor'
    # last = 0
    # todo = None
    def __init__(self, todo): # {{{2
        threading.Thread.__init__(self)
        self.todo = todo
        self.last = 0
        self.stoped = False

    def run(self): # {{{2
        'listening for new messages'
        while not self.stoped:
            self.todo.fetch()
            times = self.todo.get('times')
            if self.last == 0:
                self.last = times
            elif times > self.last:
                _messagebox.info('New message!')
                self.last = times
            endtime = time.time() + 60
            while not self.stoped and time.time() < endtime:
                time.sleep(1)

    def send(self): # {{{2
        'to tell the monitor to do nothing'
        self.last -= 1

    def tostop(self): # {{{2
        'to stop running'
        self.stoped = True
