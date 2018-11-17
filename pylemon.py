import atexit
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
        self.first = True
        self.separator = '  %{F#c22330}•%{F-}  '

        # sets order of modules
        self.states = {
                'torrent': False,
                'volume': False,
                'cpu': False,
                'battery': False,
                'brightness': False,
                'redshift': False,
                'wifi': False,
                'layout': False,
                'date': False,
                'music': False,
                'workspaces': False
        }

        self.functions = {
                'torrent': self.get_torrent,
                'wifi': self.get_wifi,
                'volume': self.get_volume,
                'brightness': self.get_brightness,
                'cpu': self.get_cpu,
                'battery': self.get_battery,
                'date': self.get_date,
                'layout': self.get_layout,
                'redshift': self.get_redshift,
                'music': self.get_music,
                'workspaces': self.get_workspaces
        }

        self.positions = {
                'torrent': 'right',
                'wifi': 'right',
                'volume': 'right',
                'brightness': 'right',
                'cpu': 'right',
                'battery': 'right',
                'layout': 'right',
                'date': 'right',
                'redshift': 'right',
                'music': 'left',
                'workspaces': 'center'
        }

        self.lemonbar = subprocess.Popen(['lemonbar', '-p', '-f', 'Monaco-12', '-f', 'FontAwesome-13', '-B', '#000000', '-F', '#CCCCCC', '-g', '1920x25+0+0'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        wakeup = subprocess.Popen(['/home/infiniter/Code/Pylemon/pylemon_wakeup', '5'])
        self.wakeup_pid = wakeup.pid
        sub_workspace = subprocess.Popen(['/home/infiniter/Code/Pylemon/subscribe_workspaces'])
        self.sub_workspace_pid  = sub_workspace.pid
        self.run()

    def get_date(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/date'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_layout(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/layout'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_redshift(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/redshift'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_music(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/music'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_cpu(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/cpu'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_battery(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/battery'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_brightness(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/brightness'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_workspaces(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/workspaces'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_volume(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/volume'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_wifi(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/wifi'], stdout=subprocess.PIPE)
        return result.stdout.decode()
    def get_torrent(self):
        result = subprocess.run(['/home/infiniter/Code/Pylemon/torrent'], stdout=subprocess.PIPE)
        return result.stdout.decode()

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
        left = '%{l}' + self.separator.join([x for x in self.outputs['left'].values() if x != ''])
        center = '%{c}' + self.separator.join([x for x in self.outputs['center'].values() if x != ''])
        right = '%{r}' + self.separator.join([x for x in self.outputs['right'].values() if x != ''])
        self.lemonbar.stdin.write(' {} '.format(left + center + right).encode())
        self.lemonbar.stdin.flush()

    def run(self):
        signal.signal(signal.SIGSEGV, self.refresh_timer)
        signal.signal(signal.SIGUSR1, self.refresh_user)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        # initial paint
        self.refresh()
        while True:
            signal.pause()

    def kill_child_processes():
        print('cleaning up child processes')
        subprocess.Popen(['pkill', '-f', 'pylemon_wakeup'])
        subprocess.Popen(['pkill', '-f', 'subscribe_workspaces'])
        subprocess.Popen(['pkill', '-f', 'stalonetray'])
        subprocess.Popen(['killall', 'lemonbar'])

if __name__ == '__main__':
    atexit.register(Pylemon.kill_child_processes)
    instance = Pylemon()
