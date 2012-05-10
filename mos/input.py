from definitions import State
from process import Process
from definitions import Priority
from rm import RM
from io_channel import IOChannel


class Input(Process):
    
    def __init__(self):
        Process.__init__(self, state=State.BLOCKED, priority=Priority.HIGH)
        
    def run(self):
        #RM.current_vm.state = State.READY
        self.state = State.BLOCKED
