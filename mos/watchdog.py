
from process import Process
from definitions import State
from definitions import Priority
from rm import RM


#process responsible for lifecycle of user's programs
class Watchdog(Process):
    def __init__(self):
        Process.__init__(self, state=State.READY, priority=Priority.MEDIUM)
    
    #checks if there is no process which get into lifecycle
    def run(self):
        if(RM.current_vm and RM.current_vm.LC < 0):
            RM.SI = 4

        self.state = State.READY
