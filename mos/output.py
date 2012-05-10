from definitions import State
from process import Process
from definitions import Priority
from rm import RM
from io_channel import IOChannel


class Output(Process):
    
    def __init__(self):
        Process.__init__(self, state=State.BLOCKED, priority=Priority.HIGH)
        
    def run(self):
        vm, output = IOChannel.get_output()
        vm.state = State.BLOCKED
        Output.stream = output
        Output.vm = vm
        #print(output, end='')
        self.state = State.BLOCKED
