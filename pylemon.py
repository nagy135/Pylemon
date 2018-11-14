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

        # sets order of modules
        self.states = {
                'volume': False,
                'brightness': False,
                'battery': False,
                'redshift': False,
                'layout': False,
                'date': False,
                'music': False,
                'workspaces': False
        }

        self.functions = {
                'volume': self.get_volume,
                'brightness': self.get_brightness,
                'battery': self.get_battery,
                'date': self.get_date,
                'layout': self.get_layout,
                'redshift': self.get_redshift,
                'music': self.get_music,
                'workspaces': self.get_workspaces
        }

        self.positions = {
                'volume': 'right',
                'brightness': 'right',
                'battery': 'right',
                'layout': 'right',
                'date': 'right',
                'redshift': 'right',
                'music': 'left',
                'workspaces': 'center'
        }

        self.lemon_pipe = subprocess.Popen(['lemonbar', '-p', '-f', 'Monaco-12', '-f', 'Awesome-13', '-B', '#000000', '-F', '#CCCCCC', '-g', '1920x25+0+0'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        subprocess.Popen(['/home/infiniter/Code/Pylemon/pylemon_wakeup', '2'])
        subprocess.Popen(['/home/infiniter/Code/Pylemon/subscribe_workspaces'])
        self.run()

    def get_date(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/date'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_layout(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/layout'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_redshift(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/redshift'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_music(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/music'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_battery(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/battery'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_brightness(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/brightness'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_workspaces(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/workspaces'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    def get_volume(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/volume'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')


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
        elif target == 'brightness':
            self.states['brightness'] = False
        elif target == 'redshift':
            self.states['redshift'] = False
        elif target == 'music':
            self.states['music'] = False
        elif target == 'layout':
            self.states['layout'] = False
        elif target == 'workspaces':
            self.states['workspaces'] = False
        elif target == 'volume':
            self.states['volume'] = False
        self.refresh()
    def refresh_timer(self, *args, **kwargs):
        for key in self.states:
            self.states[key] = False
        self.refresh()

    def refresh(self):
        for key in self.states:
            if self.states[key] is False:
                self.outputs[self.positions[key]][key] = self.functions[key]()
                self.states[key] = True
        left = '%{l}' + ' | '.join(list(self.outputs['left'].values()))
        center = '%{c}' + ' | '.join(list(self.outputs['center'].values()))
        right = '%{r}' + ' | '.join(list(self.outputs['right'].values()))
        self.lemon_pipe.stdin.write('{}'.format(left + center + right).encode('utf-8'))
        self.lemon_pipe.stdin.flush()



    def run(self):
        signal.signal(signal.SIGSEGV, self.refresh_timer)
        signal.signal(signal.SIGUSR1, self.refresh_user)
        # initial pain
        self.refresh()
        while True:
            signal.pause()
if __name__ == '__main__':
    instance = Pylemon()
