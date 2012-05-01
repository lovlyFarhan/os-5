
from process import Process
from definitions import Priority
from definitions import State
from load import Load
from interrupt import Interrupt
from main import Main
from watchdog import Watchdog



class Init(Process):
    def __init__(self):
        Process.__init__(self, State.READY, Priority.HIGH)


    def run(self):
        Load()
        Interrupt()
        Main()
        Watchdog()

