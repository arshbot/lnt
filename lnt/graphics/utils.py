import sys
import threading
import itertools
import time

from PyInquirer import style_from_dict, Token, prompt, Separator

def ratio_graphic(local, remote):
    total = local + remote
    local_ratio = int((round(local/total, 1) * 10) / 2)
    remote_ratio = int((round(remote/total, 1) * 10) / 2)

    return local_ratio * "🁢" + ( (5 - local_ratio) * "-" )  + ( (5 - remote_ratio) * "-" ) + remote_ratio * "🁢"

def vars_to_string(chan_id, local_balance, remote_balance, nick=None):
    total_balance = local_balance + remote_balance
    nick = "-" if nick == None else nick
    # TODO, pretty this up -> https://stackoverflow.com/a/9996049/5838056
    return "{}, {}, {}, {}, {}".format(nick, chan_id, local_balance,
            remote_balance, ratio_graphic(local_balance, remote_balance))

class Spinner:

    def __init__(self, message, delay=0.1):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        sys.stdout.write(message)

    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(next(self.spinner))
                self.spinner_visible = True
                sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')       # overwrite spinner with blank
                    sys.stdout.write('\r')      # move to next line
                sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\r')
