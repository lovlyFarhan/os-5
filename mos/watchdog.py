
from process import Process
from definitions import State
from definitions import Priority


#process responsible for lifecycle of user's programs
class Watchdog(Process):
    def __init__(self):
        Process.__init__(self, priority=Priority.MEDIUM)
    
    #checks if there is no process which get into lifecycle
    def run(self):
        pass
