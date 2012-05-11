
from definitions import State
from process import Process
from definitions import Priority
from io_channel import IOChannel
from rm import RM


class Input(Process):
    
    def __init__(self):
        Process.__init__(self, state=State.BLOCKED, priority=Priority.HIGH)
        
    def run(self):
        input_waiting_vm = IOChannel.input_waiting_queue[0]
        input = IOChannel.input_buffer.get(input_waiting_vm)
        if input != None:
            del IOChannel.input_buffer[input_waiting_vm]
            vm_sp = input_waiting_vm.PAGE * 256 + input_waiting_vm.SP
            RM.memory[vm_sp] = input
            input_waiting_vm.state = State.BLOCKED
            IOChannel.input_waiting_queue.pop(0)
            if IOChannel.rotate_iwq():
                self.state = State.BLOCKED
            Input.vm_page = None
        else:
            Input.vm_page = input_waiting_vm.PAGE
            self.state = State.READY



