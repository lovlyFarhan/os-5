
from process import Process
from definitions import Priority
from definitions import State
from vm import VM


#it should operate with jobGovernor process
class Main(Process):
    def __init__(self):
        Process.__init__(self, Priority.MEDIUM)

    #creates new jobGovernor instance?
    def run(self):
         VM()
         self.state = State.BLOCKED

