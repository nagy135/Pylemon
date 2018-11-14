import signal
import subprocess
import os
import time

class Pylemon(object):
    def __init__(self):
        self.outputs = dict()
        self.outputs['left'] = dict()
        self.outputs['right'] = dict()
        self.outputs['center'] = dict()

        self.states = {
                'date': False,
                'redshift': False,
                'layout': False
        }

        self.functions = {
                'date': self.get_date,
                'layout': self.get_layout,
                'redshift': self.get_redshift
        }

        self.positions = {
                'date': 'left',
                'redshift': 'left',
                'layout': 'right'
        }

        self.lemon_pipe = subprocess.Popen(['lemonbar', '-p', '-g', '1920x25+0+25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        subprocess.Popen(['./pylemon_wakeup', '2'])
        self.run()

    def get_date(self):
        return 'mydate'
    def get_layout(self):
        return 'mylayout'
    def get_redshift(self):
        return 'myredshift'

    def refresh_user(self, *args, **kwargs):
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

    def refresh(self, *args, **kwargs):
        print('refreshing')
        for key in self.states:
            if self.states[key] is False:
                self.outputs[self.positions[key]][key] = self.functions[key]()
                self.states[key] = True
        left = '%{l}' + ' | '.join(list(self.outputs['left'].values()))
        center = '%{c}' + ' | '.join(list(self.outputs['center'].values()))
        right = '%{r}' + ' | '.join(list(self.outputs['right'].values()))
        # self.lemon_pipe.stdin.write('Hello there'.encode('utf-8'))
        self.lemon_pipe.stdin.write('{}'.format(left + center + right).encode('utf-8'))
        self.lemon_pipe.stdin.flush()



    def run(self):
        signal.signal(signal.SIGSEGV, self.refresh)
        signal.signal(signal.SIGUSR1, self.refresh_user)
        # initial pain
        self.refresh()
        while True:
            signal.pause()
instance = Pylemon()
