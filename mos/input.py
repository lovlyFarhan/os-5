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
        Input.vmNr = RM.current_vm.PAGE
        
        
        if IOChannel.input_buffer.__len__() != 0:
            vm, rcvStream = IOChannel.get_input()
            RM.memory[vm.SP] = rcvStream
            vm.state = State.READY
        
        
        
        self.state = State.WAITING