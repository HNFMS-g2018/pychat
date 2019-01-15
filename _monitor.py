'Make a monitor'
import threading
import time
import _messagebox

class Monitor(threading.Thread): # {{{1
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
            # _messagebox.info(str(times) + 'vs' + str(self.last))
            if self.last == 0:
                self.last = times
            elif times > self.last:
                _messagebox.info(str(times-self.last) + ' new messages!')
                self.last = times
            endtime = time.time() + 120
            while not self.stoped and time.time() < endtime:
                time.sleep(1)

    def send(self, times): # {{{2
        'to tell the monitor to do nothing'
        # self.todo.fetch()
        # self.last = self.todo.get('times')
        self.last = times

    def tostop(self): # {{{2
        'to stop running'
        self.stoped = True
        self.join()
