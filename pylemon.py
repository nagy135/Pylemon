import signal
import subprocess
import os

class Pylemon(object):
    def __init__(self):
        self.outputs = dict()
        self.outputs['left'] = dict()
        self.outputs['right'] = dict()
        self.outputs['center'] = dict()

        self.states = {
                'date': False,
                'layout': False
        }

        self.functions = {
                'date': self.get_date,
                'layout': self.get_layout
        }

        self.positions = {
                'date': 'left',
                'layout': 'right'
        }

        self.lemon_pid = subprocess.Popen(['lemonbar', '-p', '&'], stdin=subprocess.PIPE)
        self.lemon_pid = self.lemon_pid.pid
        subprocess.Popen(['/home/infiniter/Code/Pylemon/pylemon_wakeup', '2'])
        self.run()

    def get_date(self):
        return 'mydate'
    def get_layout(self):
        return 'mylayout'

    def refresh_user(self):
        try:
            with open('/tmp/refresh', 'r') as t:
                target = t.read().replace('\n','')
            with open('/tmp/refresh', 'w') as t:
                t.write('')
        except FileNotFoundError:
            with open('/tmp/refresh', 'w') as t:
                t.write('')
            return
        if target == 'date':
            self.states['date'] = False
        if target == 'layout':
            self.states['layout'] = False
        self.refresh()

    def refresh(self):
        for key in self.states:
            if self.states[key] is False:
                self.outputs[self.positions[key]][key] = self.functions[key]()
                self.states[key] = True
        left = '%{l}' + ''.join(self.outputs['left'])
        center = '%{c}' + ''.join(self.outputs['center'])
        right = '%{r}' + ''.join(self.outputs['right'])
        assert False, str(self.lemon_pid)
        with open(os.path.join('/proc', str(self.lemon_pid), 'fd', '1'), 'a') as stdin:
            stdin.write('Hello there\n')



    def run(self):
        signal.signal(signal.SIGSEGV, self.refresh)
        signal.signal(signal.SIGUSR1, self.refresh_user)
        # initial pain
        self.refresh()
        while True:
            signal.pause()
instance = Pylemon()
