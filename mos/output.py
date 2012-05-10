from definitions import State
from process import Process
from definitions import Priority
from rm import RM
from vm import VM


class Output(Process):
    
    String = ""

    def __init__(self):
        Process.__init__(self, state=State.BLOCKED, priority=Priority.MEDIUM)
        
    def run(self):
        
        Output.String = VM.Output
        
        
        self.state = State.BLOCKED
        RM.current_vm.state = State.READY