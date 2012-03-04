

class VirtualMachine:
    def __init__(self, proc, rm_memory):
        self.memory = rm_memory
        self.DS = "00"
        self.CS = "40"
        self.SS = "A0"
        self.IP = self.CS
        self.SP = self.SS
        
    def fill_mem(self, proc):
        for i in range(256):
            if i < len(proc.commands):
                self.memory[i] = proc.commands[i]
            else:
                self.memory[i] = ""
            
            
