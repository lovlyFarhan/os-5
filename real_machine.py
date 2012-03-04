
from virtual_machine import VirtualMachine

class Proccess():
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.commands = [line.rstrip('\n') for line in file if line[0] != '#']


class RealMachine():
    def __init__(self):
        self.clear_mem()
        
    def clear_mem(self):
        self.memory = {i : "" for i in ("%X" %i for i in range(256))}

    def start_vm(self, file_name):
        self.vm = VirtualMachine(Proccess(file_name), self.memory)


rm = RealMachine()
rm.start_vm('first.pr')

