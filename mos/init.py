
from process import Process
from definitions import Priority
from definitions import State
from load import Load
from interrupt import Interrupt
from main import Main
from watchdog import Watchdog



#the father process of whole OS
#it starts intermediate processes and blocks waiting till OS is halted
class Init(Process):
    def __init__(self):
        #state ready because it has to be runned first as soon as OS starts   
        Process.__init__(self, state=State.READY, priority=Priority.HIGH)


    def run(self):
        #creates 4 process which will serve users programs
        Load()
        Interrupt()
        Main()
        Watchdog()
        self.state = State.BLOCKED

