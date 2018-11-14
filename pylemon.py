import signal

def eleven():
    print('eleven')
def ten():
    print('ten')
signal.signal(signal.SIGSEGV, eleven)
signal.signal(signal.SIGUSR1, ten)

while True:
  signal.pause()

class Pylemon(object):
    def __init__(self):
        self.data = list()
        self.states = {
                'date': False,
                'layout': False
        }
    def get_date(self):
        return 'mydate'
    def get_layout(self):
        return 'mylayout'
    def refresh(self):
        with open('/tmp/refresh', 'r') as t:
            target = t.read().replace('\n','')
        with open('/tmp/refresh', 'w') as t:
            t.write('')
        if target == 'date':
            self.states['date'] = False
        for key in self.states:
            if key is True
    def run(self):
        signal.signal(signal.SIGUSR1, refresh)
        while True:
            signal.pause()
