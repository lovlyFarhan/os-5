
from process import Process
from definitions import State


class Watchdog(Process):
    def __init__(self):
        Process.__init__(self, State.BLOCKED)
    

    def run(self):
        pass
