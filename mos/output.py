
from definitions import State
from process import Process
from definitions import Priority
from io_channel import IOChannel

class Output(Process):
    
    def __init__(self):
        Process.__init__(self, state=State.BLOCKED, priority=Priority.HIGH)
        
    def run(self):
        vm, output = IOChannel.get_output()
        vm.state = State.BLOCKED
        vm.put_to_end
        Output.stream = output
        Output.vm = vm
        if IOChannel.output_buffer == {}:
            self.state = State.BLOCKED
