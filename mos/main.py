
from process import Process
from definitions import Priority
from definitions import State
from vm import VM


#it should operate with VM process
class Main(Process):
    def __init__(self):
        Process.__init__(self, priority = Priority.MEDIUM)

    #creates new VM process
    def run(self):
         VM()
         self.state = State.BLOCKED

